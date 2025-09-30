# 🏨 ホテル返信システム - Streamlit版

## 🚀 クイックスタート

### 1. 環境設定

```bash
# 環境変数ファイルをコピー
cp env.example .env

# .envファイルを編集してAPIキーを設定
# 最低限必要な設定:
# - OPENAI_API_KEY (OpenAI APIキー)
# - GOOGLE_MAPS_API_KEY (Google Maps APIキー、オプション)
```

### 2. デプロイ実行

#### Windowsの場合:
```bash
deploy-streamlit.bat
```

#### Linux/Macの場合:
```bash
chmod +x deploy-streamlit.sh
./deploy-streamlit.sh
```

### 3. アクセス

- **Streamlitアプリ**: http://localhost:8501
- **FastAPI API**: http://localhost:8000
- **API仕様書**: http://localhost:8000/docs

## 📋 機能

- ✅ ホテル選択
- ✅ メッセージ管理
- ✅ 返信候補生成
- ✅ 分析データ表示
- ✅ 周辺観光地情報
- ✅ エラーハンドリング

## 🔧 手動セットアップ

### 1. 仮想環境作成
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows
```

### 2. 依存関係インストール
```bash
pip install -r requirements-streamlit.txt
```

### 3. データベース初期化
```bash
python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

### 4. サンプルデータ作成
```bash
python -c "from app.seed_data import create_sample_data; create_sample_data()"
```

### 5. サーバー起動
```bash
# FastAPIサーバー（別ターミナル）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Streamlitアプリ（別ターミナル）
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 🛠️ トラブルシューティング

### API接続エラー
- FastAPIサーバーが起動しているか確認
- ポート8000が使用可能か確認
- ファイアウォール設定を確認

### データベースエラー
- SQLiteファイルの権限を確認
- データベース初期化を再実行

### 依存関係エラー
- Python 3.8以上を使用
- 仮想環境を再作成

## 📁 ファイル構成

```
pushtest/
├── .streamlit/
│   └── config.toml          # Streamlit設定
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIアプリ
│   ├── config.py            # 設定管理
│   ├── database.py          # データベース接続
│   ├── models.py            # データモデル
│   ├── seed_data.py         # サンプルデータ
│   ├── agents/              # AIエージェント
│   └── services/            # サービス層
├── streamlit_app.py         # Streamlitアプリ
├── requirements-streamlit.txt # 依存関係
├── env.example              # 環境変数例
├── deploy-streamlit.sh      # Linux/Macデプロイスクリプト
├── deploy-streamlit.bat     # Windowsデプロイスクリプト
└── README.md                # このファイル
```

## 🔒 セキュリティ

- `.env`ファイルは`.gitignore`に含まれています
- APIキーは環境変数で管理
- 本番環境では適切な認証を実装してください

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. ログファイルの確認
2. 環境変数の設定
3. 依存関係のバージョン
4. ネットワーク接続

## 🎯 次のステップ

- [ ] 本番環境へのデプロイ
- [ ] CI/CDパイプラインの構築
- [ ] 監視・ログ機能の追加
- [ ] パフォーマンス最適化
