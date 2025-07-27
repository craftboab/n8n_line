#!/bin/bash

# Hetznerへのデプロイスクリプト

echo "🚀 アプリケーションをHetznerにデプロイします..."

# 1. 環境変数ファイルの確認
if [ ! -f .env ]; then
    echo "❌ .envファイルが見つかりません"
    echo "env.exampleをコピーして.envファイルを作成してください"
    exit 1
fi

# 2. Docker Composeの停止
echo "📦 既存のコンテナを停止..."
docker compose down

# 3. 本番環境用のDocker Composeで起動
echo "🚀 本番環境でアプリケーションを起動..."
docker compose -f docker-compose.prod.yml up -d

# 4. データベースのマイグレーション
echo "🗄️ データベースのマイグレーションを実行..."
docker compose -f docker-compose.prod.yml exec django python manage.py migrate

# 5. 静的ファイルの収集
echo "📁 静的ファイルを収集..."
docker compose -f docker-compose.prod.yml exec django python manage.py collectstatic --noinput

# 6. スーパーユーザーの作成（初回のみ）
echo "👤 スーパーユーザーを作成しますか？ (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker compose -f docker-compose.prod.yml exec django python manage.py createsuperuser
fi

echo "✅ デプロイが完了しました！"
echo "🌐 アプリケーションにアクセス:"
echo "   - n8n: http://your-domain.com"
echo "   - Django Admin: http://your-domain.com/admin/"
echo "   - LINE Bot Webhook: http://your-domain.com/linebot/webhook/" 