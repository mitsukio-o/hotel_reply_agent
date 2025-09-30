# 🚀 GitHub公開手順書

## 📋 公開前のチェックリスト

### ✅ 必須確認項目

- [ ] `.env`ファイルが`.gitignore`に含まれている
- [ ] `env.example`ファイルが作成されている
- [ ] 実際のAPIキーがコードにハードコーディングされていない
- [ ] データベースパスワードがコードに含まれていない
- [ ] 秘密鍵ファイルが除外されている
- [ ] ログファイルに機密情報が含まれていない

### 🔍 機密情報の検索

以下のコマンドで機密情報がコード内に含まれていないか確認してください：

```bash
# APIキーの検索
grep -r "sk-" . --exclude-dir=.git
grep -r "AIza" . --exclude-dir=.git
grep -r "password" . --exclude-dir=.git
grep -r "secret" . --exclude-dir=.git

# 環境変数ファイルの確認
ls -la | grep "\.env"
```

## 🛠️ GitHub公開手順

### 1. Gitリポジトリの初期化

```bash
# プロジェクトディレクトリに移動
cd hotelcursor2

# Gitリポジトリを初期化
git init

# リモートリポジトリを追加（GitHubで作成したリポジトリのURL）
git remote add origin https://github.com/yourusername/hotel-response-system.git
```

### 2. ファイルの追加とコミット

```bash
# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: Hotel Response System

- AI搭載マルチエージェントシステム
- Streamlit Web UI
- FastAPI バックエンド
- PostgreSQL データベース
- Docker Compose設定
- セキュリティ対策実装"
```

### 3. GitHubにプッシュ

```bash
# メインブランチを設定
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

## 🔐 セキュリティ設定

### 1. GitHub Secretsの設定

GitHubリポジトリで以下のSecretsを設定してください：

1. **Settings** → **Secrets and variables** → **Actions**
2. 以下のSecretsを追加：

```
OPENAI_API_KEY=your-actual-openai-key
GOOGLE_MAPS_API_KEY=your-actual-google-maps-key
DATABASE_URL=postgresql://user:password@localhost:5432/hotel_db
SECRET_KEY=your-secret-key
```

### 2. Branch Protection Rules

1. **Settings** → **Branches**
2. **Add rule**をクリック
3. **main**ブランチを保護
4. 以下の設定を有効化：
   - Require a pull request before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging

## 📝 リポジトリ設定

### 1. リポジトリの説明

GitHubリポジトリの**About**セクションに以下を設定：

- **Description**: `AI-powered hotel response system with multi-agent architecture`
- **Website**: `http://localhost:8501`（開発環境）
- **Topics**: `hotel`, `ai`, `fastapi`, `streamlit`, `docker`, `automation`

### 2. README.mdの更新

リポジトリURLを実際のものに更新：

```bash
# README.md内のURLを更新
sed -i 's/yourusername/実際のユーザー名/g' README.md
sed -i 's/hotel-response-system/実際のリポジトリ名/g' README.md
```

## 🚀 CI/CD設定（オプション）

### GitHub Actions設定

`.github/workflows/ci.yml`ファイルを作成：

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Build Docker images
      run: |
        docker-compose build
    
    - name: Run system tests
      run: |
        docker-compose up -d
        sleep 30
        python test_data.py
        docker-compose down
```

## 📊 リリース管理

### 1. 初回リリース

```bash
# タグを作成
git tag -a v1.0.0 -m "Initial release: Hotel Response System v1.0.0"

# タグをプッシュ
git push origin v1.0.0
```

### 2. GitHub Releases

1. **Releases** → **Create a new release**
2. **Tag version**: `v1.0.0`
3. **Release title**: `Hotel Response System v1.0.0`
4. **Description**: リリースノートを記述
5. **Publish release**をクリック

## 🔍 公開後の確認

### 1. リポジトリの確認

- [ ] README.mdが正しく表示される
- [ ] すべてのファイルがアップロードされている
- [ ] `.env`ファイルが除外されている
- [ ] セキュリティ設定が適用されている

### 2. 動作確認

```bash
# 新しい環境でクローン
git clone https://github.com/yourusername/hotel-response-system.git
cd hotel-response-system

# 環境変数を設定
cp env.example .env
# .envファイルを編集

# システム起動
docker-compose up -d

# 動作確認
curl http://localhost:8000/docs
```

## 📈 プロモーション

### 1. ソーシャルメディア

- Twitterでプロジェクトを紹介
- LinkedInで技術記事を投稿
- 技術ブログで詳細解説

### 2. コミュニティ

- Redditのr/MachineLearningで紹介
- GitHubのExploreで発見されやすくする
- 関連するOSSプロジェクトに貢献

## 🛡️ 継続的なセキュリティ

### 1. 定期的な確認

- 月1回の依存関係更新
- セキュリティ脆弱性のチェック
- APIキーの定期ローテーション

### 2. 監視設定

- GitHub Dependabotの有効化
- セキュリティアラートの設定
- コードスキャンの有効化

## 📞 サポート

公開後のサポート体制：

1. **GitHub Issues**: バグ報告・機能要望
2. **Discussions**: 質問・議論
3. **Wiki**: 詳細ドキュメント
4. **Discord/Slack**: リアルタイムサポート

---

**🎉 おめでとうございます！プロジェクトがGitHubに公開されました！**
