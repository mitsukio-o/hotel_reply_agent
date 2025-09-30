# Streamlit Cloud用の設定ファイル

## 📋 デプロイ前の準備

### 1. GitHubリポジトリの準備
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

### 2. 必要なファイルの確認
- ✅ `streamlit_app_fixed.py` - メインアプリ
- ✅ `requirements.txt` - 依存関係
- ✅ `.gitignore` - Git除外設定
- ✅ `README.md` - プロジェクト説明

### 3. requirements.txtの作成
```txt
streamlit>=1.25.0
requests>=2.30.0
```

### 4. .gitignoreの設定
```gitignore
# 環境変数ファイル
.env

# データベースファイル
hotel_agent.db

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# IDE
.vscode/
.idea/

# ログファイル
*.log
*.tmp
*.temp

# macOS
.DS_Store

# Windows
Thumbs.db
```

## 🚀 Streamlit Cloudデプロイ手順

### ステップ1: Streamlit Cloudにアクセス
1. [Streamlit Cloud](https://share.streamlit.io/)にアクセス
2. GitHubアカウントでログイン

### ステップ2: 新しいアプリを作成
1. "New app"ボタンをクリック
2. GitHubリポジトリを選択
3. ブランチを選択（main）
4. メインファイルを指定：`streamlit_app_fixed.py`

### ステップ3: 環境変数の設定（オプション）
```bash
# Streamlit Cloudの設定で環境変数を追加
OPENAI_API_KEY=your-openai-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### ステップ4: デプロイ実行
1. "Deploy!"ボタンをクリック
2. デプロイが完了するまで待機
3. 提供されたURLでアクセス

## 🔧 デプロイ後の設定

### 1. カスタムドメインの設定（オプション）
- Streamlit Cloudの設定でカスタムドメインを追加
- DNS設定でドメインを設定

### 2. 環境変数の管理
- 機密情報は環境変数で管理
- Streamlit Cloudの設定で環境変数を追加

### 3. 自動デプロイの設定
- GitHubにプッシュすると自動でデプロイ
- ブランチごとにデプロイ環境を分けることも可能

## 📊 メリット・デメリット

### メリット
- ✅ 無料で利用可能
- ✅ 自動デプロイ
- ✅ カスタムドメイン対応
- ✅ 簡単設定
- ✅ GitHub連携

### デメリット
- ❌ 実行時間制限
- ❌ メモリ制限
- ❌ 外部API制限
- ❌ データベース永続化の制限

## 🛠️ トラブルシューティング

### よくある問題

#### 1. デプロイエラー
```
Error: Failed to deploy
```
**解決方法:**
- requirements.txtの依存関係を確認
- メインファイル名が正しいか確認
- GitHubリポジトリが公開されているか確認

#### 2. アプリが起動しない
```
Error: App failed to start
```
**解決方法:**
- ログを確認してエラーを特定
- 依存関係のバージョンを確認
- 環境変数の設定を確認

#### 3. データベースエラー
```
Error: Database not found
```
**解決方法:**
- スタンドアロンモードで動作するか確認
- データベース初期化機能を使用

## 📝 注意事項

- 本番環境では適切なセキュリティ設定を行ってください
- APIキーは環境変数で管理してください
- データベースは永続化されないため、重要なデータは外部ストレージを使用してください
- 実行時間制限があるため、長時間の処理は避けてください

## 🎯 推奨設定

### 本番環境
- 環境変数でAPIキーを管理
- カスタムドメインを使用
- 適切なREADME.mdを作成

### 開発環境
- ローカルでテストしてからデプロイ
- ブランチごとにデプロイ環境を分ける
- ログを定期的に確認
