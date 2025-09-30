# 🏨 ホテル向け自動返信システム - システム構成

## 📋 概要

このシステムは、ホテルがゲストからのメッセージに対して自動的に適切な返信を生成し、送信するためのAI搭載システムです。複数のプラットフォーム（Booking.com、Airbnb等）からのメッセージを統合管理し、過去のデータから学習して最適な返信を提供します。

## 🏗️ システムアーキテクチャ

### 全体構成図

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   FastAPI       │    │   PostgreSQL    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (Cache)       │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  External APIs  │
                       │ (Google Maps,   │
                       │  Booking.com,   │
                       │  Airbnb)        │
                       └─────────────────┘
```

## 🧩 コンポーネント詳細

### 1. フロントエンド (Streamlit UI)

**ファイル**: `streamlit_app.py`

**役割**:
- ホテル管理者向けのWebインターフェース
- メッセージの表示・管理
- 返信候補の生成・選択
- 分析データの可視化

**主要機能**:
- ホテル選択
- メッセージ一覧表示
- 返信候補生成（3つの選択肢）
- 根拠ソース表示
- 分析データ表示
- 周辺観光地情報表示

### 2. バックエンド (FastAPI)

**ファイル**: `app/main.py`

**役割**:
- RESTful APIの提供
- ビジネスロジックの実装
- データベースとの連携
- 外部APIとの連携

**主要エンドポイント**:
```
GET  /hotels                    # ホテル一覧取得
POST /hotels                    # ホテル作成
GET  /messages/{hotel_id}       # メッセージ一覧取得
POST /messages                  # メッセージ作成
POST /messages/{id}/suggestions # 返信候補生成
POST /messages/{id}/respond     # 返信送信
GET  /hotels/{id}/analytics    # 分析データ取得
GET  /hotels/{id}/nearby-attractions # 周辺観光地取得
```

### 3. データベース (PostgreSQL)

**ファイル**: `app/models.py`

**テーブル構成**:
- `hotels`: ホテル基本情報
- `bookings`: 予約データ
- `guest_messages`: ゲストメッセージ
- `response_templates`: 返信テンプレート
- `response_logs`: 返信ログ
- `nearby_attractions`: 周辺観光地情報

### 4. AIエージェントシステム

#### 4.1 ホテル周辺情報検索エージェント

**ファイル**: `app/agents/hotel_info_agent.py`

**役割**:
- Google Maps APIを使用した周辺施設検索
- 荷物預かり情報の提供
- 観光地情報の取得
- モックデータの提供（APIキーなしでも動作）

**主要メソッド**:
- `get_nearby_attractions()`: 周辺観光地取得
- `get_luggage_storage_info()`: 荷物預かり情報取得
- `get_booking_availability()`: 予約可能期間取得

#### 4.2 予約データ学習エージェント

**ファイル**: `app/agents/booking_data_agent.py`

**役割**:
- 過去のメッセージ・返信ログから学習
- TF-IDFベクトル化による類似メッセージ検索
- 予約パターン分析
- 返信テンプレートの最適化

**主要メソッド**:
- `analyze_booking_patterns()`: 予約パターン分析
- `learn_from_historical_data()`: 過去データから学習
- `generate_response_suggestions()`: 返信候補生成

### 5. サービス層

#### 5.1 返信生成サービス

**ファイル**: `app/services/response_generator.py`

**役割**:
- メッセージタイプ別の返信候補生成
- 複数のエージェントの結果を統合
- 信頼度による候補のランキング

#### 5.2 API連携サービス

**ファイル**: `app/services/api_service.py`

**役割**:
- 外部プラットフォームAPIとの連携
- メッセージの取得・送信
- プラットフォーム別の処理

## 🔄 データフロー

### 1. メッセージ受信フロー

```
外部プラットフォーム → API連携サービス → データベース → フロントエンド表示
```

### 2. 返信生成フロー

```
メッセージ受信 → メッセージタイプ分類 → エージェント呼び出し → 返信候補生成 → 信頼度ランキング → 3つの候補選択
```

### 3. 学習フロー

```
過去のメッセージ・返信 → TF-IDFベクトル化 → パターン学習 → テンプレート最適化
```

## 🛠️ 技術スタック

### バックエンド
- **FastAPI**: 高性能なWebフレームワーク
- **SQLAlchemy**: ORM（Object-Relational Mapping）
- **PostgreSQL**: リレーショナルデータベース
- **Redis**: キャッシュ・セッション管理
- **Pandas**: データ分析
- **scikit-learn**: 機械学習（TF-IDF）

### フロントエンド
- **Streamlit**: データサイエンス向けWebアプリフレームワーク

### インフラ
- **Docker**: コンテナ化
- **Docker Compose**: マルチコンテナ管理

### 外部API
- **Google Maps API**: 周辺施設検索
- **OpenAI API**: AI返信生成（将来実装予定）
- **Booking.com API**: 予約データ取得
- **Airbnb API**: 予約データ取得

## 📁 ディレクトリ構造

```
hotelcursor2/
├── app/                    # アプリケーション本体
│   ├── __init__.py
│   ├── config.py          # 設定管理
│   ├── database.py        # データベース接続
│   ├── main.py            # FastAPIアプリケーション
│   ├── models.py          # データベースモデル
│   ├── seed_data.py       # 初期データ
│   ├── agents/            # AIエージェント
│   │   ├── hotel_info_agent.py
│   │   └── booking_data_agent.py
│   └── services/          # ビジネスロジック
│       ├── api_service.py
│       └── response_generator.py
├── streamlit_app.py       # フロントエンド
├── docker-compose.yml     # Docker設定
├── Dockerfile            # Dockerイメージ定義
├── requirements.txt      # Python依存関係
├── .gitignore           # Git除外設定
├── env.example          # 環境変数例
└── README.md           # プロジェクト説明
```

## 🔧 設定管理

### 環境変数

システムは以下の環境変数を使用します：

- `OPENAI_API_KEY`: OpenAI APIキー
- `GOOGLE_MAPS_API_KEY`: Google Maps APIキー
- `DATABASE_URL`: PostgreSQL接続URL
- `REDIS_URL`: Redis接続URL
- `BOOKING_API_KEY`: Booking.com APIキー
- `AIRBNB_API_KEY`: Airbnb APIキー

### 設定ファイル

- `app/config.py`: 設定クラスの定義
- `env.example`: 環境変数の例
- `.env`: 実際の環境変数（Git除外）

## 🚀 デプロイメント

### Docker Compose構成

```yaml
services:
  api:          # FastAPIバックエンド
  postgres:     # PostgreSQLデータベース
  redis:        # Redisキャッシュ
  streamlit:    # Streamlitフロントエンド
```

### 起動コマンド

```bash
# システム起動
docker-compose up -d

# ログ確認
docker-compose logs -f

# システム停止
docker-compose down
```

## 🔒 セキュリティ考慮事項

### 1. APIキー管理
- 環境変数による管理
- `.gitignore`による除外
- 本番環境での暗号化

### 2. データベースセキュリティ
- 接続文字列の暗号化
- アクセス権限の制限
- 定期的なバックアップ

### 3. ネットワークセキュリティ
- HTTPS通信の強制
- CORS設定
- レート制限の実装

## 📊 パフォーマンス最適化

### 1. キャッシュ戦略
- Redisによるレスポンスキャッシュ
- データベースクエリの最適化

### 2. 非同期処理
- FastAPIの非同期機能活用
- バックグラウンドタスクの実装

### 3. データベース最適化
- インデックスの適切な設定
- クエリの最適化

## 🔮 将来の拡張予定

### 1. AI機能の強化
- OpenAI GPT統合
- 感情分析機能
- 多言語対応

### 2. プラットフォーム拡張
- 新しい予約プラットフォーム対応
- チャットボット統合

### 3. 分析機能の強化
- リアルタイムダッシュボード
- 予測分析機能
- レポート生成

## 🐛 トラブルシューティング

### よくある問題

1. **APIキーエラー**
   - 環境変数の設定確認
   - APIキーの有効性確認

2. **データベース接続エラー**
   - PostgreSQLサービスの起動確認
   - 接続文字列の確認

3. **メモリ不足**
   - Dockerのメモリ制限調整
   - 不要なコンテナの停止

### ログ確認方法

```bash
# 全サービスのログ
docker-compose logs

# 特定サービスのログ
docker-compose logs api
docker-compose logs postgres
```

## 📚 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [Docker公式ドキュメント](https://docs.docker.com/)
- [Google Maps API](https://developers.google.com/maps/documentation)
