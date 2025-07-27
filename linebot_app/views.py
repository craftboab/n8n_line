import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    TextSendMessage, 
    TemplateSendMessage, 
    ButtonsTemplate, 
    MessageAction,
    MessageEvent,
    TextMessage
)
import requests
from .models import LineUser, MessageLog

logger = logging.getLogger(__name__)

# LINE Bot API初期化
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request):
    """LINE Webhookを受信するエンドポイント"""
    signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
    body = request.body.decode('utf-8')

    try:
        # LINE署名を検証
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        return HttpResponse(status=400)

    return HttpResponse(status=200)


def get_or_create_user(user_id):
    """ユーザー情報を取得または作成"""
    try:
        user = LineUser.objects.get(line_user_id=user_id)
        return user, False
    except LineUser.DoesNotExist:
        # LINE APIからユーザー情報を取得
        try:
            profile = line_bot_api.get_profile(user_id)
            user = LineUser.objects.create(
                line_user_id=user_id,
                display_name=profile.display_name,
                picture_url=profile.picture_url,
                status_message=profile.status_message,
                is_active=False  # 初期状態では未登録
            )
            logger.info(f"Created new user: {user.display_name}")
            return user, True
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            # プロフィール取得に失敗した場合のフォールバック
            user = LineUser.objects.create(
                line_user_id=user_id,
                display_name=f"User_{user_id[:8]}",
                is_active=False
            )
            return user, True


def send_to_n8n(user_id, message_text):
    """n8nのWebhookにメッセージを送信"""
    try:
        payload = {
            'user_id': user_id,
            'message': message_text,
            'timestamp': timezone.now().isoformat()
        }

        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            return result.get('response', '処理が完了しました。')
        else:
            logger.error(f"n8n webhook error: {response.status_code}")
            return '申し訳ございません。処理中にエラーが発生しました。'

    except requests.exceptions.RequestException as e:
        logger.error(f"n8n webhook request failed: {e}")
        return '申し訳ございません。システムに接続できませんでした。'


def send_registration_message(reply_token):
    """未登録ユーザーに登録誘導メッセージを送信"""
    buttons_template = TemplateSendMessage(
        alt_text='登録について',
        template=ButtonsTemplate(
            title='アカウント登録',
            text='このサービスを利用するには登録が必要です。',
            actions=[
                MessageAction(
                    label='登録する',
                    text='登録します'
                ),
                MessageAction(
                    label='詳細を見る',
                    text='詳細を教えてください'
                )
            ]
        )
    )

    line_bot_api.reply_message(reply_token, buttons_template)


def handle_text_message(event):
    """テキストメッセージを処理"""
    user_id = event.source.user_id
    message_text = event.message.text

    logger.info(f"Received message from {user_id}: {message_text}")

    # ユーザー情報を取得または作成
    user, created = get_or_create_user(user_id)

    # メッセージログを記録
    MessageLog.objects.create(
        user=user,
        message_type='text',
        message_text=message_text,
        raw_data=event.as_json_dict()
    )

    # 登録済みユーザーかチェック
    if user.is_active:
        # n8nにメッセージを転送
        response_text = send_to_n8n(user_id, message_text)

        # LINEに返信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_text)
        )
    else:
        # 未登録ユーザーには登録誘導メッセージを送信
        send_registration_message(event.reply_token)


def handle_registration(event):
    """登録関連のメッセージを処理"""
    user_id = event.source.user_id
    message_text = event.message.text

    try:
        user = LineUser.objects.get(line_user_id=user_id)

        if message_text == '登録します':
            user.is_active = True
            user.save()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='登録が完了しました！これでサービスをご利用いただけます。')
            )
        elif message_text == '詳細を教えてください':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='このサービスでは、AIを活用した自動応答機能をご提供しています。\n\n登録後は、様々な質問にお答えいたします。')
            )
        else:
            # 通常のメッセージ処理に戻る
            handle_text_message(event)

    except LineUser.DoesNotExist:
        # ユーザーが存在しない場合は新規作成
        get_or_create_user(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='ユーザー情報を取得中です。もう一度お試しください。')
        )


# デコレータを関数定義後に追加
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message_wrapper(event):
    """テキストメッセージのラッパー関数"""
    handle_text_message(event)


@handler.add(MessageEvent, message=TextMessage)
def handle_registration_wrapper(event):
    """登録関連メッセージのラッパー関数"""
    handle_registration(event) 