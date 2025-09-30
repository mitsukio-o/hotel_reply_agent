# ホテル向け自動返信システム - 使用例

このドキュメントでは、ホテル向け自動返信システムの具体的な使用方法と実際のシナリオを詳しく説明します。

## 📋 目次

1. [システム概要](#システム概要)
2. [セットアップ手順](#セットアップ手順)
3. [基本的な使用例](#基本的な使用例)
4. [実際のシナリオ例](#実際のシナリオ例)
5. [API使用例](#api使用例)
6. [トラブルシューティング](#トラブルシューティング)

## 🏨 システム概要

このシステムは、Booking.comやAirbnbなどのプラットフォームからのゲストメッセージに対して、AIを活用した自動返信候補を生成し、ワンクリックで返信できるシステムです。

### 主要機能
- **マルチエージェントシステム**: ホテル周辺情報検索エージェントと予約データ学習エージェント
- **自動返信候補生成**: メッセージ内容に基づいて3つの返信候補を自動生成
- **ワンクリック返信**: 選択した候補で即座にプラットフォームに返信
- **リアルタイムメッセージ取得**: Booking.com/Airbnb APIから新しいメッセージを自動取得
- **学習機能**: 過去の対応ログから学習し、返信品質を向上

## 🚀 セットアップ手順

### 1. 環境変数の設定

`.env`ファイルを作成し、必要なAPIキーを設定してください：

```bash
# OpenAI APIキー（必須）
OPENAI_API_KEY=sk-your-openai-api-key-here

# Google Maps APIキー（必須）
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Booking.com APIキー（オプション）
BOOKING_API_KEY=your-booking-api-key-here

# Airbnb APIキー（オプション）
AIRBNB_API_KEY=your-airbnb-api-key-here

# データベース設定
DATABASE_URL=postgresql://postgres:password@localhost:5432/hotel_agent_db

# Redis設定
REDIS_URL=redis://localhost:6379/0

# アプリケーション設定
APP_NAME=Hotel Response Agent
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 2. Docker Composeを使用した起動

```bash
# アプリケーションを起動
docker-compose up -d

# ログを確認
docker-compose logs -f

# アプリケーションを停止
docker-compose down
```

### 3. 手動セットアップ

```bash
# 依存関係をインストール
pip install -r requirements.txt

# データベースを初期化
python -c "from app.database import create_tables; create_tables()"

# サンプルデータを投入
python app/seed_data.py

# FastAPIサーバーを起動
python -m uvicorn app.main:app --reload

# 別のターミナルでStreamlitを起動
streamlit run streamlit_app.py
```

## 📱 基本的な使用例

### 1. Webインターフェースにアクセス

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs

### 2. ホテル登録

Streamlit UIで「ホテル選択」セクションを使用して新しいホテルを登録：

```python
# API経由でホテルを登録
import requests

hotel_data = {
    "name": "サンプルホテル",
    "address": "東京都渋谷区道玄坂1-2-3",
    "latitude": 35.6581,
    "longitude": 139.7016,
    "city": "東京",
    "country": "日本"
}

response = requests.post("http://localhost:8000/hotels", params=hotel_data)
print(response.json())
```

### 3. メッセージ管理

1. 「メッセージ管理」タブで新しいメッセージを取得
2. 未処理メッセージの「返信候補を取得」をクリック
3. 生成された3つの候補から選択
4. 「この候補で返信」をクリックして送信

## 🎯 実際のシナリオ例

### シナリオ1: 荷物預かりの問い合わせ

**ゲストメッセージ:**
```
「チェックイン前に荷物を預かってもらえますか？午前10時に到着予定です。」
```

**システムの処理:**
1. メッセージタイプを「荷物預かり」として分類
2. ホテル周辺情報エージェントが荷物預かりサービスを検索
3. 予約データ学習エージェントが過去の類似対応を分析
4. 3つの返信候補を生成

**生成される返信候補:**

**候補1（高信頼度）:**
```
お客様、お疲れ様です。

チェックイン前の荷物預かりサービスをご利用いただけます。
午前10時にお越しいただき、フロントデスクまでお声がけください。
荷物は安全に保管させていただきます。

チェックイン時間は15:00からとなっております。
ご不明な点がございましたら、お気軽にお声がけください。

お待ちしております。
```

**候補2（中信頼度）:**
```
こんにちは。

荷物預かりサービスは承っております。
午前10時にお越しいただき、フロントデスクでお預かりいたします。
チェックイン時間（15:00）まで安全に保管いたします。

ご質問がございましたら、お気軽にお声がけください。
```

**候補3（低信頼度）:**
```
お客様

荷物預かりは可能です。
フロントデスクまでお越しください。
```

### シナリオ2: 予約可能期間の問い合わせ

**ゲストメッセージ:**
```
「来月の15日から3泊4日で予約できますか？」
```

**システムの処理:**
1. メッセージタイプを「予約確認」として分類
2. 予約データ学習エージェントが過去の予約パターンを分析
3. ホテル周辺情報エージェントが観光地情報を取得
4. 3つの返信候補を生成

**生成される返信候補:**

**候補1（高信頼度）:**
```
お客様、お疲れ様です。

来月15日から3泊4日のご予約についてお調べいたします。
現在、その期間の空室状況を確認いたします。

お近くには以下の観光地がございます：
- 浅草寺（徒歩10分）
- 東京スカイツリー（電車で15分）
- 上野公園（電車で20分）

詳細な空室状況と料金については、改めてご連絡いたします。
お急ぎの場合は、お電話でもお問い合わせください。

お待ちしております。
```

### シナリオ3: 周辺観光地の問い合わせ

**ゲストメッセージ:**
```
「ホテル周辺でおすすめの観光地はありますか？」
```

**システムの処理:**
1. メッセージタイプを「観光地情報」として分類
2. ホテル周辺情報エージェントがGoogle Maps APIを使用して周辺観光地を検索
3. 過去の対応ログから人気の観光地を分析
4. 3つの返信候補を生成

**生成される返信候補:**

**候補1（高信頼度）:**
```
お客様、お疲れ様です。

ホテル周辺のおすすめ観光地をご案内いたします：

【徒歩圏内】
・浅草寺（徒歩10分）- 東京の代表的な観光地
・浅草花やしき（徒歩15分）- 日本最古の遊園地

【電車で15分以内】
・東京スカイツリー（電車で10分）- 東京の新名所
・上野公園（電車で15分）- 博物館・美術館が充実

【電車で30分以内】
・皇居（電車で25分）- 東京の中心部
・銀座（電車で20分）- ショッピングエリア

各観光地の詳細情報やアクセス方法については、フロントデスクでもご案内いたします。
お気軽にお声がけください。
```

## 🔧 API使用例

### 1. ホテル一覧取得

```python
import requests

# ホテル一覧を取得
response = requests.get("http://localhost:8000/hotels")
hotels = response.json()

for hotel in hotels:
    print(f"ID: {hotel['id']}, 名前: {hotel['name']}, 都市: {hotel['city']}")
```

### 2. メッセージ取得

```python
# 特定のホテルのメッセージを取得
hotel_id = 1
response = requests.get(f"http://localhost:8000/messages/{hotel_id}")
messages = response.json()

for message in messages:
    print(f"プラットフォーム: {message['platform']}")
    print(f"メッセージ: {message['message_content']}")
    print(f"処理済み: {message['is_processed']}")
    print("---")
```

### 3. 返信候補生成

```python
# メッセージに対する返信候補を取得
message_id = 1
hotel_id = 1

response = requests.post(
    f"http://localhost:8000/messages/{message_id}/suggestions",
    params={"hotel_id": hotel_id}
)

suggestions_data = response.json()
print(f"メッセージタイプ: {suggestions_data['message_type']}")

for i, suggestion in enumerate(suggestions_data['suggestions']):
    print(f"候補 {i+1}:")
    print(f"内容: {suggestion['content']}")
    print(f"信頼度: {suggestion['confidence']}")
    print(f"タイプ: {suggestion['type']}")
    print("---")
```

### 4. 返信送信

```python
# 返信を送信
message_id = 1
response_content = "お客様、お疲れ様です。ご質問にお答えいたします。"
platform = "booking.com"

response = requests.post(
    f"http://localhost:8000/messages/{message_id}/respond",
    params={
        "response_content": response_content,
        "platform": platform
    }
)

result = response.json()
print(f"送信結果: {result['result']}")
```

### 5. 分析データ取得

```python
# ホテルの分析データを取得
hotel_id = 1
response = requests.get(f"http://localhost:8000/hotels/{hotel_id}/analytics")
analytics = response.json()

print("予約分析:")
booking_analysis = analytics['booking_analysis']
print(f"総予約数: {booking_analysis['total_bookings']}")
print(f"平均滞在日数: {booking_analysis['average_stay_duration']}日")
print(f"平均宿泊人数: {booking_analysis['average_guest_count']}人")

print("\n学習結果:")
learning_result = analytics['learning_result']
print(f"処理済みメッセージ: {learning_result['messages_processed']}件")
print(f"処理済み返信: {learning_result['responses_processed']}件")
```

### 6. 周辺観光地取得

```python
# ホテル周辺の観光地を取得
hotel_id = 1
radius = 2000  # 2km以内

response = requests.get(
    f"http://localhost:8000/hotels/{hotel_id}/nearby-attractions",
    params={"radius": radius}
)

attractions_data = response.json()
attractions = attractions_data['attractions']

for attraction in attractions:
    print(f"名前: {attraction['name']}")
    print(f"カテゴリ: {attraction['category']}")
    print(f"距離: {attraction['distance_km']}km")
    print(f"評価: {attraction['rating']}/5")
    print(f"住所: {attraction['address']}")
    print("---")
```

## 🐛 トラブルシューティング

### よくある問題と解決方法

#### 1. API接続エラー

**問題:** `API接続エラー: Connection refused`

**解決方法:**
```bash
# サービスが起動しているか確認
docker-compose ps

# ログを確認
docker-compose logs api

# サービスを再起動
docker-compose restart api
```

#### 2. データベース接続エラー

**問題:** `Database connection failed`

**解決方法:**
```bash
# PostgreSQLが起動しているか確認
docker-compose ps postgres

# データベースを再起動
docker-compose restart postgres

# 接続文字列を確認
echo $DATABASE_URL
```

#### 3. OpenAI APIエラー

**問題:** `OpenAI API error: Invalid API key`

**解決方法:**
```bash
# .envファイルのAPIキーを確認
cat .env | grep OPENAI_API_KEY

# APIキーが正しく設定されているか確認
python -c "from app.config import settings; print(settings.OPENAI_API_KEY[:10] + '...')"
```

#### 4. Google Maps APIエラー

**問題:** `Google Maps API error: REQUEST_DENIED`

**解決方法:**
```bash
# APIキーを確認
cat .env | grep GOOGLE_MAPS_API_KEY

# APIキーの権限を確認（Google Cloud Console）
# Places API、Maps JavaScript API、Geocoding APIが有効になっているか確認
```

#### 5. メッセージ取得エラー

**問題:** `Failed to fetch messages`

**解決方法:**
```bash
# 外部APIの制限を確認
# Booking.com/Airbnb APIの制限に達していないか確認

# ログを確認
docker-compose logs api | grep "fetch"

# 手動でメッセージ取得をテスト
curl -X POST "http://localhost:8000/messages/fetch/1"
```

### デバッグ方法

#### 1. ログレベルを上げる

```python
# app/config.pyでDEBUG=Trueに設定
DEBUG = True

# 詳細なログを出力
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 2. APIエンドポイントのテスト

```bash
# ヘルスチェック
curl http://localhost:8000/health

# ホテル一覧取得
curl http://localhost:8000/hotels

# メッセージ取得
curl http://localhost:8000/messages/1
```

#### 3. データベースの確認

```bash
# PostgreSQLに接続
docker-compose exec postgres psql -U postgres -d hotel_agent_db

# テーブル一覧を確認
\dt

# データを確認
SELECT * FROM hotels;
SELECT * FROM guest_messages;
```

## 📊 パフォーマンス最適化

### 1. キャッシュの活用

```python
# Redisキャッシュを使用
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# 周辺観光地情報をキャッシュ
def get_cached_attractions(hotel_id):
    cache_key = f"attractions_{hotel_id}"
    cached_data = r.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    
    # データを取得してキャッシュに保存
    attractions = fetch_attractions(hotel_id)
    r.setex(cache_key, 3600, json.dumps(attractions))  # 1時間キャッシュ
    
    return attractions
```

### 2. 非同期処理の活用

```python
# バックグラウンドでメッセージを取得
from fastapi import BackgroundTasks

@app.post("/messages/fetch/{hotel_id}")
async def fetch_new_messages(
    hotel_id: int,
    background_tasks: BackgroundTasks
):
    async def save_messages():
        messages = await message_processor.fetch_all_messages(str(hotel_id))
        # データベースに保存
    
    background_tasks.add_task(save_messages)
    return {"message": "メッセージの取得を開始しました"}
```

### 3. データベース最適化

```sql
-- インデックスを作成
CREATE INDEX idx_guest_messages_hotel_id ON guest_messages(hotel_id);
CREATE INDEX idx_guest_messages_timestamp ON guest_messages(timestamp);
CREATE INDEX idx_guest_messages_processed ON guest_messages(is_processed);

-- 複合インデックス
CREATE INDEX idx_guest_messages_hotel_processed ON guest_messages(hotel_id, is_processed);
```

## 🔒 セキュリティ考慮事項

### 1. APIキーの管理

```bash
# .envファイルを.gitignoreに追加
echo ".env" >> .gitignore

# 本番環境では環境変数を使用
export OPENAI_API_KEY="your-production-key"
export GOOGLE_MAPS_API_KEY="your-production-key"
```

### 2. データベースセキュリティ

```python
# 接続文字列にSSLを追加
DATABASE_URL = "postgresql://user:password@host:port/db?sslmode=require"
```

### 3. APIレート制限

```python
# FastAPIでレート制限を実装
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/messages/fetch/{hotel_id}")
@limiter.limit("10/minute")
async def fetch_new_messages(request: Request, hotel_id: int):
    # 実装
```

## 📈 監視とメトリクス

### 1. ヘルスチェック

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": "connected",
        "redis": "connected"
    }
```

### 2. メトリクス収集

```python
# メッセージ処理統計
@app.get("/metrics")
async def get_metrics():
    return {
        "total_messages": db.query(GuestMessage).count(),
        "processed_messages": db.query(GuestMessage).filter(GuestMessage.is_processed == True).count(),
        "pending_messages": db.query(GuestMessage).filter(GuestMessage.is_processed == False).count(),
        "average_response_time": calculate_average_response_time()
    }
```

このドキュメントを参考に、システムの使用方法を理解し、実際の運用に活用してください。不明な点がございましたら、GitHubのIssuesセクションでお知らせください。
