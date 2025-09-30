# Streamlit用の簡単な起動コマンド

## 🚀 クイックスタート

### 1. 環境変数の設定
```bash
cp env.example .env
# .envファイルを編集してAPIキーを設定
```

### 2. 自動デプロイ
```bash
python start-streamlit.py
```

### 3. 手動デプロイ
```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows

# 依存関係インストール
pip install -r requirements-streamlit.txt

# データベース初期化
python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"

# サンプルデータ作成
python -c "from app.seed_data import create_sample_data; create_sample_data()"

# FastAPIサーバー起動（別ターミナル）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Streamlitアプリ起動（別ターミナル）
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### 4. テスト実行
```bash
python test-streamlit.py
```

## 🌐 アクセス

- **Streamlitアプリ**: http://localhost:8501
- **FastAPI API**: http://localhost:8000
- **API仕様書**: http://localhost:8000/docs

## 🔧 トラブルシューティング

### よくある問題
1. **API接続エラー**: FastAPIサーバーが起動しているか確認
2. **データベースエラー**: データベース初期化を再実行
3. **依存関係エラー**: 仮想環境を再作成
4. **ポート競合**: 他のアプリケーションでポートを使用していないか確認

## 📁 ファイル構成

```
pushtest/
├── .streamlit/config.toml      # Streamlit設定
├── app/                        # FastAPIアプリ
├── streamlit_app.py           # Streamlitアプリ
├── requirements-streamlit.txt  # 依存関係
├── env.example                 # 環境変数例
├── start-streamlit.py         # Python起動スクリプト
├── test-streamlit.py          # テストスクリプト
└── DEPLOYMENT-GUIDE.md        # 詳細ガイド
```

## 🔒 セキュリティ

- `.env`ファイルは`.gitignore`に含まれています
- APIキーは環境変数で管理
- 本番環境では適切な認証を実装してください
