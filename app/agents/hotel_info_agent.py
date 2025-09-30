import googlemaps
import requests
from typing import List, Dict, Optional
from app.config import settings
from app.models import Hotel, NearbyAttraction
from sqlalchemy.orm import Session
import json

class HotelInfoAgent:
    def __init__(self):
        # Google Maps APIキーが設定されている場合のみクライアントを初期化
        if settings.GOOGLE_MAPS_API_KEY and settings.GOOGLE_MAPS_API_KEY != "your_google_maps_api_key_here":
            self.gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        else:
            self.gmaps = None
    
    def get_nearby_attractions(self, hotel_id: int, db: Session, radius: int = 2000) -> List[Dict]:
        """ホテル周辺の観光地・施設を取得"""
        try:
            # ホテル情報を取得
            hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
            if not hotel:
                return []
            
            # Google Maps APIキーが設定されていない場合はモックデータを返す
            if not self.gmaps or not settings.GOOGLE_MAPS_API_KEY or settings.GOOGLE_MAPS_API_KEY == "your_google_maps_api_key_here":
                return self._get_mock_attractions(hotel)
            
            try:
                # Google Places APIで周辺施設を検索
                places_result = self.gmaps.places_nearby(
                    location=(hotel.latitude, hotel.longitude),
                    radius=radius,
                    type=['tourist_attraction', 'restaurant', 'shopping_mall', 'park']
                )
                
                attractions = []
                for place in places_result.get('results', []):
                    attraction_data = {
                        'name': place.get('name'),
                        'category': self._categorize_place(place.get('types', [])),
                        'rating': place.get('rating', 0),
                        'address': place.get('vicinity'),
                        'latitude': place.get('geometry', {}).get('location', {}).get('lat'),
                        'longitude': place.get('geometry', {}).get('location', {}).get('lng'),
                        'distance_km': self._calculate_distance(
                            hotel.latitude, hotel.longitude,
                            place.get('geometry', {}).get('location', {}).get('lat'),
                            place.get('geometry', {}).get('location', {}).get('lng')
                        )
                    }
                    attractions.append(attraction_data)
                
                return attractions
            except Exception as e:
                # APIエラーが発生した場合はモックデータを返す
                print(f"Google Maps API エラー (観光地): {str(e)}")
                return self._get_mock_attractions(hotel)
        except Exception as e:
            # APIエラーが発生した場合はモックデータを返す
            print(f"Google Maps API エラー: {str(e)}")
            hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
            if hotel:
                return self._get_mock_attractions(hotel)
            return []
    
    def get_luggage_storage_info(self, hotel_id: int, db: Session) -> Dict:
        """荷物預かり情報を取得"""
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            return {}
        
        # Google Maps APIキーが設定されていない場合はモックデータを返す
        if not self.gmaps or not settings.GOOGLE_MAPS_API_KEY or settings.GOOGLE_MAPS_API_KEY == "your_google_maps_api_key_here":
            return self._get_mock_luggage_info(hotel)
        
        try:
            # ホテル周辺のコインロッカーや荷物預かりサービスを検索
            places_result = self.gmaps.places_nearby(
                location=(hotel.latitude, hotel.longitude),
                radius=1000,
                keyword='コインロッカー 荷物預かり'
            )
            
            storage_options = []
            for place in places_result.get('results', []):
                storage_options.append({
                    'name': place.get('name'),
                    'address': place.get('vicinity'),
                    'rating': place.get('rating', 0),
                    'distance_km': self._calculate_distance(
                        hotel.latitude, hotel.longitude,
                        place.get('geometry', {}).get('location', {}).get('lat'),
                        place.get('geometry', {}).get('location', {}).get('lng')
                    )
                })
            
            return {
                'hotel_name': hotel.name,
                'hotel_address': hotel.address,
                'storage_options': storage_options,
                'hotel_storage_available': True  # 仮の値、実際はホテルデータから取得
            }
        except Exception as e:
            # APIエラーが発生した場合はモックデータを返す
            print(f"Google Maps API エラー (荷物預かり): {str(e)}")
            return self._get_mock_luggage_info(hotel)
    
    def get_booking_availability(self, hotel_id: int, db: Session) -> Dict:
        """予約可能期間を取得"""
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            return {}
        
        # 実際の実装では、ホテルの予約システムAPIと連携
        # ここでは仮のデータを返す
        return {
            'hotel_name': hotel.name,
            'availability': {
                'next_30_days': 'limited',
                'next_90_days': 'available',
                'peak_season': '2024-07-15 to 2024-08-31',
                'off_season': '2024-09-01 to 2024-12-31'
            },
            'recommended_booking_window': '30-60 days in advance'
        }
    
    def _categorize_place(self, types: List[str]) -> str:
        """Google Placesのタイプを日本語カテゴリに変換"""
        type_mapping = {
            'tourist_attraction': '観光地',
            'restaurant': 'レストラン',
            'shopping_mall': 'ショッピング',
            'park': '公園',
            'museum': '博物館',
            'amusement_park': 'テーマパーク',
            'zoo': '動物園',
            'aquarium': '水族館'
        }
        
        for place_type in types:
            if place_type in type_mapping:
                return type_mapping[place_type]
        return 'その他'
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """2点間の距離を計算（km）"""
        from math import radians, cos, sin, asin, sqrt
        
        # Haversine formula
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Earth's radius in kilometers
        return round(c * r, 2)
    
    def _get_mock_attractions(self, hotel) -> List[Dict]:
        """モック観光地データを生成"""
        # ホテルの都市に応じて観光地を生成
        city_attractions = {
            '東京': [
                {'name': '東京スカイツリー', 'category': '観光地', 'rating': 4.5, 'distance_km': 1.2},
                {'name': '浅草寺', 'category': '観光地', 'rating': 4.3, 'distance_km': 0.8},
                {'name': '上野公園', 'category': '公園', 'rating': 4.2, 'distance_km': 2.1},
                {'name': '築地市場', 'category': '市場', 'rating': 4.0, 'distance_km': 1.5},
                {'name': '銀座', 'category': 'ショッピング', 'rating': 4.4, 'distance_km': 2.8}
            ],
            '大阪': [
                {'name': '大阪城', 'category': '観光地', 'rating': 4.3, 'distance_km': 1.5},
                {'name': '道頓堀', 'category': '観光地', 'rating': 4.2, 'distance_km': 0.9},
                {'name': '通天閣', 'category': '観光地', 'rating': 4.1, 'distance_km': 1.8},
                {'name': '心斎橋', 'category': 'ショッピング', 'rating': 4.0, 'distance_km': 1.2},
                {'name': '大阪海遊館', 'category': '水族館', 'rating': 4.4, 'distance_km': 3.2}
            ],
            '京都': [
                {'name': '清水寺', 'category': '観光地', 'rating': 4.5, 'distance_km': 2.1},
                {'name': '金閣寺', 'category': '観光地', 'rating': 4.4, 'distance_km': 3.5},
                {'name': '嵐山', 'category': '観光地', 'rating': 4.3, 'distance_km': 5.2},
                {'name': '伏見稲荷大社', 'category': '観光地', 'rating': 4.2, 'distance_km': 4.8},
                {'name': '祇園', 'category': '観光地', 'rating': 4.1, 'distance_km': 1.8}
            ],
            '横浜': [
                {'name': '横浜中華街', 'category': '観光地', 'rating': 4.2, 'distance_km': 1.8},
                {'name': 'みなとみらい', 'category': '観光地', 'rating': 4.3, 'distance_km': 2.5},
                {'name': '横浜ランドマークタワー', 'category': '観光地', 'rating': 4.1, 'distance_km': 2.2},
                {'name': '山下公園', 'category': '公園', 'rating': 4.0, 'distance_km': 1.5},
                {'name': '横浜コスモワールド', 'category': 'テーマパーク', 'rating': 4.2, 'distance_km': 3.1}
            ],
            '福岡': [
                {'name': '博多駅', 'category': '観光地', 'rating': 4.0, 'distance_km': 0.5},
                {'name': '天神', 'category': 'ショッピング', 'rating': 4.2, 'distance_km': 1.2},
                {'name': '太宰府天満宮', 'category': '観光地', 'rating': 4.3, 'distance_km': 8.5},
                {'name': '福岡城跡', 'category': '観光地', 'rating': 4.1, 'distance_km': 2.8},
                {'name': '福岡市博物館', 'category': '博物館', 'rating': 4.0, 'distance_km': 3.2}
            ]
        }
        
        # デフォルトの観光地
        default_attractions = [
            {'name': '近くの公園', 'category': '公園', 'rating': 4.0, 'distance_km': 0.8},
            {'name': '地元レストラン', 'category': 'レストラン', 'rating': 4.1, 'distance_km': 0.5},
            {'name': 'ショッピングセンター', 'category': 'ショッピング', 'rating': 4.2, 'distance_km': 1.2},
            {'name': '観光スポット', 'category': '観光地', 'rating': 4.3, 'distance_km': 1.5},
            {'name': '博物館', 'category': '博物館', 'rating': 4.0, 'distance_km': 2.1}
        ]
        
        # ホテルの都市に応じた観光地を取得、なければデフォルトを使用
        attractions = city_attractions.get(hotel.city, default_attractions)
        
        # 各観光地に住所を追加
        for attraction in attractions:
            attraction['address'] = f"{hotel.city}市{attraction['name']}周辺"
            attraction['latitude'] = hotel.latitude + (attraction['distance_km'] * 0.01)  # 仮の座標
            attraction['longitude'] = hotel.longitude + (attraction['distance_km'] * 0.01)
        
        return attractions[:5]  # 最大5件まで返す
    
    def _get_mock_luggage_info(self, hotel) -> Dict:
        """モック荷物預かり情報を生成"""
        # ホテルの都市に応じて荷物預かりオプションを生成
        city_storage_options = {
            '東京': [
                {'name': 'JR東京駅コインロッカー', 'address': 'JR東京駅内', 'rating': 4.2, 'distance_km': 0.8},
                {'name': '渋谷駅コインロッカー', 'address': 'JR渋谷駅内', 'rating': 4.0, 'distance_km': 1.2},
                {'name': '新宿駅コインロッカー', 'address': 'JR新宿駅内', 'rating': 4.1, 'distance_km': 1.5}
            ],
            '大阪': [
                {'name': 'JR大阪駅コインロッカー', 'address': 'JR大阪駅内', 'rating': 4.3, 'distance_km': 0.9},
                {'name': '難波駅コインロッカー', 'address': '南海難波駅内', 'rating': 4.1, 'distance_km': 1.1},
                {'name': '梅田駅コインロッカー', 'address': '阪急梅田駅内', 'rating': 4.2, 'distance_km': 1.3}
            ],
            '京都': [
                {'name': 'JR京都駅コインロッカー', 'address': 'JR京都駅内', 'rating': 4.4, 'distance_km': 1.0},
                {'name': '祇園四条駅コインロッカー', 'address': '京阪祇園四条駅内', 'rating': 4.0, 'distance_km': 1.8},
                {'name': '河原町駅コインロッカー', 'address': '阪急河原町駅内', 'rating': 4.1, 'distance_km': 2.0}
            ],
            '横浜': [
                {'name': 'JR横浜駅コインロッカー', 'address': 'JR横浜駅内', 'rating': 4.2, 'distance_km': 1.2},
                {'name': 'みなとみらい駅コインロッカー', 'address': 'みなとみらい線内', 'rating': 4.0, 'distance_km': 2.5},
                {'name': '関内駅コインロッカー', 'address': 'JR関内駅内', 'rating': 4.1, 'distance_km': 1.8}
            ],
            '福岡': [
                {'name': 'JR博多駅コインロッカー', 'address': 'JR博多駅内', 'rating': 4.3, 'distance_km': 0.5},
                {'name': '天神駅コインロッカー', 'address': '地下鉄天神駅内', 'rating': 4.1, 'distance_km': 1.2},
                {'name': '中洲川端駅コインロッカー', 'address': '地下鉄中洲川端駅内', 'rating': 4.0, 'distance_km': 1.5}
            ]
        }
        
        # デフォルトの荷物預かりオプション
        default_storage_options = [
            {'name': '最寄り駅コインロッカー', 'address': '最寄り駅内', 'rating': 4.0, 'distance_km': 0.8},
            {'name': '近隣コンビニエンスストア', 'address': '近隣コンビニ', 'rating': 3.8, 'distance_km': 0.5},
            {'name': '地元荷物預かりサービス', 'address': '地元サービス', 'rating': 4.1, 'distance_km': 1.0}
        ]
        
        # ホテルの都市に応じた荷物預かりオプションを取得、なければデフォルトを使用
        storage_options = city_storage_options.get(hotel.city, default_storage_options)
        
        return {
            'hotel_name': hotel.name,
            'hotel_address': hotel.address,
            'storage_options': storage_options,
            'hotel_storage_available': True
        }