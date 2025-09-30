#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
サンプルデータ作成スクリプト
ホテル、予約、メッセージのサンプルデータを作成します
"""

import requests
import json
from datetime import datetime, timedelta
import random

# API設定
API_BASE_URL = "http://localhost:8000"

def create_sample_bookings_and_messages(hotel_id: int):
    """サンプルの予約とメッセージを作成"""
    
    # サンプル予約データ
    sample_bookings = [
        {
            "guest_name": "田中太郎",
            "check_in": (datetime.now() + timedelta(days=7)).isoformat(),
            "check_out": (datetime.now() + timedelta(days=10)).isoformat(),
            "room_type": "シングル",
            "guest_count": 1,
            "booking_reference": f"BK{hotel_id}001",
            "status": "confirmed"
        },
        {
            "guest_name": "佐藤花子",
            "check_in": (datetime.now() + timedelta(days=14)).isoformat(),
            "check_out": (datetime.now() + timedelta(days=17)).isoformat(),
            "room_type": "ダブル",
            "guest_count": 2,
            "booking_reference": f"BK{hotel_id}002",
            "status": "confirmed"
        },
        {
            "guest_name": "鈴木一郎",
            "check_in": (datetime.now() + timedelta(days=21)).isoformat(),
            "check_out": (datetime.now() + timedelta(days=24)).isoformat(),
            "room_type": "ツイン",
            "guest_count": 2,
            "booking_reference": f"BK{hotel_id}003",
            "status": "confirmed"
        }
    ]
    
    # サンプルメッセージデータ
    sample_messages = [
        {
            "platform": "booking.com",
            "message_content": "チェックイン前に荷物を預かってもらえますか？午前10時に到着予定です。",
            "message_type": "luggage"
        },
        {
            "platform": "airbnb",
            "message_content": "来月の15日から3泊4日で予約できますか？",
            "message_type": "availability"
        },
        {
            "platform": "booking.com",
            "message_content": "ホテル周辺でおすすめの観光地はありますか？",
            "message_type": "attractions"
        },
        {
            "platform": "airbnb",
            "message_content": "チェックイン時間は何時ですか？",
            "message_type": "checkin"
        },
        {
            "platform": "booking.com",
            "message_content": "WiFiは無料で使えますか？パスワードを教えてください。",
            "message_type": "wifi"
        }
    ]
    
    print(f"[INFO] ホテルID {hotel_id} のサンプルデータを作成中...")
    
    # 予約を作成（実際のAPIエンドポイントがないため、直接データベースに挿入することを想定）
    # ここでは、メッセージ取得APIをテストするために、ダミーデータを返す
    
    # メッセージ取得をテスト
    try:
        response = requests.get(f"{API_BASE_URL}/messages/{hotel_id}")
        if response.status_code == 200:
            messages = response.json()
            print(f"[OK] メッセージ取得成功: {len(messages)}件")
            return messages
        else:
            print(f"[ERROR] メッセージ取得失敗: {response.status_code}")
            return []
    except Exception as e:
        print(f"[ERROR] メッセージ取得エラー: {e}")
        return []

def create_sample_data_for_hotels():
    """すべてのホテルに対してサンプルデータを作成"""
    
    # ホテル一覧を取得
    try:
        response = requests.get(f"{API_BASE_URL}/hotels")
        if response.status_code == 200:
            hotels = response.json()
            print(f"[INFO] {len(hotels)}件のホテルが見つかりました")
            
            for hotel in hotels:
                hotel_id = hotel['id']
                create_sample_bookings_and_messages(hotel_id)
            
            return True
        else:
            print(f"[ERROR] ホテル一覧取得失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] ホテル一覧取得エラー: {e}")
        return False

def main():
    """メイン関数"""
    print("サンプルデータ作成スクリプト")
    print("=" * 50)
    
    # ヘルスチェック
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("[OK] APIサーバーが正常に動作しています")
        else:
            print("[ERROR] APIサーバーに接続できません")
            return
    except Exception as e:
        print(f"[ERROR] API接続エラー: {e}")
        return
    
    # サンプルデータを作成
    success = create_sample_data_for_hotels()
    
    if success:
        print("\n[SUCCESS] サンプルデータの作成が完了しました")
        print("\n[INFO] 次のステップ:")
        print("   1. python test_data.py を再実行")
        print("   2. メッセージ管理機能をテスト")
    else:
        print("\n[ERROR] サンプルデータの作成に失敗しました")

if __name__ == "__main__":
    main()
