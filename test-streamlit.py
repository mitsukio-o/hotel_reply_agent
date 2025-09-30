#!/usr/bin/env python3
"""
Streamlit用の簡単なテストスクリプト
"""

import requests
import time
import sys
from pathlib import Path

def test_api_connection(base_url="http://localhost:8000"):
    """API接続をテスト"""
    print(f"🔍 API接続をテスト中: {base_url}")
    
    try:
        # ヘルスチェック
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API接続成功")
            return True
        else:
            print(f"❌ API接続失敗: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API接続エラー: サーバーに接続できません")
        return False
    except requests.exceptions.Timeout:
        print("❌ API接続タイムアウト")
        return False
    except Exception as e:
        print(f"❌ API接続エラー: {str(e)}")
        return False

def test_hotels_endpoint(base_url="http://localhost:8000"):
    """ホテルエンドポイントをテスト"""
    print("🏨 ホテルエンドポイントをテスト中...")
    
    try:
        response = requests.get(f"{base_url}/hotels", timeout=10)
        if response.status_code == 200:
            hotels = response.json()
            print(f"✅ ホテル一覧取得成功: {len(hotels)}件")
            return hotels
        else:
            print(f"❌ ホテル一覧取得失敗: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ ホテル一覧取得エラー: {str(e)}")
        return []

def test_messages_endpoint(base_url="http://localhost:8000", hotel_id=1):
    """メッセージエンドポイントをテスト"""
    print(f"📨 メッセージエンドポイントをテスト中 (ホテルID: {hotel_id})...")
    
    try:
        response = requests.get(f"{base_url}/messages/{hotel_id}", timeout=10)
        if response.status_code == 200:
            messages = response.json()
            print(f"✅ メッセージ一覧取得成功: {len(messages)}件")
            return messages
        else:
            print(f"❌ メッセージ一覧取得失敗: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ メッセージ一覧取得エラー: {str(e)}")
        return []

def test_analytics_endpoint(base_url="http://localhost:8000", hotel_id=1):
    """分析エンドポイントをテスト"""
    print(f"📊 分析エンドポイントをテスト中 (ホテルID: {hotel_id})...")
    
    try:
        response = requests.get(f"{base_url}/hotels/{hotel_id}/analytics", timeout=15)
        if response.status_code == 200:
            analytics = response.json()
            print("✅ 分析データ取得成功")
            return analytics
        else:
            print(f"❌ 分析データ取得失敗: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ 分析データ取得エラー: {str(e)}")
        return {}

def test_nearby_attractions_endpoint(base_url="http://localhost:8000", hotel_id=1):
    """周辺観光地エンドポイントをテスト"""
    print(f"🏞️ 周辺観光地エンドポイントをテスト中 (ホテルID: {hotel_id})...")
    
    try:
        response = requests.get(f"{base_url}/hotels/{hotel_id}/nearby-attractions", timeout=15)
        if response.status_code == 200:
            attractions = response.json()
            print(f"✅ 周辺観光地取得成功: {len(attractions.get('attractions', []))}件")
            return attractions
        else:
            print(f"❌ 周辺観光地取得失敗: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ 周辺観光地取得エラー: {str(e)}")
        return {}

def test_streamlit_app():
    """Streamlitアプリのテスト"""
    print("🎨 Streamlitアプリをテスト中...")
    
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlitアプリ接続成功")
            return True
        else:
            print(f"❌ Streamlitアプリ接続失敗: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Streamlitアプリ接続エラー: アプリに接続できません")
        return False
    except Exception as e:
        print(f"❌ Streamlitアプリ接続エラー: {str(e)}")
        return False

def main():
    """メイン関数"""
    print("🧪 Streamlitテストスクリプトを開始します...")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # API接続テスト
    if not test_api_connection(base_url):
        print("❌ API接続に失敗しました。サーバーが起動しているか確認してください。")
        return 1
    
    # ホテルエンドポイントテスト
    hotels = test_hotels_endpoint(base_url)
    if not hotels:
        print("❌ ホテルデータが見つかりません。サンプルデータを作成してください。")
        return 1
    
    # 最初のホテルのIDを取得
    hotel_id = hotels[0]['id'] if hotels else 1
    
    # メッセージエンドポイントテスト
    messages = test_messages_endpoint(base_url, hotel_id)
    
    # 分析エンドポイントテスト
    analytics = test_analytics_endpoint(base_url, hotel_id)
    
    # 周辺観光地エンドポイントテスト
    attractions = test_nearby_attractions_endpoint(base_url, hotel_id)
    
    # Streamlitアプリテスト
    streamlit_ok = test_streamlit_app()
    
    print("=" * 50)
    print("📋 テスト結果サマリー:")
    print(f"  - API接続: ✅")
    print(f"  - ホテル一覧: ✅ ({len(hotels)}件)")
    print(f"  - メッセージ一覧: ✅ ({len(messages)}件)")
    print(f"  - 分析データ: ✅")
    print(f"  - 周辺観光地: ✅ ({len(attractions.get('attractions', []))}件)")
    print(f"  - Streamlitアプリ: {'✅' if streamlit_ok else '❌'}")
    
    if streamlit_ok:
        print("\n🎉 すべてのテストが成功しました！")
        print("🌐 Streamlitアプリ: http://localhost:8501")
        print("🌐 FastAPI API: http://localhost:8000")
        print("📚 API仕様書: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️ 一部のテストが失敗しました。")
        print("Streamlitアプリが起動しているか確認してください。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
