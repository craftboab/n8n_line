FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージを更新
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 静的ファイル用のディレクトリを作成
RUN mkdir -p /app/static

# ポート8000を公開
EXPOSE 8000

# 起動コマンド（本番環境用）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 