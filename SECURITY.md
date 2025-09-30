# 🔒 セキュリティガイドライン

## ⚠️ 重要な注意事項

このプロジェクトをGitHubに公開する前に、以下のセキュリティ対策を必ず実施してください。

## 🚨 必須セキュリティ対策

### 1. APIキーの保護

#### ❌ 絶対にコミットしてはいけないファイル
- `.env` - 実際のAPIキーを含む環境変数ファイル
- `config.ini` - 機密設定ファイル
- `secrets.json` - 秘密情報ファイル
- `*.key` - 秘密鍵ファイル
- `*.pem` - 証明書ファイル

#### ✅ 正しい設定方法
```bash
# 1. .envファイルを作成（Gitにコミットしない）
cp env.example .env

# 2. .envファイルに実際のAPIキーを設定
# 例：
OPENAI_API_KEY=sk-actual-openai-key-here
GOOGLE_MAPS_API_KEY=actual-google-maps-key-here
```

### 2. 環境変数の設定

#### 本番環境での設定例
```bash
# 本番環境では強力なパスワードを使用
DATABASE_URL=postgresql://user:strong_password@localhost:5432/hotel_db
SECRET_KEY=very-long-random-secret-key-here
```

#### 開発環境での設定例
```bash
# 開発環境では簡単なパスワードでも可
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/hotel_dev
SECRET_KEY=dev-secret-key
```

### 3. データベースセキュリティ

#### PostgreSQL設定
```sql
-- 強力なパスワードを設定
ALTER USER hotel_user PASSWORD 'strong_password_here';

-- 不要な権限を削除
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO hotel_user;
GRANT CREATE ON SCHEMA public TO hotel_user;
```

## 🔐 GitHub公開前のチェックリスト

### ✅ 必須確認項目

- [ ] `.env`ファイルが`.gitignore`に含まれている
- [ ] `env.example`ファイルが作成されている
- [ ] 実際のAPIキーがコードにハードコーディングされていない
- [ ] データベースパスワードがコードに含まれていない
- [ ] 秘密鍵ファイルが除外されている
- [ ] ログファイルに機密情報が含まれていない

### 🔍 コード内の機密情報チェック

以下の文字列がコード内に含まれていないか確認してください：

```bash
# 以下のコマンドで機密情報を検索
grep -r "sk-" . --exclude-dir=.git
grep -r "AIza" . --exclude-dir=.git
grep -r "password" . --exclude-dir=.git
grep -r "secret" . --exclude-dir=.git
```

## 🛡️ 本番環境でのセキュリティ

### 1. HTTPS通信の強制
```python
# FastAPI設定例
app = FastAPI(
    title="Hotel Response Agent",
    ssl_redirect=True,  # HTTPSリダイレクト
    ssl_context=ssl_context
)
```

### 2. CORS設定
```python
# 適切なCORS設定
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 本番ドメインのみ
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. レート制限
```python
# レート制限の実装
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/messages")
@limiter.limit("10/minute")  # 1分間に10リクエストまで
async def create_message(request: Request, ...):
    pass
```

## 🔑 APIキーの取得方法

### 1. OpenAI APIキー
1. [OpenAI Platform](https://platform.openai.com/)にアクセス
2. アカウントを作成・ログイン
3. API Keysセクションで新しいキーを生成
4. 生成されたキーを`.env`ファイルに設定

### 2. Google Maps APIキー
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを作成
3. Maps JavaScript APIを有効化
4. 認証情報でAPIキーを作成
5. 使用制限を設定（推奨）

### 3. Booking.com API
1. [Booking.com Partner Hub](https://partner.booking.com/)にアクセス
2. パートナーアカウントを作成
3. APIアクセスを申請
4. 承認後にAPIキーを取得

## 📋 環境変数の完全リスト

### 必須環境変数
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/hotel_db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Application Settings
SECRET_KEY=your-secret-key-here
DEBUG=False  # 本番環境ではFalse
```

### オプション環境変数
```bash
# Booking.com API
BOOKING_API_KEY=your-booking-api-key-here
BOOKING_API_URL=https://distribution-xml.booking.com/2.5/json

# Airbnb API
AIRBNB_API_KEY=your-airbnb-api-key-here
AIRBNB_API_URL=https://api.airbnb.com/v2

# ログ設定
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 🚨 緊急時の対応

### APIキーが漏洩した場合
1. 即座に該当APIキーを無効化
2. 新しいAPIキーを生成
3. `.env`ファイルを更新
4. システムを再起動

### データベースが侵害された場合
1. データベース接続を切断
2. パスワードを変更
3. ログを確認して侵入経路を特定
4. 必要に応じてデータベースを再構築

## 📞 サポート

セキュリティに関する質問や問題が発生した場合は、以下の方法でサポートを受けてください：

1. GitHubのIssuesで報告
2. セキュリティ関連の場合はPrivate Issueを作成
3. 緊急の場合は直接連絡

## 📚 参考資料

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)
