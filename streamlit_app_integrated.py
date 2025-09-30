import streamlit as st
import requests
import json
import os
import sys
import subprocess
import threading
import time
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random

# ページ設定
st.set_page_config(
    page_title="ホテル返信システム",
    page_icon="🏨",
    layout="wide"
)

# APIベースURL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# セッション状態の初期化
if 'selected_hotel' not in st.session_state:
    st.session_state.selected_hotel = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []
if 'api_server_started' not in st.session_state:
    st.session_state.api_server_started = False
if 'database_initialized' not in st.session_state:
    st.session_state.database_initialized = False

# =============================================================================
# データベース管理機能
# =============================================================================

def init_database():
    """データベースを初期化"""
    try:
        # SQLiteデータベースを作成
        conn = sqlite3.connect('hotel_agent.db')
        cursor = conn.cursor()
        
        # テーブルを作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id TEXT UNIQUE,
                hotel_id INTEGER NOT NULL,
                guest_name TEXT,
                check_in TIMESTAMP,
                check_out TIMESTAMP,
                room_type TEXT,
                guest_count INTEGER,
                booking_reference TEXT UNIQUE,
                total_amount REAL,
                status TEXT DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hotel_id) REFERENCES hotels (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guest_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER,
                platform TEXT NOT NULL,
                message_content TEXT NOT NULL,
                message_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_processed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (booking_id) REFERENCES bookings (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS response_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hotel_id INTEGER NOT NULL,
                message_type TEXT NOT NULL,
                template_content TEXT NOT NULL,
                language TEXT DEFAULT 'ja',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hotel_id) REFERENCES hotels (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        st.session_state.database_initialized = True
        return True
    except Exception as e:
        st.error(f"データベース初期化エラー: {str(e)}")
        return False

def create_sample_data():
    """サンプルデータを作成"""
    try:
        conn = sqlite3.connect('hotel_agent.db')
        cursor = conn.cursor()
        
        # ホテルデータを作成
        hotels_data = [
            ("東京グランドホテル", "東京都千代田区丸の内1-1-1", 35.6762, 139.6503, "東京", "日本"),
            ("大阪ビジネスホテル", "大阪府大阪市北区梅田1-1-1", 34.6937, 135.5023, "大阪", "日本"),
            ("京都伝統旅館", "京都府京都市下京区四条通烏丸西入ル", 35.0116, 135.7681, "京都", "日本")
        ]
        
        hotel_ids = []
        for hotel_data in hotels_data:
            cursor.execute('''
                INSERT OR IGNORE INTO hotels (name, address, latitude, longitude, city, country)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', hotel_data)
            hotel_id = cursor.lastrowid
            if hotel_id == 0:  # 既に存在する場合
                cursor.execute('SELECT id FROM hotels WHERE name = ?', (hotel_data[0],))
                hotel_id = cursor.fetchone()[0]
            hotel_ids.append(hotel_id)
        
        # 予約データを作成
        for hotel_id in hotel_ids:
            for i in range(5):
                check_in = datetime.now() + timedelta(days=random.randint(-30, 30))
                check_out = check_in + timedelta(days=random.randint(1, 7))
                
                cursor.execute('''
                    INSERT OR IGNORE INTO bookings 
                    (hotel_id, guest_name, check_in, check_out, room_type, guest_count, booking_reference, total_amount, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    hotel_id,
                    f"ゲスト{i+1}",
                    check_in.isoformat(),
                    check_out.isoformat(),
                    random.choice(["シングル", "ダブル", "ツイン", "スイート"]),
                    random.randint(1, 4),
                    f"REF{hotel_id:03d}{i+1:03d}",
                    random.randint(8000, 15000),
                    random.choice(["confirmed", "cancelled", "completed"])
                ))
        
        # テンプレートデータを作成
        templates_data = [
            ("luggage", "お荷物の預かりサービスをご利用いただけます。フロントデスクまでお越しください。"),
            ("luggage", "チェックイン前・チェックアウト後もお荷物をお預かりいたします。"),
            ("availability", "空室状況をお調べいたします。ご希望の日程をお教えください。"),
            ("availability", "ご予約可能な期間をご案内いたします。お急ぎの場合はお電話にてお問い合わせください。"),
            ("attractions", "周辺の観光地をご案内いたします。おすすめスポットをご紹介いたします。"),
            ("attractions", "ホテル周辺の観光情報をお調べいたします。アクセス方法もご案内いたします。")
        ]
        
        for hotel_id in hotel_ids:
            for template_type, template_content in templates_data:
                cursor.execute('''
                    INSERT OR IGNORE INTO response_templates 
                    (hotel_id, message_type, template_content, language, is_active)
                    VALUES (?, ?, ?, ?, ?)
                ''', (hotel_id, template_type, template_content, "ja", True))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"サンプルデータ作成エラー: {str(e)}")
        return False

# =============================================================================
# FastAPIサーバー管理機能
# =============================================================================

def start_api_server():
    """FastAPIサーバーを起動"""
    if st.session_state.api_server_started:
        return True
    
    try:
        # FastAPIサーバーをバックグラウンドで起動
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 少し待機してサーバーが起動するのを待つ
        time.sleep(3)
        
        # サーバーが起動しているかチェック
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.session_state.api_server_started = True
                return True
        except:
            pass
        
        return False
    except Exception as e:
        st.error(f"APIサーバー起動エラー: {str(e)}")
        return False

def check_api_connection():
    """API接続をチェック"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# =============================================================================
# エラーハンドリング機能
# =============================================================================

def parse_error_response(response: requests.Response) -> str:
    """APIエラーレスポンスからエラーメッセージを抽出"""
    try:
        error_data = response.json()
        
        # HTTPValidationErrorの場合
        if 'detail' in error_data:
            detail = error_data['detail']
            if isinstance(detail, list) and len(detail) > 0:
                error_items = []
                for item in detail:
                    if isinstance(item, dict) and 'msg' in item:
                        error_items.append(item['msg'])
                        # エラーの場所も含める
                        if 'loc' in item and item['loc']:
                            location = ' -> '.join(map(str, item['loc']))
                            error_items[-1] += f" (場所: {location})"
                return '\n'.join(error_items)
            elif isinstance(detail, str):
                return detail
        
        # ValidationErrorの場合
        if 'msg' in error_data:
            msg = error_data['msg']
            if 'loc' in error_data and error_data['loc']:
                location = ' -> '.join(map(str, error_data['loc']))
                return f"{msg} (場所: {location})"
            return msg
        
        # その他のエラー
        if 'message' in error_data:
            return error_data['message']
        if 'error' in error_data:
            return error_data['error']
        
        # JSONパースは成功したが、予期しない構造
        return f"予期しないエラーレスポンス形式: {json.dumps(error_data, ensure_ascii=False, indent=2)}"
        
    except json.JSONDecodeError:
        # JSONパースに失敗した場合
        return f"エラーレスポンスの解析に失敗しました。レスポンス: {response.text[:500]}"
    except Exception as e:
        return f"エラーメッセージの抽出中にエラーが発生しました: {str(e)}"

def display_error_with_details(response: requests.Response, operation: str):
    """詳細なエラー情報を表示"""
    error_message = parse_error_response(response)
    
    st.error(f"{operation}に失敗しました")
    st.error(f"HTTPステータス: {response.status_code}")
    st.error(f"エラーメッセージ: {error_message}")
    
    # デバッグ情報を表示（デバッグモードが有効な場合）
    if st.sidebar.checkbox("デバッグ情報を表示"):
        with st.expander(f"詳細なエラー情報 ({operation})"):
            st.code(f"ステータスコード: {response.status_code}")
            st.code(f"レスポンスヘッダー: {dict(response.headers)}")
            st.code(f"レスポンス本文: {response.text}")

# =============================================================================
# API呼び出し機能
# =============================================================================

def fetch_hotels() -> List[Dict]:
    """ホテル一覧を取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/hotels", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            display_error_with_details(response, "ホテル一覧の取得")
            return []
    except requests.exceptions.Timeout:
        st.error("API接続タイムアウト - サーバーが起動していない可能性があります")
        return []
    except requests.exceptions.ConnectionError:
        st.error("API接続エラー - サーバーに接続できません")
        st.error(f"接続先URL: {API_BASE_URL}")
        return []
    except Exception as e:
        st.error(f"API接続エラー: {str(e)}")
        return []

def fetch_messages(hotel_id: int) -> List[Dict]:
    """メッセージ一覧を取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/messages/{hotel_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            display_error_with_details(response, "メッセージの取得")
            return []
    except requests.exceptions.Timeout:
        st.error("API接続タイムアウト")
        return []
    except requests.exceptions.ConnectionError:
        st.error("API接続エラー")
        return []
    except Exception as e:
        st.error(f"API接続エラー: {str(e)}")
        return []

def fetch_response_suggestions(message_id: int, hotel_id: int) -> Dict:
    """返信候補を取得"""
    try:
        response = requests.post(f"{API_BASE_URL}/messages/{message_id}/suggestions", 
                               params={"hotel_id": hotel_id}, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            display_error_with_details(response, "返信候補の取得")
            return {}
    except requests.exceptions.Timeout:
        st.error("返信候補生成タイムアウト - 処理に時間がかかっています")
        return {}
    except requests.exceptions.ConnectionError:
        st.error("API接続エラー")
        return {}
    except Exception as e:
        st.error(f"API接続エラー: {str(e)}")
        return {}

def send_response(message_id: int, response_content: str, platform: str) -> Dict:
    """返信を送信"""
    try:
        response = requests.post(f"{API_BASE_URL}/messages/{message_id}/respond",
                               params={
                                   "response_content": response_content,
                                   "platform": platform
                               }, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            display_error_with_details(response, "返信の送信")
            return {}
    except requests.exceptions.Timeout:
        st.error("返信送信タイムアウト")
        return {}
    except requests.exceptions.ConnectionError:
        st.error("API接続エラー")
        return {}
    except Exception as e:
        st.error(f"API接続エラー: {str(e)}")
        return {}

# =============================================================================
# メインアプリケーション
# =============================================================================

def main():
    st.title("🏨 ホテル返信システム")
    st.markdown("---")
    
    # サイドバーでシステム状態を表示
    with st.sidebar:
        st.header("システム状態")
        
        # データベース状態
        if st.session_state.database_initialized:
            st.success("✅ データベース初期化済み")
        else:
            st.warning("⚠️ データベース未初期化")
        
        # APIサーバー状態
        if st.session_state.api_server_started:
            st.success("✅ APIサーバー起動済み")
        else:
            st.warning("⚠️ APIサーバー未起動")
        
        # 初期化ボタン
        if not st.session_state.database_initialized:
            if st.button("データベースを初期化", type="primary"):
                with st.spinner("データベースを初期化中..."):
                    if init_database():
                        st.success("データベース初期化完了")
                        st.rerun()
                    else:
                        st.error("データベース初期化失敗")
        
        if not st.session_state.api_server_started:
            if st.button("APIサーバーを起動", type="primary"):
                with st.spinner("APIサーバーを起動中..."):
                    if start_api_server():
                        st.success("APIサーバー起動完了")
                        st.rerun()
                    else:
                        st.error("APIサーバー起動失敗")
        
        # サンプルデータ作成ボタン
        if st.session_state.database_initialized:
            if st.button("サンプルデータを作成"):
                with st.spinner("サンプルデータを作成中..."):
                    if create_sample_data():
                        st.success("サンプルデータ作成完了")
                        st.rerun()
                    else:
                        st.error("サンプルデータ作成失敗")
        
        # デバッグ情報を表示
        if st.checkbox("デバッグ情報を表示"):
            st.write(f"API_BASE_URL: {API_BASE_URL}")
            st.write(f"Environment: {os.getenv('ENV', 'development')}")
            st.write(f"Database initialized: {st.session_state.database_initialized}")
            st.write(f"API server started: {st.session_state.api_server_started}")
    
    # API接続テスト
    if not check_api_connection():
        st.error("APIサーバーに接続できません。以下を確認してください：")
        st.write("1. サイドバーの「APIサーバーを起動」ボタンをクリック")
        st.write("2. データベースが初期化されているか確認")
        st.write("3. ネットワーク設定を確認")
        return
    
    # ホテル選択
    with st.sidebar:
        st.header("ホテル選択")
        
        # ホテル一覧を取得
        hotels = fetch_hotels()
        
        if hotels:
            hotel_options = {f"{hotel['name']} ({hotel['city']})": hotel for hotel in hotels}
            selected_hotel_name = st.selectbox(
                "ホテルを選択してください",
                options=list(hotel_options.keys()),
                index=0 if not st.session_state.selected_hotel else None
            )
            
            if selected_hotel_name:
                st.session_state.selected_hotel = hotel_options[selected_hotel_name]
                
                # ホテル情報を表示
                hotel = st.session_state.selected_hotel
                st.subheader("ホテル情報")
                st.write(f"**名前:** {hotel['name']}")
                st.write(f"**住所:** {hotel['address']}")
                st.write(f"**都市:** {hotel['city']}")
                st.write(f"**国:** {hotel['country']}")
        else:
            st.warning("ホテルが見つかりません。サンプルデータを作成してください。")
    
    # メインコンテンツ
    if st.session_state.selected_hotel:
        hotel = st.session_state.selected_hotel
        
        # タブを作成
        tab1, tab2, tab3 = st.tabs(["📨 メッセージ管理", "📊 分析", "🏨 ホテル情報"])
        
        with tab1:
            st.header("メッセージ管理")
            
            # メッセージ一覧を取得
            messages = fetch_messages(hotel['id'])
            
            if messages:
                st.subheader(f"未処理メッセージ ({len([m for m in messages if not m['is_processed']])}件)")
                
                for message in messages:
                    if not message['is_processed']:
                        with st.expander(f"📩 {message['platform']} - {message['message_content'][:50]}..."):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**メッセージ:** {message['message_content']}")
                                st.write(f"**プラットフォーム:** {message['platform']}")
                                st.write(f"**受信時刻:** {message['timestamp']}")
                                st.write(f"**メッセージタイプ:** {message['message_type']}")
                            
                            with col2:
                                if st.button(f"返信候補を取得", key=f"suggest_{message['id']}"):
                                    with st.spinner("返信候補を生成中..."):
                                        suggestions_data = fetch_response_suggestions(message['id'], hotel['id'])
                                        st.session_state.suggestions = suggestions_data.get('suggestions', [])
                                        st.session_state.current_message = message
                                
                                # 返信候補を表示
                                if st.session_state.suggestions and st.session_state.current_message['id'] == message['id']:
                                    st.subheader("返信候補")
                                    
                                    for i, suggestion in enumerate(st.session_state.suggestions):
                                        st.write(f"**候補 {i+1}:**")
                                        
                                        # 返信内容を表示
                                        st.write(suggestion['content'])
                                        
                                        # 信頼度とタイプを表示
                                        col_info1, col_info2, col_info3 = st.columns(3)
                                        with col_info1:
                                            st.write(f"*信頼度: {suggestion['confidence']:.2f}*")
                                        with col_info2:
                                            st.write(f"*タイプ: {suggestion['type']}*")
                                        with col_info3:
                                            st.write(f"*根拠: {suggestion['source']}*")
                                        
                                        # 根拠ソースの詳細説明
                                        with st.expander(f"根拠ソースの詳細 (候補 {i+1})"):
                                            source_explanations = {
                                                'Hotel Service Info': 'ホテルの公式サービス情報に基づく回答',
                                                'Standard Response': '一般的なホテル業界の標準的な回答',
                                                'Personalized Service': 'お客様の個別のご要望に応じた回答',
                                                'Nearby Options': 'ホテル周辺の施設情報に基づく回答',
                                                'Availability Data': '実際の予約データに基づく回答',
                                                'Booking Encouragement': '予約促進を目的とした回答',
                                                'Information Service': '情報提供サービスに基づく回答',
                                                'Local Knowledge': '地元の知識に基づく回答',
                                                'General Response': '一般的な対応に基づく回答',
                                                'Acknowledgment': 'お客様のご要望の確認に基づく回答',
                                                'Service Commitment': 'サービス提供へのコミットメントに基づく回答'
                                            }
                                            explanation = source_explanations.get(suggestion['source'], 'システムが生成した回答')
                                            st.write(f"**{suggestion['source']}**: {explanation}")
                                        
                                        if st.button(f"この候補で返信", key=f"send_{message['id']}_{i}"):
                                            with st.spinner("返信を送信中..."):
                                                result = send_response(
                                                    message['id'],
                                                    suggestion['content'],
                                                    message['platform']
                                                )
                                                
                                                if result.get('result', {}).get('success'):
                                                    st.success("返信を送信しました！")
                                                    st.rerun()
                                                else:
                                                    st.error("返信の送信に失敗しました")
                                        
                                        st.markdown("---")
            else:
                st.info("新しいメッセージはありません")
        
        with tab2:
            st.header("分析データ")
            
            if st.button("分析データを更新"):
                with st.spinner("分析データを取得中..."):
                    try:
                        response = requests.get(f"{API_BASE_URL}/hotels/{hotel['id']}/analytics", timeout=15)
                        if response.status_code == 200:
                            analytics = response.json()
                            
                            st.subheader("予約分析")
                            booking_analysis = analytics.get('booking_analysis', {})
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("総予約数", booking_analysis.get('total_bookings', 0))
                            with col2:
                                st.metric("平均滞在日数", f"{booking_analysis.get('average_stay_duration', 0):.1f}日")
                            with col3:
                                st.metric("平均宿泊人数", f"{booking_analysis.get('average_guest_count', 0):.1f}人")
                            
                            st.subheader("人気の部屋タイプ")
                            room_types = booking_analysis.get('popular_room_types', {})
                            if room_types:
                                for room_type, count in room_types.items():
                                    st.write(f"**{room_type}:** {count}件")
                            
                            st.subheader("学習結果")
                            learning_result = analytics.get('learning_result', {})
                            st.write(f"処理済みメッセージ: {learning_result.get('messages_processed', 0)}件")
                            st.write(f"処理済み返信: {learning_result.get('responses_processed', 0)}件")
                            st.write(f"読み込み済みテンプレート: {learning_result.get('templates_loaded', 0)}件")
                        else:
                            display_error_with_details(response, "分析データの取得")
                    except requests.exceptions.Timeout:
                        st.error("分析データ取得タイムアウト")
                    except Exception as e:
                        st.error(f"エラー: {str(e)}")
        
        with tab3:
            st.header("ホテル情報")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("周辺観光地")
                if st.button("観光地情報を取得"):
                    with st.spinner("観光地情報を取得中..."):
                        try:
                            response = requests.get(f"{API_BASE_URL}/hotels/{hotel['id']}/nearby-attractions", timeout=15)
                            if response.status_code == 200:
                                attractions_data = response.json()
                                attractions = attractions_data.get('attractions', [])
                                
                                for attraction in attractions:
                                    st.write(f"**{attraction['name']}**")
                                    st.write(f"カテゴリ: {attraction['category']}")
                                    st.write(f"距離: {attraction['distance_km']}km")
                                    st.write(f"評価: {attraction['rating']}/5")
                                    st.write(f"住所: {attraction['address']}")
                                    st.markdown("---")
                            else:
                                display_error_with_details(response, "観光地情報の取得")
                        except requests.exceptions.Timeout:
                            st.error("観光地情報取得タイムアウト")
                        except Exception as e:
                            st.error(f"エラー: {str(e)}")
            
            with col2:
                st.subheader("ホテル詳細")
                st.write(f"**ホテル名:** {hotel['name']}")
                st.write(f"**住所:** {hotel['address']}")
                st.write(f"**都市:** {hotel['city']}")
                st.write(f"**国:** {hotel['country']}")
    
    else:
        st.info("サイドバーからホテルを選択してください")

if __name__ == "__main__":
    main()
