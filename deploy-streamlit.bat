@echo off
echo 🚀 Streamlitデプロイスクリプトを開始します...

REM 環境変数ファイルの確認
if not exist ".env" (
    echo ⚠️  .envファイルが見つかりません。env.exampleをコピーして設定してください。
    echo copy env.example .env
    echo その後、.envファイルを編集してAPIキーを設定してください。
    pause
    exit /b 1
)

REM Python仮想環境の確認
if not exist "venv" (
    echo 📦 Python仮想環境を作成中...
    python -m venv venv
)

REM 仮想環境をアクティベート
echo 🔧 仮想環境をアクティベート中...
call venv\Scripts\activate.bat

REM 依存関係のインストール
echo 📥 依存関係をインストール中...
pip install -r requirements-streamlit.txt

REM データベースの初期化
echo 🗄️ データベースを初期化中...
python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine); print('データベース初期化完了')"

REM サンプルデータの作成
echo 📊 サンプルデータを作成中...
python -c "from app.seed_data import create_sample_data; create_sample_data(); print('サンプルデータ作成完了')"

REM FastAPIサーバーをバックグラウンドで起動
echo 🌐 FastAPIサーバーを起動中...
start /B python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

REM 少し待機
timeout /t 3 /nobreak >nul

REM Streamlitアプリを起動
echo 🎨 Streamlitアプリを起動中...
echo ブラウザで http://localhost:8501 にアクセスしてください
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

echo ✅ デプロイ完了
pause
