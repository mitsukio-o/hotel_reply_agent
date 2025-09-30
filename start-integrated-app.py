#!/usr/bin/env python3
"""
統合されたStreamlitアプリの簡単起動スクリプト
"""

import subprocess
import sys
import os
import time

def check_requirements():
    """必要なファイルの存在をチェック"""
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
    return True

def install_dependencies():
    """依存関係をインストール"""
    print("📥 依存関係をインストール中...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "requests"], 
                      check=True, capture_output=True)
        print("✅ 依存関係のインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依存関係のインストールに失敗しました: {e}")
        return False

def start_app():
    """統合されたアプリを起動"""
    print("🚀 統合されたStreamlitアプリを起動中...")
    print("ブラウザで http://localhost:8501 にアクセスしてください")
    print("終了するには Ctrl+C を押してください")
    print("=" * 60)
    
    try:
        # Streamlitアプリを起動
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app_integrated.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        return True
    except KeyboardInterrupt:
        print("\n🛑 ユーザーによって中断されました")
        return True
    except Exception as e:
        print(f"❌ アプリ起動エラー: {str(e)}")
        return False

def main():
    """メイン関数"""
    print("🚀 統合されたStreamlitアプリ起動スクリプト")
    print("=" * 60)
    
    # ファイル存在確認
    if not check_requirements():
        return 1
    
    # 依存関係インストール
    if not install_dependencies():
        return 1
    
    # アプリ起動
    if start_app():
        print("=" * 60)
        print("✅ アプリが正常に終了しました")
        return 0
    else:
        print("=" * 60)
        print("❌ アプリの起動に失敗しました")
        return 1

if __name__ == "__main__":
    sys.exit(main())
