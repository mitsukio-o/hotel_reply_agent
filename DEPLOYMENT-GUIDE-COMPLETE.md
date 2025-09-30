# 🚀 完全デプロイガイド

## 📋 デプロイ方法一覧

1. **ローカルデプロイ** - 自分のPCで動作
2. **Streamlit Cloud** - 無料クラウドデプロイ
3. **Heroku** - 人気のクラウドプラットフォーム
4. **Docker** - コンテナ化デプロイ
5. **GitHub Pages** - 静的サイトデプロイ
6. **VPS/サーバー** - 専用サーバーでのデプロイ

---

## 🏠 1. ローカルデプロイ（推奨）

### 前提条件
- Python 3.8以上
- pip（Pythonパッケージマネージャー）

### 手順

#### ステップ1: ファイルの準備
```bash
# プロジェクトディレクトリに移動
cd pushtest

# 必要なファイルを確認
ls -la streamlit_app_fixed.py
```

#### ステップ2: 依存関係のインストール
```bash
# 仮想環境を作成（推奨）
python -m venv venv

# 仮想環境をアクティベート
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 依存関係をインストール
pip install streamlit requests
```

#### ステップ3: アプリの起動
```bash
# 修正されたアプリを起動
streamlit run streamlit_app_fixed.py --server.port 8501 --server.address 0.0.0.0
```

#### ステップ4: アクセス
- **ローカル**: http://localhost:8501
- **ネットワーク**: http://[あなたのIP]:8501

### 自動起動スクリプト
```bash
# Windows用バッチファイル
deploy-local.bat

# Linux/Mac用シェルスクリプト
chmod +x deploy-local.sh
./deploy-local.sh
```

---

## ☁️ 2. Streamlit Cloud（無料・推奨）

### 前提条件
- GitHubアカウント
- GitHubリポジトリ

### 手順

#### ステップ1: GitHubにプッシュ
```bash
# Gitリポジトリを初期化
git init

# ファイルを追加
git add .

# コミット
git commit -m "Initial commit"

# GitHubリポジトリを作成してプッシュ
git remote add origin https://github.com/yourusername/hotel-reply-agent.git
git push -u origin main
```

#### ステップ2: Streamlit Cloudでデプロイ
1. [Streamlit Cloud](https://share.streamlit.io/)にアクセス
2. "New app"をクリック
3. GitHubリポジトリを選択
4. ブランチを選択（main）
5. メインファイルを指定：`streamlit_app_fixed.py`
6. "Deploy!"をクリック

#### ステップ3: 環境変数の設定（オプション）
```bash
# Streamlit Cloudの設定で環境変数を追加
OPENAI_API_KEY=your-openai-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### メリット
- ✅ 無料
- ✅ 自動デプロイ
- ✅ カスタムドメイン対応
- ✅ 簡単設定

---

## 🐳 3. Dockerデプロイ

### 前提条件
- Docker
- Docker Compose

### 手順

#### ステップ1: Dockerfileの作成
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app_fixed.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

#### ステップ2: requirements.txtの作成
```txt
streamlit>=1.25.0
requests>=2.30.0
```

#### ステップ3: Dockerイメージのビルド
```bash
# Dockerイメージをビルド
docker build -t hotel-reply-agent .

# コンテナを実行
docker run -p 8501:8501 hotel-reply-agent
```

#### ステップ4: Docker Composeで実行
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./hotel_agent.db:/app/hotel_agent.db
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}
```

```bash
# Docker Composeで起動
docker-compose up -d
```

---

## 🌐 4. Herokuデプロイ

### 前提条件
- Herokuアカウント
- Heroku CLI

### 手順

#### ステップ1: Heroku CLIのインストール
```bash
# Heroku CLIをインストール
# https://devcenter.heroku.com/articles/heroku-cli
```

#### ステップ2: プロジェクトの準備
```bash
# Procfileを作成
echo "web: streamlit run streamlit_app_fixed.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# requirements.txtを作成
echo "streamlit>=1.25.0
requests>=2.30.0" > requirements.txt

# runtime.txtを作成
echo "python-3.9.16" > runtime.txt
```

#### ステップ3: Herokuにデプロイ
```bash
# Herokuアプリを作成
heroku create your-app-name

# 環境変数を設定
heroku config:set OPENAI_API_KEY=your-openai-api-key
heroku config:set GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# デプロイ
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

## 📱 5. GitHub Pages（静的サイト）

### 前提条件
- GitHubアカウント
- GitHub Actions

### 手順

#### ステップ1: GitHub Actionsの設定
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install streamlit requests
        
    - name: Deploy
      run: |
        streamlit run streamlit_app_fixed.py --server.port 8501
```

#### ステップ2: デプロイ
```bash
# GitHubにプッシュ
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

---

## 🖥️ 6. VPS/サーバーデプロイ

### 前提条件
- VPS/サーバー
- SSHアクセス

### 手順

#### ステップ1: サーバーに接続
```bash
# SSHでサーバーに接続
ssh user@your-server-ip
```

#### ステップ2: 環境の準備
```bash
# Pythonをインストール
sudo apt update
sudo apt install python3 python3-pip

# プロジェクトディレクトリを作成
mkdir -p /var/www/hotel-reply-agent
cd /var/www/hotel-reply-agent
```

#### ステップ3: アプリの配置
```bash
# ファイルをアップロード
scp -r pushtest/* user@your-server-ip:/var/www/hotel-reply-agent/

# 依存関係をインストール
pip3 install streamlit requests
```

#### ステップ4: サービスとして実行
```bash
# systemdサービスファイルを作成
sudo nano /etc/systemd/system/hotel-reply-agent.service
```

```ini
[Unit]
Description=Hotel Reply Agent
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/hotel-reply-agent
ExecStart=/usr/bin/python3 -m streamlit run streamlit_app_fixed.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# サービスを有効化
sudo systemctl enable hotel-reply-agent
sudo systemctl start hotel-reply-agent
```

---

## 🔧 デプロイ前の準備

### 1. 環境変数の設定
```bash
# .envファイルを作成
cp env.example .env

# .envファイルを編集
nano .env
```

### 2. セキュリティ設定
```bash
# .gitignoreに機密情報を追加
echo ".env" >> .gitignore
echo "hotel_agent.db" >> .gitignore
echo "*.log" >> .gitignore
```

### 3. テスト実行
```bash
# ローカルでテスト
python test-integrated-app.py

# アプリを起動してテスト
streamlit run streamlit_app_fixed.py
```

---

## 📊 デプロイ方法の比較

| 方法 | 難易度 | コスト | スケーラビリティ | 推奨度 |
|------|--------|--------|------------------|--------|
| ローカル | ⭐ | 無料 | ⭐ | ⭐⭐⭐⭐⭐ |
| Streamlit Cloud | ⭐⭐ | 無料 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Docker | ⭐⭐⭐ | 無料〜 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Heroku | ⭐⭐ | 有料 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| GitHub Pages | ⭐⭐⭐ | 無料 | ⭐⭐ | ⭐⭐ |
| VPS/サーバー | ⭐⭐⭐⭐ | 有料 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🚨 トラブルシューティング

### よくある問題

#### 1. ポート競合
```bash
# ポート8501が使用中の場合
streamlit run streamlit_app_fixed.py --server.port 8502
```

#### 2. 依存関係エラー
```bash
# 仮想環境を再作成
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install streamlit requests
```

#### 3. 権限エラー
```bash
# ファイルの権限を確認
chmod +x streamlit_app_fixed.py
```

#### 4. データベースエラー
```bash
# データベースファイルを削除して再作成
rm hotel_agent.db
# アプリを起動して初期化
```

---

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. **ログファイル**: エラーメッセージを確認
2. **環境変数**: 設定が正しいか確認
3. **依存関係**: 必要なパッケージがインストールされているか確認
4. **ネットワーク**: ポートが開いているか確認

---

## 🎯 推奨デプロイ手順

### 初心者向け
1. **ローカルデプロイ**で動作確認
2. **Streamlit Cloud**で無料デプロイ

### 中級者向け
1. **Docker**でコンテナ化
2. **Heroku**でクラウドデプロイ

### 上級者向け
1. **VPS/サーバー**で本格運用
2. **CI/CD**パイプラインの構築

---

## 📝 注意事項

- 本番環境では適切なセキュリティ設定を行ってください
- APIキーは環境変数で管理してください
- データベースファイルは定期的にバックアップしてください
- ログファイルは適切に管理してください
