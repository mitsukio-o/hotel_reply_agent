# API接続エラーのトラブルシューティングガイド

## 現在の状況確認

### ✅ 正常に動作している項目
- Dockerサービス: 全て起動済み
- APIサーバー: http://localhost:8000 で正常動作
- Streamlitアプリ: http://localhost:8501 で正常動作
- テストスクリプト: 正常に実行

## よくあるAPI接続エラーの原因と解決方法

### 1. **ブラウザでのアクセス時のエラー**

**症状**: ブラウザでStreamlitアプリにアクセスした時に「API接続エラー」が表示される

**原因**: Streamlitアプリ内でAPIリクエストが失敗している

**解決方法**:
```bash
# 1. サービスが起動しているか確認
docker-compose ps

# 2. APIサーバーのログを確認
docker-compose logs api

# 3. Streamlitアプリのログを確認
docker-compose logs streamlit
```

### 2. **ポート競合エラー**

**症状**: "Address already in use" エラー

**解決方法**:
```bash
# 1. ポート使用状況を確認
netstat -an | findstr :8000
netstat -an | findstr :8501

# 2. サービスを再起動
docker-compose restart

# 3. 完全に停止してから再起動
docker-compose down
docker-compose up -d
```

### 3. **Firewall/セキュリティソフトのブロック**

**症状**: 接続がタイムアウトする

**解決方法**:
- Windowsファイアウォールでポート8000、8501を許可
- セキュリティソフトの例外設定に追加

### 4. **ネットワーク設定の問題**

**症状**: "Connection refused" エラー

**解決方法**:
```bash
# 1. localhostの名前解決を確認
ping localhost

# 2. 127.0.0.1でアクセスしてみる
curl http://127.0.0.1:8000/health
```

### 5. **Docker環境の問題**

**症状**: コンテナが起動しない、またはすぐに停止する

**解決方法**:
```bash
# 1. Dockerの状態を確認
docker --version
docker-compose --version

# 2. コンテナのログを確認
docker-compose logs api
docker-compose logs streamlit

# 3. コンテナを完全にリビルド
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 診断コマンド

### 基本的な接続テスト
```bash
# APIサーバーのヘルスチェック
curl http://localhost:8000/health

# Streamlitアプリの確認
curl http://localhost:8501

# ポートの確認
netstat -an | findstr :8000
netstat -an | findstr :8501
```

### 詳細な診断
```bash
# 全サービスのログを確認
docker-compose logs

# 特定サービスのログ
docker-compose logs api
docker-compose logs streamlit
docker-compose logs postgres
docker-compose logs redis

# リアルタイムログ監視
docker-compose logs -f api
```

## エラーメッセージ別の対処法

### "API接続エラー - サーバーに接続できません"
1. Dockerサービスが起動しているか確認
2. ポート8000が使用されているか確認
3. ファイアウォール設定を確認

### "Connection refused"
1. サーバーが起動していない
2. ポートが間違っている
3. ネットワーク設定の問題

### "Timeout"
1. サーバーの負荷が高い
2. ネットワークが遅い
3. ファイアウォールがブロックしている

### "404 Not Found"
1. エンドポイントのURLが間違っている
2. サーバーが起動していない
3. ルーティング設定の問題

## 緊急時の対処法

### 1. 完全リセット
```bash
# 全サービスを停止
docker-compose down

# ボリュームも削除（データは消えます）
docker-compose down -v

# 再起動
docker-compose up -d
```

### 2. 個別サービスの再起動
```bash
# APIサーバーのみ再起動
docker-compose restart api

# Streamlitアプリのみ再起動
docker-compose restart streamlit
```

### 3. ログファイルの確認
```bash
# 最新のログを確認
docker-compose logs --tail=50 api
```

## 予防策

1. **定期的なヘルスチェック**
   ```bash
   # 毎回実行前に確認
   curl http://localhost:8000/health
   ```

2. **ログの監視**
   ```bash
   # バックグラウンドでログを監視
   docker-compose logs -f
   ```

3. **リソースの確認**
   ```bash
   # システムリソースの確認
   docker stats
   ```

## サポート情報

問題が解決しない場合は、以下の情報を提供してください：

1. エラーメッセージの全文
2. 実行したコマンド
3. `docker-compose ps` の出力
4. `docker-compose logs api` の出力
5. オペレーティングシステムの情報

## アクセスURL

- **Streamlit UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

