#!/bin/bash

# ローカルデプロイスクリプト
echo "🚀 ローカルデプロイスクリプトを開始します..."

# 必要なファイルの確認
if [ ! -f "streamlit_app_fixed.py" ]; then
    echo "❌ streamlit_app_fixed.py が見つかりません"
    exit 1
fi

echo "✅ 必要なファイルが存在します"

# Pythonのバージョンチェック
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
if [ -z "$python_version" ]; then
    echo "❌ Python3がインストールされていません"
    exit 1
fi

echo "✅ Python $python_version を検出"

# 仮想環境の作成
if [ ! -d "venv" ]; then
    echo "📦 Python仮想環境を作成中..."
    python3 -m venv venv
fi

# 仮想環境をアクティベート
echo "🔧 仮想環境をアクティベート中..."
source venv/bin/activate

# 依存関係のインストール
echo "📥 依存関係をインストール中..."
pip install streamlit requests

# データベースの初期化
echo "🗄️ データベースを初期化中..."
python3 -c "
import sqlite3
import os

# データベースファイルが存在しない場合は作成
if not os.path.exists('hotel_agent.db'):
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
    print('データベース初期化完了')
else:
    print('データベースは既に存在します')
"

# サンプルデータの作成
echo "📊 サンプルデータを作成中..."
python3 -c "
import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('hotel_agent.db')
cursor = conn.cursor()

# ホテルデータを作成
hotels_data = [
    ('東京グランドホテル', '東京都千代田区丸の内1-1-1', 35.6762, 139.6503, '東京', '日本'),
    ('大阪ビジネスホテル', '大阪府大阪市北区梅田1-1-1', 34.6937, 135.5023, '大阪', '日本'),
    ('京都伝統旅館', '京都府京都市下京区四条通烏丸西入ル', 35.0116, 135.7681, '京都', '日本')
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
            f'ゲスト{i+1}',
            check_in.isoformat(),
            check_out.isoformat(),
            random.choice(['シングル', 'ダブル', 'ツイン', 'スイート']),
            random.randint(1, 4),
            f'REF{hotel_id:03d}{i+1:03d}',
            random.randint(8000, 15000),
            random.choice(['confirmed', 'cancelled', 'completed'])
        ))

# サンプルメッセージを作成
sample_messages = [
    ('チェックイン前に荷物を預かってもらえますか？午前10時に到着予定です。', 'luggage'),
    ('来月の15日から3泊4日で予約できますか？', 'availability'),
    ('ホテル周辺でおすすめの観光地はありますか？', 'attractions'),
    ('Wi-Fiのパスワードを教えてください。', 'general'),
    ('朝食は何時からですか？', 'general')
]

for hotel_id in hotel_ids:
    for message_content, message_type in sample_messages:
        # 予約IDを取得
        cursor.execute('SELECT id FROM bookings WHERE hotel_id = ? LIMIT 1', (hotel_id,))
        booking_result = cursor.fetchone()
        if booking_result:
            booking_id = booking_result[0]
            
            cursor.execute('''
                INSERT OR IGNORE INTO guest_messages 
                (booking_id, platform, message_content, message_type, is_processed)
                VALUES (?, ?, ?, ?, ?)
            ''', (booking_id, 'booking.com', message_content, message_type, False))

# テンプレートデータを作成
templates_data = [
    ('luggage', 'お荷物の預かりサービスをご利用いただけます。フロントデスクまでお越しください。'),
    ('luggage', 'チェックイン前・チェックアウト後もお荷物をお預かりいたします。'),
    ('availability', '空室状況をお調べいたします。ご希望の日程をお教えください。'),
    ('availability', 'ご予約可能な期間をご案内いたします。お急ぎの場合はお電話にてお問い合わせください。'),
    ('attractions', '周辺の観光地をご案内いたします。おすすめスポットをご紹介いたします。'),
    ('attractions', 'ホテル周辺の観光情報をお調べいたします。アクセス方法もご案内いたします。')
]

for hotel_id in hotel_ids:
    for template_type, template_content in templates_data:
        cursor.execute('''
            INSERT OR IGNORE INTO response_templates 
            (hotel_id, message_type, template_content, language, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', (hotel_id, template_type, template_content, 'ja', True))

conn.commit()
conn.close()
print('サンプルデータ作成完了')
"

# Streamlitアプリを起動
echo "🎨 Streamlitアプリを起動中..."
echo "ブラウザで http://localhost:8501 にアクセスしてください"
echo "終了するには Ctrl+C を押してください"
echo "=" * 60

streamlit run streamlit_app_fixed.py --server.port 8501 --server.address 0.0.0.0

echo "✅ デプロイが完了しました"
