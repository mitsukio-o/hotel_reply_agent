# Figma UI設計ガイド - ホテル返信システム

このガイドでは、ホテル向け自動返信システムのUIをFigmaで設計する方法を詳しく説明します。

## 📋 目次

1. [Figmaの基本設定](#figmaの基本設定)
2. [デザインシステムの構築](#デザインシステムの構築)
3. [メインレイアウトの設計](#メインレイアウトの設計)
4. [コンポーネント設計](#コンポーネント設計)
5. [プロトタイプ作成](#プロトタイプ作成)
6. [開発者向け仕様書](#開発者向け仕様書)

## 🎨 Figmaの基本設定

### 1. 新しいファイルの作成

1. **Figmaにアクセス**: https://www.figma.com
2. **新しいファイルを作成**: "Create new file" → "Design file"
3. **ファイル名**: "Hotel Response System - UI Design"
4. **フレームサイズ**: Desktop (1440x1024) を選択

### 2. 基本設定

```
- グリッド: 8px
- カラーモード: RGB
- フォント: Inter (Google Fonts)
- 言語: 日本語対応
```

## 🎯 デザインシステムの構築

### 1. カラーパレット

#### プライマリカラー
```
Primary Blue: #2563EB
Primary Blue Light: #3B82F6
Primary Blue Dark: #1D4ED8
```

#### セカンダリカラー
```
Success Green: #10B981
Warning Orange: #F59E0B
Error Red: #EF4444
Info Cyan: #06B6D4
```

#### ニュートラルカラー
```
Gray 50: #F9FAFB
Gray 100: #F3F4F6
Gray 200: #E5E7EB
Gray 300: #D1D5DB
Gray 400: #9CA3AF
Gray 500: #6B7280
Gray 600: #4B5563
Gray 700: #374151
Gray 800: #1F2937
Gray 900: #111827
```

#### テキストカラー
```
Text Primary: #111827
Text Secondary: #6B7280
Text Disabled: #9CA3AF
Text Inverse: #FFFFFF
```

### 2. タイポグラフィ

#### フォントサイズ
```
Heading 1: 32px / 40px line-height
Heading 2: 24px / 32px line-height
Heading 3: 20px / 28px line-height
Body Large: 16px / 24px line-height
Body Medium: 14px / 20px line-height
Body Small: 12px / 16px line-height
Caption: 11px / 16px line-height
```

#### フォントウェイト
```
Regular: 400
Medium: 500
SemiBold: 600
Bold: 700
```

### 3. スペーシング

```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
2xl: 48px
3xl: 64px
```

### 4. ボーダーラディウス

```
sm: 4px
md: 8px
lg: 12px
xl: 16px
full: 50%
```

## 🏗️ メインレイアウトの設計

### 1. レイアウト構造

```
┌─────────────────────────────────────────────────────────┐
│                    Header (80px)                        │
├─────────────┬───────────────────────────────────────────┤
│             │                                           │
│   Sidebar   │              Main Content                 │
│  (280px)    │             (1160px)                     │
│             │                                           │
│             │                                           │
└─────────────┴───────────────────────────────────────────┘
```

### 2. ヘッダー設計

#### ヘッダーコンポーネント
```
- 高さ: 80px
- 背景: White
- ボーダー: 1px solid Gray 200
- パディング: 0 24px
- 内容:
  - ロゴ (左側)
  - ページタイトル (中央)
  - ユーザー情報 (右側)
```

#### ヘッダーの要素
```
1. ロゴ
   - サイズ: 40x40px
   - アイコン: 🏨 (ホテルアイコン)
   - テキスト: "ホテル返信システム"

2. ページタイトル
   - フォント: Heading 3
   - カラー: Text Primary

3. ユーザー情報
   - アバター: 32x32px
   - ユーザー名: Body Medium
   - ドロップダウンメニュー
```

### 3. サイドバー設計

#### サイドバーコンポーネント
```
- 幅: 280px
- 背景: Gray 50
- ボーダー: 1px solid Gray 200 (右側)
- パディング: 24px 16px
```

#### サイドバーの要素

##### ホテル選択セクション
```
1. セクションヘッダー
   - テキスト: "ホテル選択"
   - フォント: Heading 3
   - マージン: 0 0 16px 0

2. ホテル選択ドロップダウン
   - 高さ: 40px
   - 背景: White
   - ボーダー: 1px solid Gray 300
   - ボーダーラディウス: md
   - パディング: 0 12px

3. ホテル情報カード
   - 背景: White
   - ボーダーラディウス: lg
   - パディング: 16px
   - シャドウ: 0 1px 3px rgba(0, 0, 0, 0.1)
   - 内容:
     - ホテル名 (Bold)
     - 住所 (Body Small, Text Secondary)
     - 都市・国 (Body Small, Text Secondary)

4. 新しいメッセージ取得ボタン
   - 高さ: 40px
   - 背景: Primary Blue
   - テキスト: White
   - ボーダーラディウス: md
   - 幅: 100%
```

##### ホテル追加セクション
```
1. セクションヘッダー
   - テキスト: "新しいホテルを追加"
   - フォント: Heading 3
   - マージン: 32px 0 16px 0

2. ホテル追加フォーム
   - 背景: White
   - ボーダーラディウス: lg
   - パディング: 16px
   - シャドウ: 0 1px 3px rgba(0, 0, 0, 0.1)

   フォーム要素:
   - ホテル名入力 (必須)
   - 都市入力 (必須)
   - 国入力 (必須)
   - 住所入力 (必須)
   - 緯度入力 (必須)
   - 経度入力 (必須)
   - 追加ボタン (Primary Blue)
```

### 4. メインコンテンツ設計

#### メインコンテンツコンテナ
```
- パディング: 24px
- 背景: White
- 最小高さ: calc(100vh - 80px)
```

#### タブナビゲーション
```
1. タブコンテナ
   - 高さ: 48px
   - ボーダー: 1px solid Gray 200 (下側)
   - パディング: 0 24px

2. タブアイテム
   - 高さ: 48px
   - パディング: 0 16px
   - フォント: Body Medium
   - アクティブ: Primary Blue, ボーダー 2px solid Primary Blue
   - 非アクティブ: Text Secondary
```

## 🧩 コンポーネント設計

### 1. メッセージ管理タブ

#### メッセージカード
```
- 背景: White
- ボーダー: 1px solid Gray 200
- ボーダーラディウス: lg
- パディング: 16px
- マージン: 0 0 16px 0
- シャドウ: 0 1px 3px rgba(0, 0, 0, 0.1)

内容:
1. メッセージヘッダー
   - プラットフォームアイコン (24x24px)
   - プラットフォーム名 (Bold)
   - 受信時刻 (Body Small, Text Secondary)
   - 展開/折りたたみアイコン

2. メッセージ内容
   - メッセージテキスト (Body Medium)
   - メッセージタイプ (Badge)

3. メッセージタグ
   - 緊急度タグ (🚨 緊急 / 📝 通常)
   - 処理状況タグ (✅ 処理済み / ⏳ 未処理)
   - 優先度タグ (🔴 高 / 🟡 中 / 🟢 低)

4. アクションボタン
   - 返信候補を取得ボタン (Primary Blue)
```

#### 返信候補カード
```
- 背景: Gray 50
- ボーダーラディウス: md
- パディング: 16px
- マージン: 8px 0

内容:
1. 候補ヘッダー
   - 候補番号 (Badge)
   - 信頼度 (Progress Bar)

2. 返信内容
   - 返信テキスト (Body Medium)

3. 参考資料情報
   - タイプ (Badge)
   - 参考資料 (Body Small)
   - 詳細情報 (展開可能)

4. 視覚的インジケーター
   - テンプレート: 📋
   - AI生成: 🤖
   - 過去の成功例: 📊

5. アクションボタン
   - この候補で返信ボタン (Success Green)
```

### 2. 分析タブ

#### 分析ダッシュボード
```
1. メトリクスカード
   - 背景: White
   - ボーダーラディウス: lg
   - パディング: 24px
   - シャドウ: 0 1px 3px rgba(0, 0, 0, 0.1)
   - 内容:
     - アイコン (48x48px)
     - 数値 (Heading 1)
     - ラベル (Body Medium)
     - 変化率 (Badge)

2. グラフコンテナ
   - 背景: White
   - ボーダーラディウス: lg
   - パディング: 24px
   - シャドウ: 0 1px 3px rgba(0, 0, 0, 0.1)
   - 高さ: 300px
```

### 3. ホテル情報タブ

#### ホテル詳細カード
```
1. 基本情報
   - ホテル名 (Heading 2)
   - 住所 (Body Medium)
   - 都市・国 (Body Medium)

2. 周辺観光地セクション
   - セクションヘッダー
   - 観光地取得ボタン
   - 観光地リスト

3. 観光地カード
   - 観光地名 (Bold)
   - カテゴリ (Badge)
   - 距離 (Body Small)
   - 評価 (Star Rating)
   - 住所 (Body Small)
```

## 🎭 プロトタイプ作成

### 1. インタラクション設計

#### メッセージ管理の流れ
```
1. ホテル選択
   - サイドバーでホテルを選択
   - ホテル情報が更新される

2. メッセージ表示
   - 未処理メッセージが表示される
   - メッセージカードをクリックで展開

3. 返信候補生成
   - "返信候補を取得"ボタンをクリック
   - ローディング状態を表示
   - 3つの候補が表示される

4. 返信送信
   - 候補を選択して"この候補で返信"をクリック
   - 送信確認ダイアログ
   - 成功メッセージ
```

#### ホテル追加の流れ
```
1. フォーム入力
   - 各フィールドに入力
   - バリデーション表示

2. 送信
   - "ホテルを追加"ボタンをクリック
   - ローディング状態
   - 成功メッセージ

3. 更新
   - ホテル一覧が更新される
   - 新しく追加されたホテルが選択可能
```

### 2. アニメーション

#### トランジション
```
- フェードイン: 300ms ease-out
- スライドイン: 300ms ease-out
- ホバーエフェクト: 200ms ease-in-out
```

#### ローディング状態
```
- スピナー: 1s linear infinite
- スケルトンローダー: 1.5s ease-in-out infinite
- プログレスバー: 2s ease-out
```

## 📋 開発者向け仕様書

### 1. CSS変数

```css
:root {
  /* Colors */
  --color-primary: #2563EB;
  --color-primary-light: #3B82F6;
  --color-primary-dark: #1D4ED8;
  
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #06B6D4;
  
  /* Typography */
  --font-family: 'Inter', sans-serif;
  --font-size-xs: 11px;
  --font-size-sm: 12px;
  --font-size-base: 14px;
  --font-size-lg: 16px;
  --font-size-xl: 20px;
  --font-size-2xl: 24px;
  --font-size-3xl: 32px;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;
  
  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 50%;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

### 2. コンポーネント仕様

#### ボタンコンポーネント
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  font-weight: 500;
  line-height: 1.5;
  text-decoration: none;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 200ms ease-in-out;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
}
```

#### カードコンポーネント
```css
.card {
  background-color: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

.card-header {
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--color-gray-200);
}

.card-body {
  margin-bottom: var(--spacing-md);
}

.card-footer {
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--color-gray-200);
}
```

### 3. レスポンシブデザイン

#### ブレークポイント
```
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+
```

#### モバイル対応
```css
@media (max-width: 767px) {
  .sidebar {
    width: 100%;
    position: fixed;
    top: 80px;
    left: -100%;
    height: calc(100vh - 80px);
    z-index: 1000;
    transition: left 300ms ease-out;
  }
  
  .sidebar.open {
    left: 0;
  }
  
  .main-content {
    width: 100%;
    padding: var(--spacing-md);
  }
}
```

## 🚀 Figmaでの実装手順

### 1. ファイル作成と設定
1. 新しいFigmaファイルを作成
2. デザインシステムページを作成
3. カラーパレットを設定
4. タイポグラフィを設定

### 2. コンポーネント作成
1. 基本コンポーネント（ボタン、カード、入力フィールド）
2. 複合コンポーネント（メッセージカード、返信候補カード）
3. レイアウトコンポーネント（ヘッダー、サイドバー）

### 3. ページ作成
1. メインレイアウトページ
2. メッセージ管理ページ
3. 分析ダッシュボードページ
4. ホテル情報ページ

### 4. プロトタイプ設定
1. インタラクションを設定
2. アニメーションを追加
3. ユーザーフローをテスト

### 5. 開発者向け準備
1. スペックモードを設定
2. エクスポート設定
3. 開発者コメントを追加

## 📚 参考リソース

### Figma公式リソース
- [Figma Design Systems](https://www.figma.com/design-systems/)
- [Figma Components](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma)
- [Figma Prototyping](https://help.figma.com/hc/en-us/articles/360040328193-Guide-to-prototyping-in-Figma)

### デザインシステム参考
- [Material Design](https://material.io/design)
- [Ant Design](https://ant.design/)
- [Chakra UI](https://chakra-ui.com/)

### 日本語対応
- [Noto Sans JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP)
- [M PLUS Rounded](https://fonts.google.com/specimen/M+PLUS+Rounded+1c)

---

このガイドを参考に、ホテル返信システムのUIをFigmaで設計してください。各セクションの詳細な実装方法については、Figmaの公式ドキュメントも併せて参照してください。
