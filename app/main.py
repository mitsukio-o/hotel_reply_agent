from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import uvicorn
from datetime import datetime, timedelta

from app.database import get_db, create_tables
from app.models import Hotel, GuestMessage, ResponseLog
from app.services.api_service import MessageProcessor
from app.services.response_generator import ResponseGenerator
from app.agents.booking_data_agent import BookingDataAgent
from app.config import settings

# FastAPIアプリケーションの初期化
app = FastAPI(
    title=settings.APP_NAME,
    description="ホテル向け自動返信システム",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依存関係
message_processor = MessageProcessor()
response_generator = ResponseGenerator()
booking_data_agent = BookingDataAgent()

# データベーステーブル作成
create_tables()

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の初期化処理"""
    print(f"{settings.APP_NAME} が起動しました")

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "ホテル向け自動返信システム",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy"}

@app.get("/hotels")
async def get_hotels(db: Session = Depends(get_db)):
    """ホテル一覧を取得"""
    hotels = db.query(Hotel).all()
    return [
        {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
            "city": hotel.city,
            "country": hotel.country
        }
        for hotel in hotels
    ]

@app.post("/hotels")
async def create_hotel(
    name: str,
    address: str,
    latitude: float,
    longitude: float,
    city: str,
    country: str,
    db: Session = Depends(get_db)
):
    """新しいホテルを作成"""
    hotel = Hotel(
        name=name,
        address=address,
        latitude=latitude,
        longitude=longitude,
        city=city,
        country=country
    )
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    
    return {
        "id": hotel.id,
        "name": hotel.name,
        "address": hotel.address,
        "message": "ホテルが正常に作成されました"
    }

@app.get("/messages/{hotel_id}")
async def get_messages(
    hotel_id: int,
    platform: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """ホテルのメッセージを取得"""
    try:
        # データベースからメッセージを取得
        # GuestMessage -> Booking -> Hotel の順でJOIN
        from app.models import Booking
        
        # まず、ホテルが存在するかチェック
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="ホテルが見つかりません")
        
        # 予約が存在するかチェック
        bookings = db.query(Booking).filter(Booking.hotel_id == hotel_id).all()
        if not bookings:
            # 予約が存在しない場合は空のリストを返す
            return []
        
        # メッセージを取得
        query = db.query(GuestMessage).join(Booking, GuestMessage.booking_id == Booking.id).filter(Booking.hotel_id == hotel_id)
        
        if platform:
            query = query.filter(GuestMessage.platform == platform)
        
        messages = query.all()
        
        return [
            {
                "id": msg.id,
                "booking_id": msg.booking_id,
                "platform": msg.platform,
                "message_content": msg.message_content,
                "message_type": msg.message_type,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                "is_processed": msg.is_processed
            }
            for msg in messages
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"メッセージ取得エラー: {str(e)}")

from pydantic import BaseModel

class MessageCreate(BaseModel):
    booking_id: str
    platform: str
    message_content: str
    message_type: str
    guest_name: str
    timestamp: str

@app.post("/messages")
async def create_message(
    message_data: MessageCreate,
    hotel_id: int,
    db: Session = Depends(get_db)
):
    """テスト用メッセージを作成"""
    try:
        # 予約が存在するかチェック
        from app.models import Booking
        booking = db.query(Booking).filter(Booking.booking_id == message_data.booking_id).first()
        
        if not booking:
            # テスト用の予約を作成
            booking = Booking(
                booking_id=message_data.booking_id,
                hotel_id=hotel_id,  # 指定されたホテルID
                guest_name=message_data.guest_name,
                check_in=datetime.now(),
                check_out=datetime.now() + timedelta(days=1),
                guest_count=2,
                total_amount=10000,
                booking_reference=f"ref_{message_data.booking_id}"
            )
            db.add(booking)
            db.commit()
            db.refresh(booking)
        
        # メッセージを作成
        message = GuestMessage(
            booking_id=booking.id,
            platform=message_data.platform,
            message_content=message_data.message_content,
            message_type=message_data.message_type,
            timestamp=datetime.fromisoformat(message_data.timestamp.replace('Z', '+00:00')) if message_data.timestamp else datetime.now(),
            is_processed=False
        )
        
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return {
            "id": message.id,
            "booking_id": message.booking_id,
            "platform": message.platform,
            "message_content": message.message_content,
            "message_type": message.message_type,
            "timestamp": message.timestamp.isoformat() if message.timestamp else None,
            "is_processed": message.is_processed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"メッセージ作成エラー: {str(e)}")

@app.post("/messages/fetch/{hotel_id}")
async def fetch_new_messages(
    hotel_id: int,
    listing_id: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """新しいメッセージを取得してデータベースに保存"""
    
    async def save_messages():
        # 全プラットフォームからメッセージを取得
        messages = await message_processor.fetch_all_messages(str(hotel_id), listing_id)
        
        # データベースに保存（実際の実装では適切なセッション管理が必要）
        # ここでは簡略化
        
        return messages
    
    # バックグラウンドでメッセージを取得
    if background_tasks:
        background_tasks.add_task(save_messages)
        return {"message": "メッセージの取得を開始しました"}
    else:
        messages = await save_messages()
        return {"messages": messages, "count": len(messages)}

@app.post("/messages/{message_id}/suggestions")
async def get_response_suggestions(
    message_id: int,
    hotel_id: int,
    db: Session = Depends(get_db)
):
    """メッセージに対する返信候補を取得"""
    
    # メッセージを取得
    message = db.query(GuestMessage).filter(GuestMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="メッセージが見つかりません")
    
    # メッセージタイプを分類
    message_type = message_processor.categorize_message(message.message_content)
    
    # 返信候補を生成
    suggestions = await response_generator.generate_response_suggestions(
        message.message_content,
        message_type,
        hotel_id,
        db
    )
    
    return {
        "message_id": message_id,
        "message_content": message.message_content,
        "message_type": message_type,
        "suggestions": suggestions
    }

@app.post("/messages/{message_id}/respond")
async def send_response(
    message_id: int,
    response_content: str,
    platform: str,
    db: Session = Depends(get_db)
):
    """返信を送信"""
    
    # メッセージを取得
    message = db.query(GuestMessage).filter(GuestMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="メッセージが見つかりません")
    
    # 返信を送信
    result = await response_generator.send_response(
        str(message_id),
        response_content,
        platform,
        db
    )
    
    # メッセージを処理済みにマーク
    message.is_processed = True
    db.commit()
    
    return {
        "message_id": message_id,
        "response_content": response_content,
        "result": result
    }

@app.get("/hotels/{hotel_id}/analytics")
async def get_hotel_analytics(
    hotel_id: int,
    db: Session = Depends(get_db)
):
    """ホテルの分析データを取得"""
    try:
        # まず、ホテルが存在するかチェック
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="ホテルが見つかりません")
        
        # 予約パターンを分析
        booking_analysis = booking_data_agent.analyze_booking_patterns(db, hotel_id)
        
        # 過去のデータから学習
        learning_result = booking_data_agent.learn_from_historical_data(db, hotel_id)
        
        return {
            "hotel_id": hotel_id,
            "booking_analysis": booking_analysis,
            "learning_result": learning_result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析データ取得エラー: {str(e)}")

@app.get("/hotels/{hotel_id}/nearby-attractions")
async def get_nearby_attractions(
    hotel_id: int,
    radius: int = 2000,
    db: Session = Depends(get_db)
):
    """ホテル周辺の観光地を取得"""
    try:
        # まず、ホテルが存在するかチェック
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="ホテルが見つかりません")
        
        from app.agents.hotel_info_agent import HotelInfoAgent
        
        hotel_info_agent = HotelInfoAgent()
        attractions = hotel_info_agent.get_nearby_attractions(hotel_id, db, radius)
        
        return {
            "hotel_id": hotel_id,
            "radius_km": radius / 1000,
            "attractions": attractions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"周辺観光地取得エラー: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )