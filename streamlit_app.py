import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

# ページ設定
st.set_page_config(
    page_title="ホテル返信システム",
    page_icon="🏨",
    layout="wide"
)

# APIベースURL
import os
# ローカル開発時は localhost:8000、Docker環境では api:8000 を使用
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# デバッグ情報を表示
if st.sidebar.checkbox("デバッグ情報を表示"):
    st.sidebar.write(f"API_BASE_URL: {API_BASE_URL}")
    st.sidebar.write(f"Environment: {os.getenv('ENV', 'development')}")

# セッション状態の初期化
if 'selected_hotel' not in st.session_state:
    st.session_state.selected_hotel = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

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

def test_api_connection() -> bool:
    """API接続をテスト"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True
        else:
            display_error_with_details(response, "API接続テスト")
            return False
    except requests.exceptions.Timeout:
        st.error("API接続タイムアウト - サーバーが起動していない可能性があります")
        return False
    except requests.exceptions.ConnectionError:
        st.error("API接続エラー - サーバーに接続できません")
        st.error(f"接続先URL: {API_BASE_URL}")
        return False
    except Exception as e:
        st.error(f"API接続エラー: {str(e)}")
        return False

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

def main():
    st.title("🏨 ホテル返信システム")
    st.markdown("---")
    
    # API接続テスト
    if not test_api_connection():
        st.error("APIサーバーに接続できません。以下を確認してください：")
        st.write("1. Dockerサービスが起動しているか確認")
        st.write("2. APIサーバーが正常に動作しているか確認")
        st.write("3. ネットワーク設定を確認")
        return
    
    # サイドバー
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
                
                # 新しいメッセージを取得
                if st.button("新しいメッセージを取得", type="primary"):
                    with st.spinner("メッセージを取得中..."):
                        try:
                            result = requests.post(f"{API_BASE_URL}/messages/fetch/{hotel['id']}", timeout=30)
                            if result.status_code == 200:
                                st.success("メッセージを取得しました")
                                st.rerun()
                            else:
                                display_error_with_details(result, "メッセージの取得")
                        except requests.exceptions.Timeout:
                            st.error("メッセージ取得タイムアウト")
                        except Exception as e:
                            st.error(f"エラー: {str(e)}")
        else:
            st.warning("ホテルが見つかりません。まずホテルを登録してください。")
    
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