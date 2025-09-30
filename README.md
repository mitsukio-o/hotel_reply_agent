# 🏨 ホテル向け自動返信システム

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Booking.comやAirbnbなどのプラットフォームからのゲストメッセージに対して、AIを活用した自動返信候補を生成し、ワンクリックで返信できるシステムです。

## ✨ 主要機能

### 🤖 AI搭載マルチエージェントシステム
- **ホテル周辺情報検索エージェント**: Google Maps APIを使用した周辺施設検索
- **予約データ学習エージェント**: 過去のデータから学習して返信品質を向上
- **返信候補生成**: メッセージ内容に基づいて3つの返信候補を自動生成
- **根拠ソース表示**: 各返信候補の根拠となるソースを明示

### 📱 ユーザーフレンドリーなUI
- **Streamlit Web UI**: 直感的なWebインターフェース
- **ワンクリック返信**: 選択した候補で即座にプラットフォームに返信
- **リアルタイム更新**: 新しいメッセージを自動取得・表示
- **分析ダッシュボード**: 予約パターンや学習結果を可視化

### 🔗 マルチプラットフォーム対応
- **Booking.com**: 予約データとメッセージの取得・送信
- **Airbnb**: 予約データとメッセージの取得・送信
- **拡張可能**: 新しいプラットフォームの追加が容易

## 🎯 対応ユースケース

- **荷物預かり**: 「チェックイン前に荷物を預かってもらえますか？」
- **予約確認**: 「来月15日から3泊4日で予約できますか？」
- **観光地案内**: 「ホテル周辺でおすすめの観光地はありますか？」
- **チェックイン時間**: 「チェックイン時間は何時ですか？」
- **WiFi情報**: 「WiFiは無料で使えますか？パスワードを教えてください」
- **レストラン情報**: 「ホテルにレストランはありますか？朝食は含まれていますか？」
- **アクセス案内**: 「空港からホテルまでのアクセス方法を教えてください」
- **ベッド追加**: 「ベッドを追加して宿泊できますか？追加料金はかかりますか？」

## 🏗️ システム構成

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

## 🚀 クイックスタート

### 1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/hotel-response-system.git
cd hotel-response-system
```

### 2. 環境変数の設定
```bash
# 環境変数ファイルをコピー
cp env.example .env

# .envファイルを編集してAPIキーを設定
nano .env
```

### 3. Docker Composeで起動
```bash
# システム起動
docker-compose up -d

# ログ確認
docker-compose logs -f
```

### 4. アクセス
- **Web UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## ⚙️ 環境変数の設定

`.env`ファイルに以下の環境変数を設定してください：

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database Configuration
DATABASE_URL=postgresql://hotel_user:hotel_password@postgres:5432/hotel_db

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Application Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 📋 必要なAPIキー

### 必須
- **OpenAI API**: 返信生成に使用（将来実装予定）
- **Google Maps API**: 周辺観光地検索に使用

### オプション
- **Booking.com API**: 実際の予約データ取得
- **Airbnb API**: 実際の予約データ取得

> **注意**: APIキーが設定されていない場合でも、モックデータを使用してシステムは動作します。

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

## 📁 プロジェクト構造

```
hotel-response-system/
├── app/                    # アプリケーション本体
│   ├── agents/            # AIエージェント
│   │   ├── hotel_info_agent.py
│   │   └── booking_data_agent.py
│   ├── services/          # ビジネスロジック
│   │   ├── api_service.py
│   │   └── response_generator.py
│   ├── config.py          # 設定管理
│   ├── database.py        # データベース接続
│   ├── main.py            # FastAPIアプリケーション
│   └── models.py          # データベースモデル
├── streamlit_app.py       # フロントエンド
├── docker-compose.yml     # Docker設定
├── Dockerfile            # Dockerイメージ定義
├── requirements.txt      # Python依存関係
├── .gitignore           # Git除外設定
├── env.example          # 環境変数例
├── construction.md      # システム構成詳細
├── SECURITY.md          # セキュリティガイドライン
└── README.md           # プロジェクト説明
```

## 🔒 セキュリティ

このプロジェクトは以下のセキュリティ対策を実装しています：

- **環境変数による機密情報管理**
- **APIキーの適切な除外設定**
- **データベース接続の暗号化**
- **CORS設定によるアクセス制御**

詳細は [SECURITY.md](SECURITY.md) を参照してください。

## 📖 ドキュメント

- **[システム構成詳細](construction.md)**: アーキテクチャとコンポーネントの詳細説明
- **[セキュリティガイドライン](SECURITY.md)**: セキュリティ対策とベストプラクティス
- **[API ドキュメント](http://localhost:8000/docs)**: FastAPI自動生成ドキュメント

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🆘 サポート

問題が発生した場合や質問がある場合は、以下の方法でサポートを受けてください：

1. [GitHub Issues](https://github.com/yourusername/hotel-response-system/issues) で報告
2. ドキュメントを確認
3. ログを確認してトラブルシューティング

## 🔮 今後の予定

- [ ] OpenAI GPT統合による高度な返信生成
- [ ] 多言語対応（英語、中国語、韓国語）
- [ ] 感情分析機能
- [ ] リアルタイムダッシュボード
- [ ] モバイルアプリ対応
- [ ] 音声メッセージ対応

## 🙏 謝辞

このプロジェクトは以下のオープンソースプロジェクトに依存しています：

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [SQLAlchemy](https://sqlalchemy.org/)
- [Docker](https://docker.com/)

---
