#!/usr/bin/env python3
"""
Streamlit用の簡単な起動スクリプト
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def run_command(command, cwd=None):
    """コマンドを実行"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Pythonのバージョンをチェック"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8以上が必要です")
        print(f"現在のバージョン: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} を検出")
    return True

def check_requirements():
    """必要なファイルの存在をチェック"""
    required_files = [
        "requirements-streamlit.txt",
        "streamlit_app.py",
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/models.py",
        "app/seed_data.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ 以下のファイルが見つかりません:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("✅ 必要なファイルがすべて存在します")
    return True

def install_dependencies():
    """依存関係をインストール"""
    print("📥 依存関係をインストール中...")
    success, stdout, stderr = run_command("pip install -r requirements-streamlit.txt")
    
    if not success:
        print("❌ 依存関係のインストールに失敗しました")
        print(f"エラー: {stderr}")
        return False
    
    print("✅ 依存関係のインストールが完了しました")
    return True

def initialize_database():
    """データベースを初期化"""
    print("🗄️ データベースを初期化中...")
    
    # データベーステーブルを作成
    success, stdout, stderr = run_command("python -c \"from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine); print('データベース初期化完了')\"")
    
    if not success:
        print("❌ データベースの初期化に失敗しました")
        print(f"エラー: {stderr}")
        return False
    
    print("✅ データベースの初期化が完了しました")
    return True

def create_sample_data():
    """サンプルデータを作成"""
    print("📊 サンプルデータを作成中...")
    
    success, stdout, stderr = run_command("python -c \"from app.seed_data import create_sample_data; create_sample_data(); print('サンプルデータ作成完了')\"")
    
    if not success:
        print("❌ サンプルデータの作成に失敗しました")
        print(f"エラー: {stderr}")
        return False
    
    print("✅ サンプルデータの作成が完了しました")
    return True

def start_fastapi():
    """FastAPIサーバーを起動"""
    print("🌐 FastAPIサーバーを起動中...")
    
    # FastAPIサーバーをバックグラウンドで起動
    process = subprocess.Popen(
        ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 少し待機してサーバーが起動するのを待つ
    time.sleep(3)
    
    # サーバーが起動しているかチェック
    success, stdout, stderr = run_command("curl -s http://localhost:8000/health")
    
    if not success:
        print("❌ FastAPIサーバーの起動に失敗しました")
        process.terminate()
        return None
    
    print("✅ FastAPIサーバーが起動しました")
    return process

def start_streamlit():
    """Streamlitアプリを起動"""
    print("🎨 Streamlitアプリを起動中...")
    print("ブラウザで http://localhost:8501 にアクセスしてください")
    
    # Streamlitアプリを起動
    process = subprocess.Popen(
        ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process

def cleanup_processes(processes):
    """プロセスをクリーンアップ"""
    print("🧹 クリーンアップ中...")
    for process in processes:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

def main():
    """メイン関数"""
    print("🚀 Streamlitデプロイスクリプトを開始します...")
    print("=" * 50)
    
    # 環境チェック
    if not check_python_version():
        return 1
    
    if not check_requirements():
        return 1
    
    # 依存関係のインストール
    if not install_dependencies():
        return 1
    
    # データベースの初期化
    if not initialize_database():
        return 1
    
    # サンプルデータの作成
    if not create_sample_data():
        return 1
    
    # FastAPIサーバーを起動
    fastapi_process = start_fastapi()
    if not fastapi_process:
        return 1
    
    # Streamlitアプリを起動
    streamlit_process = start_streamlit()
    if not streamlit_process:
        cleanup_processes([fastapi_process])
        return 1
    
    print("=" * 50)
    print("✅ デプロイが完了しました！")
    print("🌐 FastAPI API: http://localhost:8000")
    print("🎨 Streamlit App: http://localhost:8501")
    print("📚 API仕様書: http://localhost:8000/docs")
    print("=" * 50)
    print("終了するには Ctrl+C を押してください")
    
    try:
        # プロセスが終了するまで待機
        while True:
            if fastapi_process.poll() is not None:
                print("❌ FastAPIサーバーが終了しました")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlitアプリが終了しました")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 ユーザーによって中断されました")
    finally:
        cleanup_processes([fastapi_process, streamlit_process])
    
    print("✅ デプロイスクリプトが終了しました")
    return 0

if __name__ == "__main__":
    sys.exit(main())
