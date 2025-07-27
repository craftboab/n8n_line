# n8n LINE Bot Integration

Django + n8n + LINE Bot の統合アプリケーションです。LINE Botからのメッセージをn8nワークフローで処理し、自動応答を実現します。

## 🚀 機能

- **LINE Bot連携**: LINEメッセージの受信・送信
- **n8nワークフロー**: 自動化ワークフローの管理
- **Django管理画面**: ユーザー管理・メッセージログ
- **PostgreSQL**: データベース管理
- **Nginx**: リバースプロキシ・SSL対応

## 📋 前提条件

- Docker
- Docker Compose
- LINE Bot Channel（アクセストークン・チャンネルシークレット）

## 🛠️ セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/n8n-linebot.git
cd n8n-linebot
```

### 2. 環境変数の設定

```bash
# 環境変数ファイルをコピー
cp env.example .env

# 環境変数を編集
nano .env
```

以下の項目を設定してください：

```bash
# Django設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# データベース設定
DB_ENGINE=django.db.backends.postgresql
DB_NAME=linebot_db
DB_USER=linebot_user
DB_PASSWORD=linebot_password
DB_HOST=postgres
DB_PORT=5432

# LINE Bot設定
LINE_CHANNEL_ACCESS_TOKEN=your-line-channel-access-token
LINE_CHANNEL_SECRET=your-line-channel-secret

# n8n設定
N8N_WEBHOOK_URL=http://localhost:5678/webhook/n8n
```

### 3. アプリケーションの起動

```bash
# コンテナを起動
docker compose up -d

# データベースのマイグレーション
docker compose exec django python manage.py migrate

# スーパーユーザーの作成
docker compose exec django python manage.py createsuperuser
```

### 4. アクセス

- **n8n**: http://localhost:5678/
  - ユーザー名: `admin`
  - パスワード: `password`
- **Django Admin**: http://localhost:8000/admin/

## 🏗️ アーキテクチャ

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   LINE Bot  │───▶│   Django    │───▶│     n8n     │
│             │    │   (Django)  │    │  (Workflow) │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ PostgreSQL  │
                   │  (Database) │
                   └─────────────┘
```

## 📁 プロジェクト構造

```
n8n-linebot/
├── docker-compose.yml          # 開発環境用Docker Compose
├── docker-compose.prod.yml     # 本番環境用Docker Compose
├── Dockerfile                  # Djangoアプリケーション用Dockerfile
├── nginx.conf                  # Nginx設定
├── requirements.txt            # Python依存関係
├── manage.py                   # Django管理コマンド
├── linebot_app/               # LINE Botアプリケーション
│   ├── models.py              # データベースモデル
│   ├── views.py               # LINE Bot処理ロジック
│   └── urls.py                # URL設定
├── linebot_project/           # Djangoプロジェクト設定
│   ├── settings.py            # Django設定
│   └── urls.py                # メインURL設定
├── logs/                      # ログファイル
├── deploy.sh                  # デプロイスクリプト
├── DEPLOYMENT.md              # デプロイ手順書
└── README.md                  # このファイル
```

## 🔧 開発

### ローカル開発環境

```bash
# コンテナを起動
docker compose up -d

# Djangoコンテナに入る
docker compose exec django bash

# Djangoシェルを起動
python manage.py shell

# ログを確認
docker compose logs -f
```

### データベース操作

```bash
# マイグレーション
docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate

# データベースリセット
docker compose exec django python manage.py flush

# スーパーユーザー作成
docker compose exec django python manage.py createsuperuser
```

## 🚀 本番環境へのデプロイ

詳細なデプロイ手順は [DEPLOYMENT.md](./DEPLOYMENT.md) を参照してください。

### クイックデプロイ

```bash
# デプロイスクリプトを実行
chmod +x deploy.sh
./deploy.sh
```

## 📊 管理機能

### Django Admin

- **LineUser**: LINEユーザー情報の管理
- **MessageLog**: メッセージ履歴の確認

### n8n管理

- ワークフローの作成・編集
- Webhookの設定
- 自動化処理の管理

## 🔒 セキュリティ

- 環境変数による設定管理
- データベースパスワードの暗号化
- LINE署名検証
- CSRF保護

## 📝 ログ

```bash
# Djangoログ
docker compose logs -f django

# n8nログ
docker compose logs -f n8n

# PostgreSQLログ
docker compose logs -f postgres
```

## 🐛 トラブルシューティング

### よくある問題

1. **ポートが使用中**
   ```bash
   # 使用中のポートを確認
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :5678
   ```

2. **データベース接続エラー**
   ```bash
   # PostgreSQLコンテナの状態確認
   docker compose ps postgres
   ```

3. **LINE Bot接続エラー**
   - チャンネルアクセストークンの確認
   - Webhook URLの設定確認

### ログの確認

```bash
# 全ログを確認
docker compose logs

# 特定のサービスのログ
docker compose logs django
docker compose logs n8n
```

## 🤝 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 📞 サポート

問題や質問がある場合は、[Issues](../../issues) を作成してください。

## 🔄 更新履歴

- **v1.0.0**: 初期リリース
  - LINE Bot連携
  - n8n統合
  - Django管理画面
  - PostgreSQLデータベース

---

**注意**: 本番環境で使用する前に、必ずセキュリティ設定を確認してください。 