@echo off
echo 🚀 ローカルデプロイスクリプトを開始します...

REM 必要なファイルの確認
if not exist "streamlit_app_fixed.py" (
    echo ❌ streamlit_app_fixed.py が見つかりません
    pause
    exit /b 1
)

echo ✅ 必要なファイルが存在します

REM Pythonのバージョンチェック
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonがインストールされていません
    pause
    exit /b 1
)

echo ✅ Pythonを検出

REM 仮想環境の作成
if not exist "venv" (
    echo 📦 Python仮想環境を作成中...
    python -m venv venv
)

REM 仮想環境をアクティベート
echo 🔧 仮想環境をアクティベート中...
call venv\Scripts\activate.bat

REM 依存関係のインストール
echo 📥 依存関係をインストール中...
pip install streamlit requests

REM データベースの初期化
echo 🗄️ データベースを初期化中...
python -c "import sqlite3; import os; conn = sqlite3.connect('hotel_agent.db') if not os.path.exists('hotel_agent.db') else None; cursor = conn.cursor() if conn else None; cursor.execute('CREATE TABLE IF NOT EXISTS hotels (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, address TEXT NOT NULL, latitude REAL, longitude REAL, city TEXT NOT NULL, country TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)') if cursor else None; cursor.execute('CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, booking_id TEXT UNIQUE, hotel_id INTEGER NOT NULL, guest_name TEXT, check_in TIMESTAMP, check_out TIMESTAMP, room_type TEXT, guest_count INTEGER, booking_reference TEXT UNIQUE, total_amount REAL, status TEXT DEFAULT ''confirmed'', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (hotel_id) REFERENCES hotels (id))') if cursor else None; cursor.execute('CREATE TABLE IF NOT EXISTS guest_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, booking_id INTEGER, platform TEXT NOT NULL, message_content TEXT NOT NULL, message_type TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_processed BOOLEAN DEFAULT FALSE, FOREIGN KEY (booking_id) REFERENCES bookings (id))') if cursor else None; cursor.execute('CREATE TABLE IF NOT EXISTS response_templates (id INTEGER PRIMARY KEY AUTOINCREMENT, hotel_id INTEGER NOT NULL, message_type TEXT NOT NULL, template_content TEXT NOT NULL, language TEXT DEFAULT ''ja'', is_active BOOLEAN DEFAULT TRUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (hotel_id) REFERENCES hotels (id))') if cursor else None; conn.commit() if conn else None; conn.close() if conn else None; print('データベース初期化完了') if conn else print('データベースは既に存在します')"

REM サンプルデータの作成
echo 📊 サンプルデータを作成中...
python -c "import sqlite3; import random; from datetime import datetime, timedelta; conn = sqlite3.connect('hotel_agent.db'); cursor = conn.cursor(); hotels_data = [('東京グランドホテル', '東京都千代田区丸の内1-1-1', 35.6762, 139.6503, '東京', '日本'), ('大阪ビジネスホテル', '大阪府大阪市北区梅田1-1-1', 34.6937, 135.5023, '大阪', '日本'), ('京都伝統旅館', '京都府京都市下京区四条通烏丸西入ル', 35.0116, 135.7681, '京都', '日本')]; hotel_ids = []; [hotel_ids.append(cursor.lastrowid if cursor.lastrowid else cursor.fetchone()[0]) for hotel_data in hotels_data if cursor.execute('INSERT OR IGNORE INTO hotels (name, address, latitude, longitude, city, country) VALUES (?, ?, ?, ?, ?, ?)', hotel_data) or cursor.lastrowid == 0 and cursor.execute('SELECT id FROM hotels WHERE name = ?', (hotel_data[0],))]; [cursor.execute('INSERT OR IGNORE INTO bookings (hotel_id, guest_name, check_in, check_out, room_type, guest_count, booking_reference, total_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (hotel_id, f'ゲスト{i+1}', (datetime.now() + timedelta(days=random.randint(-30, 30))).isoformat(), (datetime.now() + timedelta(days=random.randint(-30, 30)) + timedelta(days=random.randint(1, 7))).isoformat(), random.choice(['シングル', 'ダブル', 'ツイン', 'スイート']), random.randint(1, 4), f'REF{hotel_id:03d}{i+1:03d}', random.randint(8000, 15000), random.choice(['confirmed', 'cancelled', 'completed']))) for hotel_id in hotel_ids for i in range(5)]; sample_messages = [('チェックイン前に荷物を預かってもらえますか？午前10時に到着予定です。', 'luggage'), ('来月の15日から3泊4日で予約できますか？', 'availability'), ('ホテル周辺でおすすめの観光地はありますか？', 'attractions'), ('Wi-Fiのパスワードを教えてください。', 'general'), ('朝食は何時からですか？', 'general')]; [cursor.execute('INSERT OR IGNORE INTO guest_messages (booking_id, platform, message_content, message_type, is_processed) VALUES (?, ?, ?, ?, ?)', (cursor.fetchone()[0], 'booking.com', message_content, message_type, False)) for hotel_id in hotel_ids for message_content, message_type in sample_messages if cursor.execute('SELECT id FROM bookings WHERE hotel_id = ? LIMIT 1', (hotel_id,)) and cursor.fetchone()]; templates_data = [('luggage', 'お荷物の預かりサービスをご利用いただけます。フロントデスクまでお越しください。'), ('luggage', 'チェックイン前・チェックアウト後もお荷物をお預かりいたします。'), ('availability', '空室状況をお調べいたします。ご希望の日程をお教えください。'), ('availability', 'ご予約可能な期間をご案内いたします。お急ぎの場合はお電話にてお問い合わせください。'), ('attractions', '周辺の観光地をご案内いたします。おすすめスポットをご紹介いたします。'), ('attractions', 'ホテル周辺の観光情報をお調べいたします。アクセス方法もご案内いたします。')]; [cursor.execute('INSERT OR IGNORE INTO response_templates (hotel_id, message_type, template_content, language, is_active) VALUES (?, ?, ?, ?, ?)', (hotel_id, template_type, template_content, 'ja', True)) for hotel_id in hotel_ids for template_type, template_content in templates_data]; conn.commit(); conn.close(); print('サンプルデータ作成完了')"

REM Streamlitアプリを起動
echo 🎨 Streamlitアプリを起動中...
echo ブラウザで http://localhost:8501 にアクセスしてください
echo 終了するには Ctrl+C を押してください
echo ============================================================

streamlit run streamlit_app_fixed.py --server.port 8501 --server.address 0.0.0.0

echo ✅ デプロイが完了しました
pause
