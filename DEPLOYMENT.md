# Hetznerへのデプロイ手順

## 前提条件

1. **Hetzner Cloud Server**がセットアップ済み
2. **ドメイン名**が設定済み
3. **Docker**と**Docker Compose**がインストール済み

## 1. サーバーへの接続

```bash
ssh root@your-server-ip
```

## 2. 必要なソフトウェアのインストール

```bash
# システムの更新
apt update && apt upgrade -y

# Dockerのインストール
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Docker Composeのインストール
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Gitのインストール
apt install git -y
```

## 3. プロジェクトのクローン

```bash
# プロジェクトディレクトリの作成
mkdir -p /opt/n8n-linebot
cd /opt/n8n-linebot

# Gitリポジトリからクローン（またはファイルをアップロード）
git clone https://github.com/your-username/your-repo.git .
```

## 4. 環境変数の設定

```bash
# 環境変数ファイルの作成
cp env.prod.example .env

# 環境変数を編集
nano .env
```

以下の項目を設定してください：

```bash
# Django設定
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# データベース設定
DB_ENGINE=django.db.backends.postgresql
DB_NAME=linebot_db
DB_USER=linebot_user
DB_PASSWORD=your-secure-password-here
DB_HOST=postgres
DB_PORT=5432

# LINE Bot設定
LINE_CHANNEL_ACCESS_TOKEN=your-line-channel-access-token
LINE_CHANNEL_SECRET=your-line-channel-secret

# n8n設定
N8N_WEBHOOK_URL=http://your-domain.com/webhook/n8n
N8N_USER=admin
N8N_PASSWORD=your-secure-n8n-password

# ドメイン設定
DOMAIN=your-domain.com
```

## 5. デプロイの実行

```bash
# デプロイスクリプトに実行権限を付与
chmod +x deploy.sh

# デプロイを実行
./deploy.sh
```

## 6. ファイアウォールの設定

```bash
# UFWのインストール
apt install ufw -y

# ファイアウォールの設定
ufw allow ssh
ufw allow 80
ufw allow 443
ufw enable
```

## 7. SSL証明書の設定（オプション）

Let's Encryptを使用してSSL証明書を取得：

```bash
# Certbotのインストール
apt install certbot -y

# SSL証明書の取得
certbot certonly --standalone -d your-domain.com

# Nginx設定でSSLを有効化
# nginx.confのコメントアウトされたSSL設定を有効化
```

## 8. サービスの確認

```bash
# コンテナの状態確認
docker compose -f docker-compose.prod.yml ps

# ログの確認
docker compose -f docker-compose.prod.yml logs -f
```

## 9. アクセスURL

デプロイ完了後、以下のURLでアクセスできます：

- **n8n**: `http://your-domain.com`
- **Django Admin**: `http://your-domain.com/admin/`
- **LINE Bot Webhook**: `http://your-domain.com/linebot/webhook/`

## 10. メンテナンス

### ログの確認
```bash
docker compose -f docker-compose.prod.yml logs -f django
docker compose -f docker-compose.prod.yml logs -f n8n
```

### バックアップ
```bash
# データベースのバックアップ
docker compose -f docker-compose.prod.yml exec postgres pg_dump -U linebot_user linebot_db > backup.sql
```

### 更新
```bash
# コードの更新
git pull

# コンテナの再起動
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

## トラブルシューティング

### ポートが使用中の場合
```bash
# 使用中のポートを確認
netstat -tulpn | grep :80
netstat -tulpn | grep :443

# プロセスを停止
kill -9 <PID>
```

### ディスク容量不足
```bash
# 不要なDockerイメージを削除
docker system prune -a

# ログファイルの確認
du -sh /var/log/*
```

### メモリ不足
```bash
# スワップファイルの作成
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
``` 