#!/usr/bin/env python3
"""
統合されたStreamlitアプリのテストスクリプト
"""

import subprocess
import sys
import time
import requests
import os

def test_integrated_app():
    """統合されたアプリをテスト"""
    print("🧪 統合されたStreamlitアプリをテスト中...")
    
    # 必要なファイルの存在確認
    required_files = [
        "streamlit_app_integrated.py",
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/models.py"
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
    
    # Pythonのバージョンチェック
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8以上が必要です")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} を検出")
    
    # 依存関係のインストール
    print("📥 依存関係をインストール中...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "requests", "sqlite3"], 
                      check=True, capture_output=True)
        print("✅ 依存関係のインストールが完了しました")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依存関係のインストールに失敗しました: {e}")
        return False
    
    # 統合されたアプリの起動テスト
    print("🚀 統合されたStreamlitアプリを起動中...")
    print("ブラウザで http://localhost:8501 にアクセスしてください")
    print("終了するには Ctrl+C を押してください")
    
    try:
        # Streamlitアプリを起動
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app_integrated.py", 
             "--server.port", "8501", "--server.address", "0.0.0.0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 少し待機
        time.sleep(5)
        
        # アプリが起動しているかチェック
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            if response.status_code == 200:
                print("✅ Streamlitアプリが正常に起動しました")
                print("🌐 アプリURL: http://localhost:8501")
                return True
            else:
                print(f"❌ Streamlitアプリの起動に失敗しました: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Streamlitアプリに接続できません")
            return False
        
    except Exception as e:
        print(f"❌ アプリ起動エラー: {str(e)}")
        return False

def main():
    """メイン関数"""
    print("🚀 統合されたStreamlitアプリテストスクリプトを開始します...")
    print("=" * 60)
    
    if test_integrated_app():
        print("=" * 60)
        print("🎉 統合されたStreamlitアプリのテストが成功しました！")
        print("🌐 アプリURL: http://localhost:8501")
        print("📋 機能:")
        print("  - データベース自動初期化")
        print("  - サンプルデータ自動作成")
        print("  - APIサーバー自動起動")
        print("  - メッセージ管理")
        print("  - 分析データ表示")
        print("  - 周辺観光地情報")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("❌ 統合されたStreamlitアプリのテストが失敗しました")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
