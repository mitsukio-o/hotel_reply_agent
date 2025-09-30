# トラブルシューティングガイド

## 問題解決済み項目

### 1. test_data.pyが時間がかかる問題
**問題**: test_data.pyの実行が無限に時間がかかる

**原因**: 
- API接続タイムアウトの設定がない
- エラーハンドリングが不十分
- サーバーが起動していない場合の適切な処理がない

**解決策**:
- 全てのAPIリクエストに10秒のタイムアウトを設定
- API接続テスト機能を追加
- 詳細なエラーメッセージとトラブルシューティング情報を表示

### 2. Streamlitアプリの読み込みが無限に時間がかかる問題
**問題**: http://localhost:8501/の読み込みが無限に時間がかかる

**原因**:
- API_BASE_URLがDocker内部のURL (`http://api:8000`) に設定されている
- ローカル開発環境では `http://localhost:8000` にアクセスする必要がある
- APIリクエストにタイムアウト設定がない

**解決策**:
- API_BASE_URLを `http://localhost:8000` に変更
- 全てのAPIリクエストにタイムアウトを設定
- 詳細なエラーハンドリングを追加

## 使用方法

### 1. システムの起動
```bash
cd hotelcursor2
docker-compose up -d
```

### 2. サービスの確認
```bash
# サービスの状態確認
docker-compose ps

# APIのヘルスチェック
curl http://localhost:8000/health

# Streamlitアプリの確認
curl http://localhost:8501
```

### 3. テストデータの生成
```bash
python test_data.py
```

### 4. アクセスURL
- **Streamlit UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## よくある問題と解決方法

### API接続エラー
**症状**: "API接続エラー - サーバーに接続できません"

**解決方法**:
1. Docker Composeサービスが起動しているか確認
   ```bash
   docker-compose ps
   ```

2. APIサービスが正常に起動しているか確認
   ```bash
   curl http://localhost:8000/health
   ```

3. ポートが使用されていないか確認
   ```bash
   netstat -an | findstr :8000
   ```

### タイムアウトエラー
**症状**: "API接続タイムアウト"

**解決方法**:
1. データベースの起動を待つ
   ```bash
   docker-compose logs postgres
   ```

2. Redisの起動を待つ
   ```bash
   docker-compose logs redis
   ```

3. サービスを再起動
   ```bash
   docker-compose restart
   ```

### Streamlitアプリが表示されない
**症状**: http://localhost:8501 にアクセスできない

**解決方法**:
1. Streamlitサービスが起動しているか確認
   ```bash
   docker-compose logs streamlit
   ```

2. ポート8501が使用されていないか確認
   ```bash
   netstat -an | findstr :8501
   ```

3. ブラウザのキャッシュをクリア

## ログの確認方法

### 全サービスのログ
```bash
docker-compose logs
```

### 特定サービスのログ
```bash
# APIサービス
docker-compose logs api

# Streamlitサービス
docker-compose logs streamlit

# データベース
docker-compose logs postgres

# Redis
docker-compose logs redis
```

### リアルタイムログ
```bash
docker-compose logs -f api
```

## パフォーマンス改善

### 1. リクエストタイムアウト
- 全てのAPIリクエストに適切なタイムアウトを設定
- 一般的なリクエスト: 10秒
- 返信候補生成: 30秒
- メッセージ取得: 30秒

### 2. エラーハンドリング
- 接続エラー、タイムアウトエラー、HTTPステータスエラーを個別に処理
- ユーザーフレンドリーなエラーメッセージを表示

### 3. 接続テスト
- アプリケーション起動時にAPI接続をテスト
- 接続失敗時は適切なメッセージを表示

## 開発時の注意点

1. **環境変数**: Docker環境では `API_BASE_URL=http://api:8000`、ローカル環境では `http://localhost:8000`
2. **ポート競合**: 8000番と8501番ポートが他のアプリケーションで使用されていないことを確認
3. **データベース初期化**: 初回起動時はデータベースの初期化に時間がかかる場合がある
4. **APIキー**: 外部APIを使用する場合は適切なAPIキーを設定

## サポート

問題が解決しない場合は、以下を確認してください：

1. DockerとDocker Composeが最新バージョンであること
2. システムのリソース（メモリ、CPU）が十分であること
3. ファイアウォールがポート8000、8501をブロックしていないこと
4. ログファイルにエラーメッセージが記録されていないこと

