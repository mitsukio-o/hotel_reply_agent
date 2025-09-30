# Docker用の設定ファイル

## 📋 Dockerfile

```dockerfile
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージを更新
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# ポートを公開
EXPOSE 8501

# ヘルスチェック
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# アプリケーションを起動
CMD ["streamlit", "run", "streamlit_app_fixed.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## 📋 requirements.txt

```txt
streamlit>=1.25.0
requests>=2.30.0
```

## 📋 docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./hotel_agent.db:/app/hotel_agent.db
      - ./logs:/app/logs
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}
      - API_BASE_URL=http://localhost:8000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # オプション: FastAPIサーバーも含める場合
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./hotel_agent.db:/app/hotel_agent.db
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}
    command: ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    restart: unless-stopped
    depends_on:
      - app
```

## 📋 .dockerignore

```dockerignore
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.env.local
.env.production

# Documentation
*.md
docs/

# Test files
test_*.py
*_test.py
tests/

# Temporary files
*.tmp
*.temp
```

## 🚀 Dockerデプロイ手順

### ステップ1: Dockerのインストール
```bash
# Dockerをインストール
# https://docs.docker.com/get-docker/

# Docker Composeをインストール
# https://docs.docker.com/compose/install/
```

### ステップ2: 環境変数の設定
```bash
# .envファイルを作成
cp env.example .env

# .envファイルを編集
nano .env
```

### ステップ3: Dockerイメージのビルド
```bash
# Dockerイメージをビルド
docker build -t hotel-reply-agent .

# イメージが作成されたか確認
docker images
```

### ステップ4: コンテナの実行
```bash
# 単一コンテナで実行
docker run -p 8501:8501 hotel-reply-agent

# Docker Composeで実行
docker-compose up -d

# ログを確認
docker-compose logs -f
```

### ステップ5: アクセス
- **アプリURL**: http://localhost:8501
- **API URL**: http://localhost:8000（APIサーバーも含める場合）

## 🔧 Docker管理コマンド

### 基本的なコマンド
```bash
# コンテナの状態確認
docker ps

# ログの確認
docker logs <container_id>

# コンテナの停止
docker stop <container_id>

# コンテナの削除
docker rm <container_id>

# イメージの削除
docker rmi hotel-reply-agent
```

### Docker Composeコマンド
```bash
# サービスの起動
docker-compose up -d

# サービスの停止
docker-compose down

# サービスの再起動
docker-compose restart

# ログの確認
docker-compose logs -f

# サービスの状態確認
docker-compose ps
```

## 🛠️ トラブルシューティング

### よくある問題

#### 1. ビルドエラー
```
Error: Failed to build
```
**解決方法:**
- Dockerfileの構文を確認
- 依存関係のバージョンを確認
- ネットワーク接続を確認

#### 2. コンテナが起動しない
```
Error: Container failed to start
```
**解決方法:**
- ログを確認してエラーを特定
- ポートの競合を確認
- 環境変数の設定を確認

#### 3. データベースエラー
```
Error: Database not found
```
**解決方法:**
- ボリュームマウントを確認
- データベースファイルの権限を確認
- 初期化スクリプトを実行

## 📊 メリット・デメリット

### メリット
- ✅ 環境の一貫性
- ✅ スケーラビリティ
- ✅ 移植性
- ✅ 依存関係の管理
- ✅ 本番環境との一致

### デメリット
- ❌ 学習コスト
- ❌ リソース使用量
- ❌ デバッグの複雑さ
- ❌ 設定の複雑さ

## 📝 注意事項

- 本番環境では適切なセキュリティ設定を行ってください
- データベースファイルはボリュームで永続化してください
- ログファイルは適切に管理してください
- リソース制限を設定してください

## 🎯 推奨設定

### 本番環境
- リソース制限を設定
- ヘルスチェックを有効化
- ログローテーションを設定
- セキュリティスキャンを実行

### 開発環境
- ホットリロードを有効化
- デバッグログを有効化
- 開発用の環境変数を設定
- ローカルファイルをマウント
