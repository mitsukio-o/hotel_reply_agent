#!/bin/bash

# Streamlitデプロイスクリプト
echo "🚀 Streamlitデプロイスクリプトを開始します..."

# 環境変数ファイルの確認
if [ ! -f ".env" ]; then
    echo "⚠️  .envファイルが見つかりません。env.exampleをコピーして設定してください。"
    echo "cp env.example .env"
    echo "その後、.envファイルを編集してAPIキーを設定してください。"
    exit 1
fi

# Python仮想環境の確認
if [ ! -d "venv" ]; then
    echo "📦 Python仮想環境を作成中..."
    python -m venv venv
fi

# 仮想環境をアクティベート
echo "🔧 仮想環境をアクティベート中..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate

# 依存関係のインストール
echo "📥 依存関係をインストール中..."
pip install -r requirements-streamlit.txt

# データベースの初期化
echo "🗄️ データベースを初期化中..."
python -c "
from app.database import engine, Base
from app.models import *
Base.metadata.create_all(bind=engine)
print('データベース初期化完了')
"

# サンプルデータの作成
echo "📊 サンプルデータを作成中..."
python -c "
from app.seed_data import create_sample_data
create_sample_data()
print('サンプルデータ作成完了')
"

# FastAPIサーバーをバックグラウンドで起動
echo "🌐 FastAPIサーバーを起動中..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# 少し待機
sleep 3

# Streamlitアプリを起動
echo "🎨 Streamlitアプリを起動中..."
echo "ブラウザで http://localhost:8501 にアクセスしてください"
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# クリーンアップ
echo "🧹 クリーンアップ中..."
kill $API_PID 2>/dev/null
echo "✅ デプロイ完了"
