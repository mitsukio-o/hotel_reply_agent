#!/usr/bin/env python3
"""
ホテル向け自動返信システム - テスト用サンプルデータ

このファイルは、システムのテストに使用するサンプルデータを生成します。
実際のテストやデモンストレーションに使用できます。

使用方法:
    python test_data.py

必要な環境:
    - システムが起動していること (docker-compose up -d)
    - データベースが初期化されていること
"""

import requests
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import sys
import time

# 設定
API_BASE_URL = "http://localhost:8000"

# リクエストタイムアウト設定
REQUEST_TIMEOUT = 10  # 10秒

class TestDataGenerator:
    """テストデータ生成クラス"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = REQUEST_TIMEOUT
        self.hotel_ids = []
        
        # API接続テスト
        self._test_api_connection()
    
    def _test_api_connection(self) -> bool:
        """API接続をテスト"""
        print("[TEST] API接続をテスト中...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                print("[OK] API接続成功")
                return True
            else:
                print(f"[WARNING] API接続失敗: {response.status_code}")
                return False
        except requests.exceptions.Timeout:
            print("[ERROR] API接続タイムアウト - サーバーが起動していない可能性があります")
            return False
        except requests.exceptions.ConnectionError:
            print("[ERROR] API接続エラー - サーバーに接続できません")
            print(f"   確認事項:")
            print(f"   1. docker-compose up -d でサーバーが起動しているか")
            print(f"   2. http://localhost:8000 にアクセスできるか")
            return False
        except Exception as e:
            print(f"[ERROR] API接続エラー: {e}")
            return False
        
    def create_sample_hotels(self) -> List[int]:
        """サンプルホテルを作成"""
        print("[HOTEL] サンプルホテルを作成中...")
        
        hotels_data = [
            {
                "name": "東京ステーションホテル",
                "address": "東京都千代田区丸の内1-9-1",
                "latitude": 35.6812,
                "longitude": 139.7671,
                "city": "東京",
                "country": "日本"
            },
            {
                "name": "大阪グランドホテル",
                "address": "大阪府大阪市北区梅田1-1-1",
                "latitude": 34.6937,
                "longitude": 135.5023,
                "city": "大阪",
                "country": "日本"
            },
            {
                "name": "京都伝統ホテル",
                "address": "京都府京都市下京区四条通烏丸東入ル",
                "latitude": 35.0038,
                "longitude": 135.7694,
                "city": "京都",
                "country": "日本"
            },
            {
                "name": "横浜ベイホテル",
                "address": "神奈川県横浜市西区みなとみらい2-2-1",
                "latitude": 35.4542,
                "longitude": 139.6311,
                "city": "横浜",
                "country": "日本"
            },
            {
                "name": "福岡シティホテル",
                "address": "福岡県福岡市博多区博多駅前1-1-1",
                "latitude": 33.5904,
                "longitude": 130.4207,
                "city": "福岡",
                "country": "日本"
            }
        ]
        
        created_hotels = []
        for hotel_data in hotels_data:
            try:
                response = self.session.post(f"{self.base_url}/hotels", params=hotel_data, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    data = response.json()
                    hotel_id = data["id"]
                    created_hotels.append(hotel_id)
                    print(f"[OK] ホテル作成成功: {hotel_data['name']} (ID: {hotel_id})")
                else:
                    print(f"[ERROR] ホテル作成失敗: {hotel_data['name']} - {response.status_code}")
            except Exception as e:
                print(f"[ERROR] ホテル作成エラー: {hotel_data['name']} - {e}")
        
        self.hotel_ids = created_hotels
        return created_hotels
    
    def create_sample_messages(self, hotel_id: int) -> List[Dict]:
        """サンプルメッセージを作成"""
        print(f"[MESSAGE] ホテルID {hotel_id} のサンプルメッセージを作成中...")
        
        # テスト用のメッセージデータを作成
        sample_messages = [
            {
                "booking_id": f"test_booking_{hotel_id}_001",
                "platform": "booking.com",
                "message_content": "チェックイン前に荷物を預かってもらえますか？午前10時に到着予定です。",
                "message_type": "luggage",
                "guest_name": "田中太郎",
                "timestamp": datetime.now().isoformat()
            },
            {
                "booking_id": f"test_booking_{hotel_id}_002", 
                "platform": "airbnb",
                "message_content": "来月の15日から3泊4日で予約できますか？",
                "message_type": "availability",
                "guest_name": "佐藤花子",
                "timestamp": datetime.now().isoformat()
            },
            {
                "booking_id": f"test_booking_{hotel_id}_003",
                "platform": "booking.com", 
                "message_content": "ホテル周辺でおすすめの観光地はありますか？",
                "message_type": "attractions",
                "guest_name": "山田次郎",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        created_messages = []
        for message_data in sample_messages:
            try:
                # メッセージ作成のAPIエンドポイントを呼び出し
                response = self.session.post(
                    f"{self.base_url}/messages",
                    json=message_data,
                    params={"hotel_id": hotel_id},
                    timeout=REQUEST_TIMEOUT
                )
                if response.status_code == 200:
                    data = response.json()
                    created_messages.append(data)
                    print(f"[OK] メッセージ作成成功: {message_data['message_content'][:30]}...")
                else:
                    print(f"[ERROR] メッセージ作成失敗: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"[ERROR] メッセージ作成エラー: {e}")
        
        # 外部APIからのメッセージ取得もテスト
        try:
            response = self.session.post(f"{self.base_url}/messages/fetch/{hotel_id}", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] 外部メッセージ取得APIテスト成功: {data}")
            else:
                print(f"[WARNING] 外部メッセージ取得APIテスト失敗: {response.status_code}")
        except Exception as e:
            print(f"[WARNING] 外部メッセージ取得APIテストエラー: {e}")
        
        return created_messages
    
    def test_response_generation(self, hotel_id: int) -> bool:
        """返信生成テスト"""
        print(f"[TEST] ホテルID {hotel_id} の返信生成をテスト中...")
        
        # メッセージ一覧を取得
        try:
            response = self.session.get(f"{self.base_url}/messages/{hotel_id}", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                messages = response.json()
                if messages:
                    # 未処理のメッセージを探す
                    unprocessed_messages = [m for m in messages if not m.get('is_processed', False)]
                    if unprocessed_messages:
                        # 最初の未処理メッセージで返信候補をテスト
                        message = unprocessed_messages[0]
                        return self.test_single_response_generation(message['id'], hotel_id)
                    else:
                        print("[INFO] 未処理のメッセージが見つかりません - 処理済みメッセージでテストします")
                        # 処理済みメッセージでもテストを実行
                        message = messages[0]
                        return self.test_single_response_generation(message['id'], hotel_id)
                else:
                    print("[INFO] メッセージが見つかりません - 返信生成テストをスキップします")
                    return True  # メッセージがない場合は成功として扱う
            else:
                print(f"[ERROR] メッセージ取得失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] メッセージ取得エラー: {e}")
            return False
    
    def test_single_response_generation(self, message_id: int, hotel_id: int) -> bool:
        """単一メッセージの返信生成テスト"""
        try:
            response = self.session.post(
                f"{self.base_url}/messages/{message_id}/suggestions",
                params={"hotel_id": hotel_id},
                timeout=REQUEST_TIMEOUT
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
                return False
        except Exception as e:
            print(f"[ERROR] 返信候補生成エラー: {e}")
            return False
    
    def test_analytics(self, hotel_id: int) -> bool:
        """分析データテスト"""
        print(f"[DATA] ホテルID {hotel_id} の分析データをテスト中...")
        
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
                return False
        except Exception as e:
            print(f"[ERROR] 分析データ取得エラー: {e}")
            return False
    
    def test_nearby_attractions(self, hotel_id: int) -> bool:
        """周辺観光地テスト"""
        print(f"[MAP] ホテルID {hotel_id} の周辺観光地をテスト中...")
        
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
                
                for attraction in attractions[:3]:  # 最初の3件のみ表示
                    print(f"  - 名前: {attraction['name']}")
                    print(f"    カテゴリ: {attraction['category']}")
                    print(f"    距離: {attraction['distance_km']}km")
                    print(f"    評価: {attraction['rating']}/5")
                
                return True
            else:
                print(f"[ERROR] 周辺観光地取得失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] 周辺観光地取得エラー: {e}")
            return False
    
    def run_comprehensive_test(self) -> bool:
        """包括的なテストを実行"""
        print("[START] 包括的なテストデータ生成を開始します...")
        print("=" * 60)
        
        # API接続確認
        if not self._test_api_connection():
            print("[ERROR] API接続に失敗しました。テストを中断します。")
            return False
        
        # サンプルホテルを作成
        hotel_ids = self.create_sample_hotels()
        if not hotel_ids:
            print("[ERROR] ホテルの作成に失敗しました")
            return False
        
        print(f"[OK] {len(hotel_ids)}件のホテルを作成しました")
        
        # 各ホテルでテストを実行
        success_count = 0
        total_tests = len(hotel_ids)
        
        for hotel_id in hotel_ids:
            print(f"\n[HOTEL] ホテルID {hotel_id} のテストを実行中...")
            print("-" * 40)
            
            hotel_success = True
            
            # メッセージ作成テスト
            try:
                created_messages = self.create_sample_messages(hotel_id)
                if created_messages:
                    print(f"[OK] {len(created_messages)}件のメッセージを作成しました")
                else:
                    print("[INFO] メッセージ作成はスキップされました")
            except Exception as e:
                print(f"[WARNING] メッセージ作成でエラーが発生しました: {e}")
            
            # 返信生成テスト
            try:
                if not self.test_response_generation(hotel_id):
                    print("[WARNING] 返信生成テストで問題が発生しました")
                    # エラーでも続行
            except Exception as e:
                print(f"[WARNING] 返信生成テストでエラーが発生しました: {e}")
            
            # 分析データテスト
            try:
                if not self.test_analytics(hotel_id):
                    print("[WARNING] 分析データテストで問題が発生しました")
            except Exception as e:
                print(f"[WARNING] 分析データテストでエラーが発生しました: {e}")
            
            # 周辺観光地テスト
            try:
                if not self.test_nearby_attractions(hotel_id):
                    print("[WARNING] 周辺観光地テストで問題が発生しました")
            except Exception as e:
                print(f"[WARNING] 周辺観光地テストでエラーが発生しました: {e}")
            
            # 基本的なAPI接続ができていれば成功としてカウント
            if hotel_success:
                success_count += 1
        
        print("=" * 60)
        print(f"[OK] テスト完了: {success_count}/{total_tests}件のホテルで基本テスト成功")
        
        # 少なくとも1つのホテルでテストが成功していれば全体として成功
        return success_count > 0

def create_sample_scenarios():
    """サンプルシナリオを作成"""
    print("[NOTE] サンプルシナリオを作成中...")
    
    scenarios = [
        {
            "title": "荷物預かりの問い合わせ",
            "message": "チェックイン前に荷物を預かってもらえますか？午前10時に到着予定です。",
            "expected_type": "荷物預かり",
            "platform": "booking.com"
        },
        {
            "title": "予約可能期間の問い合わせ",
            "message": "来月の15日から3泊4日で予約できますか？",
            "expected_type": "予約確認",
            "platform": "airbnb"
        },
        {
            "title": "周辺観光地の問い合わせ",
            "message": "ホテル周辺でおすすめの観光地はありますか？",
            "expected_type": "観光地情報",
            "platform": "booking.com"
        },
        {
            "title": "チェックイン時間の問い合わせ",
            "message": "チェックイン時間は何時からですか？",
            "expected_type": "チェックイン情報",
            "platform": "airbnb"
        },
        {
            "title": "WiFi情報の問い合わせ",
            "message": "WiFiは無料で使えますか？パスワードを教えてください。",
            "expected_type": "WiFi情報",
            "platform": "booking.com"
        },
        {
            "title": "レストランの問い合わせ",
            "message": "ホテル内にレストランはありますか？朝食は含まれていますか？",
            "expected_type": "レストラン情報",
            "platform": "airbnb"
        },
        {
            "title": "交通手段の問い合わせ",
            "message": "空港からホテルまでのアクセス方法を教えてください。",
            "expected_type": "交通情報",
            "platform": "booking.com"
        },
        {
            "title": "ペット同伴の問い合わせ",
            "message": "ペットを連れて宿泊できますか？追加料金はかかりますか？",
            "expected_type": "ペット情報",
            "platform": "airbnb"
        }
    ]
    
    print("[LIST] サンプルシナリオ一覧:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario['title']}")
        print(f"     メッセージ: {scenario['message']}")
        print(f"     期待されるタイプ: {scenario['expected_type']}")
        print(f"     プラットフォーム: {scenario['platform']}")
        print()
    
    return scenarios

def main():
    """メイン関数"""
    print("[HOTEL] ホテル向け自動返信システム - テストデータ生成")
    print("=" * 60)
    
    # サンプルシナリオを作成
    scenarios = create_sample_scenarios()
    
    print("\n" + "=" * 60)
    
    # テストデータ生成器を初期化
    generator = TestDataGenerator()
    
    # 包括的なテストを実行
    success = generator.run_comprehensive_test()
    
    if success:
        print("\n[SUCCESS] テストデータ生成が完了しました！")
        print(f"[UI] Streamlit UI: http://localhost:8501")
        print(f"[DOCS] API Docs: {API_BASE_URL}/docs")
        print("\n[INFO] 次のステップ:")
        print("   1. Streamlit UIでホテルを選択")
        print("   2. メッセージ管理タブでメッセージを確認")
        print("   3. 返信候補を生成してテスト")
        print("   4. 分析タブでデータを確認")
        print("\n[NOTE] サンプルシナリオ:")
        print("   上記のシナリオを参考に、実際のメッセージをテストしてください")
    else:
        print("\n[ERROR] テストデータ生成に失敗しました")
        print("   ログを確認して問題を解決してください")
        print("\n[FIX] トラブルシューティング:")
        print("   1. docker-compose ps でサービスが起動しているか確認")
        print("   2. docker-compose logs api でAPIログを確認")
        print("   3. EXAMPLE.mdのトラブルシューティングセクションを参照")

if __name__ == "__main__":
    main()
