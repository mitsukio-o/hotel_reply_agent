# 🚀 Streamlitデプロイガイド

## 📋 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）
- インターネット接続

## 🎯 クイックスタート

### 1. 環境変数の設定

```bash
# 環境変数ファイルをコピー
cp env.example .env

# .envファイルを編集してAPIキーを設定
# 最低限必要な設定:
# - OPENAI_API_KEY (OpenAI APIキー)
# - GOOGLE_MAPS_API_KEY (Google Maps APIキー、オプション)
```

### 2. 自動デプロイ（推奨）

#### Pythonスクリプトを使用:
```bash
python start-streamlit.py
```

#### バッチファイルを使用（Windows）:
```bash
deploy-streamlit.bat
```

#### シェルスクリプトを使用（Linux/Mac）:
```bash
chmod +x deploy-streamlit.sh
./deploy-streamlit.sh
```

### 3. 手動デプロイ

#### ステップ1: 仮想環境の作成
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows
```

#### ステップ2: 依存関係のインストール
```bash
pip install -r requirements-streamlit.txt
```

#### ステップ3: データベースの初期化
```bash
python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

#### ステップ4: サンプルデータの作成
```bash
python -c "from app.seed_data import create_sample_data; create_sample_data()"
```

#### ステップ5: サーバーの起動
```bash
# FastAPIサーバー（別ターミナル）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Streamlitアプリ（別ターミナル）
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 🌐 アクセス

- **Streamlitアプリ**: http://localhost:8501
- **FastAPI API**: http://localhost:8000
- **API仕様書**: http://localhost:8000/docs

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 1. API接続エラー
```
エラー: APIサーバーに接続できません
```
**解決方法:**
- FastAPIサーバーが起動しているか確認
- ポート8000が使用可能か確認
- ファイアウォール設定を確認

#### 2. データベースエラー
```
エラー: データベースの初期化に失敗しました
```
**解決方法:**
- SQLiteファイルの権限を確認
- データベース初期化を再実行
- ディスク容量を確認

#### 3. 依存関係エラー
```
エラー: 依存関係のインストールに失敗しました
```
**解決方法:**
- Python 3.8以上を使用
- 仮想環境を再作成
- pipを最新版に更新

#### 4. ポート競合エラー
```
エラー: ポートが既に使用されています
```
**解決方法:**
- 他のアプリケーションでポートを使用していないか確認
- プロセスを終了してから再起動
- 別のポートを使用

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
├── start-streamlit.py       # Python起動スクリプト
├── deploy-streamlit.sh      # Linux/Macデプロイスクリプト
├── deploy-streamlit.bat     # Windowsデプロイスクリプト
└── README-STREAMLIT.md      # このファイル
```

## 🔒 セキュリティ

- `.env`ファイルは`.gitignore`に含まれています
- APIキーは環境変数で管理
- 本番環境では適切な認証を実装してください

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. **ログファイルの確認**
2. **環境変数の設定**
3. **依存関係のバージョン**
4. **ネットワーク接続**

## 🎯 次のステップ

- [ ] 本番環境へのデプロイ
- [ ] CI/CDパイプラインの構築
- [ ] 監視・ログ機能の追加
- [ ] パフォーマンス最適化

## 📝 注意事項

- 初回起動時は依存関係のインストールに時間がかかる場合があります
- APIキーは適切に管理し、公開しないでください
- 本番環境では適切なセキュリティ設定を行ってください
