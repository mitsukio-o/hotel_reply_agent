# 🚀 ホテル向け自動返信システム - クイックスタートガイド

このガイドでは、ホテル向け自動返信システムを最短時間で起動し、基本的な機能をテストする方法を説明します。

## 📋 前提条件

- Docker と Docker Compose がインストールされていること
- OpenAI APIキーとGoogle Maps APIキーを持っていること
- 基本的なコマンドライン操作ができること

## ⚡ 5分で起動！

### ステップ1: 環境変数の設定

`.env`ファイルを作成し、必要なAPIキーを設定してください：

```bash
# .envファイルを作成
cat > .env << EOF
OPENAI_API_KEY=sk-your-openai-api-key-here
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/hotel_agent_db
REDIS_URL=redis://localhost:6379/0
APP_NAME=Hotel Response Agent
DEBUG=True
HOST=0.0.0.0
PORT=8000
EOF
```

### ステップ2: システムの起動

```bash
# システムを起動
docker-compose up -d

# 起動状況を確認
docker-compose ps
```

### ステップ3: 起動確認

```bash
# ヘルスチェック
curl http://localhost:8000/health

# ブラウザでアクセス
# Streamlit UI: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

## 🧪 基本テスト

### 自動テストの実行

```bash
# APIテストを実行
python test_sample.py

# テストデータを生成
python test_data.py
```

### 手動テスト

1. **Streamlit UIにアクセス**: http://localhost:8501
2. **ホテルを選択**: サイドバーからホテルを選択
3. **メッセージ管理**: 「メッセージ管理」タブでメッセージを確認
4. **返信候補生成**: 「返信候補を取得」ボタンをクリック
5. **返信送信**: 候補を選択して「この候補で返信」をクリック

## 📱 主要機能のテスト

### 1. ホテル登録

```bash
# API経由でホテルを登録
curl -X POST "http://localhost:8000/hotels" \
  -G -d "name=テストホテル" \
  -d "address=東京都渋谷区道玄坂1-2-3" \
  -d "latitude=35.6581" \
  -d "longitude=139.7016" \
  -d "city=東京" \
  -d "country=日本"
```

### 2. メッセージ取得

```bash
# メッセージを取得
curl -X POST "http://localhost:8000/messages/fetch/1"
```

### 3. 返信候補生成

```bash
# 返信候補を生成
curl -X POST "http://localhost:8000/messages/1/suggestions?hotel_id=1"
```

### 4. 分析データ取得

```bash
# 分析データを取得
curl "http://localhost:8000/hotels/1/analytics"
```

### 5. 周辺観光地取得

```bash
# 周辺観光地を取得
curl "http://localhost:8000/hotels/1/nearby-attractions?radius=2000"
```

## 🎯 実際のシナリオテスト

### シナリオ1: 荷物預かりの問い合わせ

**テストメッセージ:**
```
「チェックイン前に荷物を預かってもらえますか？午前10時に到着予定です。」
```

**期待される結果:**
- メッセージタイプ: 「荷物預かり」
- 3つの返信候補が生成される
- 信頼度の高い候補が提供される

### シナリオ2: 予約可能期間の問い合わせ

**テストメッセージ:**
```
「来月の15日から3泊4日で予約できますか？」
```

**期待される結果:**
- メッセージタイプ: 「予約確認」
- 予約データ学習エージェントが過去のデータを分析
- 適切な返信候補が生成される

### シナリオ3: 周辺観光地の問い合わせ

**テストメッセージ:**
```
「ホテル周辺でおすすめの観光地はありますか？」
```

**期待される結果:**
- メッセージタイプ: 「観光地情報」
- Google Maps APIを使用して周辺観光地を検索
- 詳細な観光地情報を含む返信候補が生成される

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 1. サービスが起動しない

```bash
# ログを確認
docker-compose logs

# サービスを再起動
docker-compose restart

# 完全にリセット
docker-compose down -v
docker-compose up -d
```

#### 2. API接続エラー

```bash
# ヘルスチェック
curl http://localhost:8000/health

# ポートが使用されているか確認
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501
```

#### 3. データベース接続エラー

```bash
# PostgreSQLの状態を確認
docker-compose ps postgres

# データベースに接続
docker-compose exec postgres psql -U postgres -d hotel_agent_db
```

#### 4. OpenAI APIエラー

```bash
# APIキーを確認
echo $OPENAI_API_KEY

# APIキーの有効性をテスト
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

#### 5. Google Maps APIエラー

```bash
# APIキーを確認
echo $GOOGLE_MAPS_API_KEY

# APIキーの有効性をテスト
curl "https://maps.googleapis.com/maps/api/geocode/json?address=Tokyo&key=$GOOGLE_MAPS_API_KEY"
```

## 📊 パフォーマンステスト

### 負荷テスト

```bash
# 複数のリクエストを同時に送信
for i in {1..10}; do
  curl "http://localhost:8000/hotels" &
done
wait
```

### メモリ使用量の確認

```bash
# Dockerコンテナのリソース使用量を確認
docker stats
```

### ログの監視

```bash
# リアルタイムでログを監視
docker-compose logs -f api
```

## 🚀 本番環境への移行

### 1. 環境変数の設定

```bash
# 本番環境用の環境変数を設定
export OPENAI_API_KEY="your-production-key"
export GOOGLE_MAPS_API_KEY="your-production-key"
export DATABASE_URL="postgresql://user:password@host:port/db"
export DEBUG=False
```

### 2. セキュリティ設定

```bash
# 秘密鍵を生成
openssl rand -hex 32

# 環境変数に設定
export SECRET_KEY="your-secret-key"
```

### 3. データベースのバックアップ

```bash
# データベースをバックアップ
docker-compose exec postgres pg_dump -U postgres hotel_agent_db > backup.sql
```

## 📈 監視とメトリクス

### ヘルスチェック

```bash
# 定期的なヘルスチェック
while true; do
  curl -s http://localhost:8000/health | jq .
  sleep 30
done
```

### メトリクス収集

```bash
# メトリクスを取得
curl "http://localhost:8000/metrics"
```

## 🎉 次のステップ

### 1. カスタマイズ

- 新しいメッセージタイプの追加
- 返信テンプレートのカスタマイズ
- 新しいプラットフォームの統合

### 2. 拡張機能

- メール通知機能
- Slack連携
- 多言語対応

### 3. 分析と改善

- 返信品質の分析
- ユーザーフィードバックの収集
- 機械学習モデルの改善

## 📚 参考資料

- [EXAMPLE.md](EXAMPLE.md) - 詳細な使用例
- [README.md](README.md) - システム概要
- [API Docs](http://localhost:8000/docs) - API仕様書

## 🆘 サポート

問題が発生した場合：

1. ログを確認: `docker-compose logs`
2. ヘルスチェック: `curl http://localhost:8000/health`
3. トラブルシューティング: [EXAMPLE.md](EXAMPLE.md)のトラブルシューティングセクションを参照
4. GitHub Issues: 問題を報告

---

**🎯 目標**: このガイドに従って、5分以内にシステムを起動し、基本的な機能をテストできるようになることです。

**💡 ヒント**: 問題が発生した場合は、まずログを確認し、EXAMPLE.mdのトラブルシューティングセクションを参照してください。
