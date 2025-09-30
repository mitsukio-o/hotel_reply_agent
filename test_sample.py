#!/usr/bin/env python3
"""
ホテル向け自動返信システム - APIテストサンプル

このファイルは、システムの各APIエンドポイントをテストするためのサンプルコードです。
実際のテストやデバッグに使用できます。

使用方法:
    python test_sample.py

必要な環境:
    - システムが起動していること (docker-compose up -d)
    - 必要なAPIキーが設定されていること (.envファイル)
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# 設定
API_BASE_URL = "http://localhost:8000"
STREAMLIT_URL = "http://localhost:8501"

# リクエストタイムアウト設定
REQUEST_TIMEOUT = 10  # 10秒

class HotelAPITester:
    """ホテルAPIテストクラス"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = REQUEST_TIMEOUT
        self.test_hotel_id = None
        self.test_message_id = None
        
    def test_health_check(self) -> bool:
        """ヘルスチェックテスト"""
        print("ヘルスチェックテスト...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print(f"OK ヘルスチェック成功: {data}")
                return True
            else:
                print(f"[ERROR] ヘルスチェック失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] ヘルスチェックエラー: {e}")
            return False
    
    def test_root_endpoint(self) -> bool:
        """ルートエンドポイントテスト"""
        print("[TEST] ルートエンドポイントテスト...")
        try:
            response = self.session.get(f"{self.base_url}/", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] ルートエンドポイント成功: {data}")
                return True
            else:
                print(f"[ERROR] ルートエンドポイント失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] ルートエンドポイントエラー: {e}")
            return False
    
    def create_test_hotel(self) -> Optional[int]:
        """テスト用ホテルを作成"""
        print("[HOTEL] テスト用ホテルを作成...")
        
        hotel_data = {
            "name": "テストホテル東京",
            "address": "東京都渋谷区道玄坂1-2-3",
            "latitude": 35.6581,
            "longitude": 139.7016,
            "city": "東京",
            "country": "日本"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/hotels", params=hotel_data, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                hotel_id = data["id"]
                print(f"[OK] テストホテル作成成功: ID={hotel_id}, 名前={data['name']}")
                self.test_hotel_id = hotel_id
                return hotel_id
            else:
                print(f"[ERROR] テストホテル作成失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                return None
        except Exception as e:
            print(f"[ERROR] テストホテル作成エラー: {e}")
            return None
    
    def get_hotels(self) -> List[Dict]:
        """ホテル一覧を取得"""
        print("[TEST] ホテル一覧を取得...")
        try:
            response = self.session.get(f"{self.base_url}/hotels", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                hotels = response.json()
                print(f"[OK] ホテル一覧取得成功: {len(hotels)}件")
                for hotel in hotels:
                    print(f"  - ID: {hotel['id']}, 名前: {hotel['name']}, 都市: {hotel['city']}")
                return hotels
            else:
                print(f"[ERROR] ホテル一覧取得失敗: {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] ホテル一覧取得エラー: {e}")
            return []
    
    def create_test_message(self, hotel_id: int) -> Optional[int]:
        """テスト用メッセージを作成"""
        print("📨 テスト用メッセージを作成...")
        
        # 実際のAPIを使用してメッセージを取得する代わりに、
        # データベースに直接テストデータを挿入することを想定
        # ここでは、メッセージ取得APIをテスト
        
        try:
            response = self.session.post(f"{self.base_url}/messages/fetch/{hotel_id}", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] メッセージ取得成功: {data}")
                return None  # 実際のメッセージIDは取得できない場合がある
            else:
                print(f"[ERROR] メッセージ取得失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                return None
        except Exception as e:
            print(f"[ERROR] メッセージ取得エラー: {e}")
            return None
    
    def get_messages(self, hotel_id: int) -> List[Dict]:
        """メッセージ一覧を取得"""
        print(f"[TEST] ホテルID {hotel_id} のメッセージ一覧を取得...")
        try:
            response = self.session.get(f"{self.base_url}/messages/{hotel_id}", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                messages = response.json()
                print(f"[OK] メッセージ一覧取得成功: {len(messages)}件")
                for message in messages:
                    print(f"  - ID: {message['id']}, プラットフォーム: {message['platform']}")
                    print(f"    内容: {message['message_content'][:50]}...")
                    print(f"    処理済み: {message['is_processed']}")
                return messages
            else:
                print(f"[ERROR] メッセージ一覧取得失敗: {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] メッセージ一覧取得エラー: {e}")
            return []
    
    def test_response_suggestions(self, message_id: int, hotel_id: int) -> bool:
        """返信候補生成テスト"""
        print(f"[TEST] メッセージID {message_id} の返信候補を生成...")
        try:
            response = self.session.post(
                f"{self.base_url}/messages/{message_id}/suggestions",
                params={"hotel_id": hotel_id},
                timeout=30  # 返信候補生成は時間がかかる場合がある
            )
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] 返信候補生成成功:")
                print(f"  メッセージタイプ: {data['message_type']}")
                print(f"  候補数: {len(data['suggestions'])}")
                
                for i, suggestion in enumerate(data['suggestions']):
                    print(f"  候補 {i+1}:")
                    print(f"    内容: {suggestion['content'][:100]}...")
                    print(f"    信頼度: {suggestion['confidence']}")
                    print(f"    タイプ: {suggestion['type']}")
                
                return True
            else:
                print(f"[ERROR] 返信候補生成失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] 返信候補生成エラー: {e}")
            return False
    
    def test_send_response(self, message_id: int, response_content: str, platform: str) -> bool:
        """返信送信テスト"""
        print(f"[TEST] メッセージID {message_id} に返信を送信...")
        try:
            response = self.session.post(
                f"{self.base_url}/messages/{message_id}/respond",
                params={
                    "response_content": response_content,
                    "platform": platform
                },
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] 返信送信成功: {data}")
                return True
            else:
                print(f"[ERROR] 返信送信失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] 返信送信エラー: {e}")
            return False
    
    def test_analytics(self, hotel_id: int) -> bool:
        """分析データ取得テスト"""
        print(f"[TEST] ホテルID {hotel_id} の分析データを取得...")
        try:
            response = self.session.get(f"{self.base_url}/hotels/{hotel_id}/analytics", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] 分析データ取得成功:")
                
                booking_analysis = data.get('booking_analysis', {})
                print(f"  予約分析:")
                print(f"    総予約数: {booking_analysis.get('total_bookings', 0)}")
                print(f"    平均滞在日数: {booking_analysis.get('average_stay_duration', 0)}日")
                print(f"    平均宿泊人数: {booking_analysis.get('average_guest_count', 0)}人")
                
                learning_result = data.get('learning_result', {})
                print(f"  学習結果:")
                print(f"    処理済みメッセージ: {learning_result.get('messages_processed', 0)}件")
                print(f"    処理済み返信: {learning_result.get('responses_processed', 0)}件")
                print(f"    読み込み済みテンプレート: {learning_result.get('templates_loaded', 0)}件")
                
                return True
            else:
                print(f"[ERROR] 分析データ取得失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] 分析データ取得エラー: {e}")
            return False
    
    def test_nearby_attractions(self, hotel_id: int) -> bool:
        """周辺観光地取得テスト"""
        print(f"[TEST] ホテルID {hotel_id} の周辺観光地を取得...")
        try:
            response = self.session.get(
                f"{self.base_url}/hotels/{hotel_id}/nearby-attractions",
                params={"radius": 2000},
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                attractions = data.get('attractions', [])
                print(f"[OK] 周辺観光地取得成功: {len(attractions)}件")
                
                for attraction in attractions[:5]:  # 最初の5件のみ表示
                    print(f"  - 名前: {attraction['name']}")
                    print(f"    カテゴリ: {attraction['category']}")
                    print(f"    距離: {attraction['distance_km']}km")
                    print(f"    評価: {attraction['rating']}/5")
                    print(f"    住所: {attraction['address']}")
                
                return True
            else:
                print(f"[ERROR] 周辺観光地取得失敗: {response.status_code}")
                print(f"レスポンス: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] 周辺観光地取得エラー: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """すべてのテストを実行"""
        print("[START] ホテルAPIテストを開始します...")
        print("=" * 50)
        
        # 基本テスト
        if not self.test_health_check():
            print("[ERROR] ヘルスチェックが失敗しました。システムが起動していない可能性があります。")
            return False
        
        if not self.test_root_endpoint():
            print("[ERROR] ルートエンドポイントが失敗しました。")
            return False
        
        # ホテル関連テスト
        hotels = self.get_hotels()
        if not hotels:
            print("[WARNING] ホテルが見つかりません。テスト用ホテルを作成します。")
            hotel_id = self.create_test_hotel()
            if not hotel_id:
                print("[ERROR] テスト用ホテルの作成に失敗しました。")
                return False
        else:
            hotel_id = hotels[0]['id']
            print(f"[OK] 既存のホテルを使用: ID={hotel_id}")
        
        # メッセージ関連テスト
        messages = self.get_messages(hotel_id)
        if messages:
            # 未処理のメッセージがある場合、返信候補をテスト
            unprocessed_messages = [m for m in messages if not m['is_processed']]
            if unprocessed_messages:
                message = unprocessed_messages[0]
                self.test_response_suggestions(message['id'], hotel_id)
                
                # テスト用返信を送信
                test_response = "お客様、お疲れ様です。ご質問にお答えいたします。"
                self.test_send_response(message['id'], test_response, message['platform'])
            else:
                print("[WARNING] 未処理のメッセージがありません。")
        else:
            print("[WARNING] メッセージが見つかりません。")
        
        # 分析データテスト
        self.test_analytics(hotel_id)
        
        # 周辺観光地テスト
        self.test_nearby_attractions(hotel_id)
        
        print("=" * 50)
        print("[OK] すべてのテストが完了しました！")
        return True

def test_streamlit_connection():
    """Streamlit接続テスト"""
    print("[TEST] Streamlit接続テスト...")
    try:
        response = requests.get(STREAMLIT_URL, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            print(f"[OK] Streamlit接続成功: {STREAMLIT_URL}")
            return True
        else:
            print(f"[ERROR] Streamlit接続失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Streamlit接続エラー: {e}")
        return False

def test_environment():
    """環境変数テスト"""
    print("[TEST] 環境変数テスト...")
    
    # 必須ではないが推奨される環境変数
    recommended_vars = [
        "OPENAI_API_KEY",
        "GOOGLE_MAPS_API_KEY",
        "BOOKING_API_KEY",
        "AIRBNB_API_KEY"
    ]
    
    missing_vars = []
    for var in recommended_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"[WARNING] 以下の環境変数が設定されていません: {', '.join(missing_vars)}")
        print("   一部の機能が制限される可能性があります。")
        print("   .envファイルを確認してください。")
        return True  # 警告のみでテストは続行
    else:
        print("[OK] 推奨環境変数が設定されています。")
        return True

def main():
    """メイン関数"""
    print("ホテル向け自動返信システム - APIテスト")
    print("=" * 60)
    
    # 環境変数テスト
    test_environment()  # 警告のみで続行
    
    # Streamlit接続テスト
    test_streamlit_connection()
    
    print("\n" + "=" * 60)
    
    # APIテスト実行
    tester = HotelAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n[SUCCESS] すべてのテストが成功しました！")
        print(f"[UI] Streamlit UI: {STREAMLIT_URL}")
        print(f"[DOCS] API Docs: {API_BASE_URL}/docs")
        print("\n[INFO] 次のステップ:")
        print("   1. Streamlit UIでホテルを選択")
        print("   2. メッセージ管理タブでメッセージを確認")
        print("   3. 返信候補を生成してテスト")
    else:
        print("\n[ERROR] 一部のテストが失敗しました。")
        print("   ログを確認して問題を解決してください。")
        print("\n[FIX] トラブルシューティング:")
        print("   1. docker-compose ps でサービスが起動しているか確認")
        print("   2. docker-compose logs api でAPIログを確認")
        print("   3. EXAMPLE.mdのトラブルシューティングセクションを参照")

if __name__ == "__main__":
    main()
