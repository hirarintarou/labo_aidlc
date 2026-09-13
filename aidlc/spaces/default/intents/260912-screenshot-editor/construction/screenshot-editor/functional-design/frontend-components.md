# Frontend Components — screenshot-editor（mvp）

技術非依存のUIコンポーネント設計。画面は左メニュー＋中央プレビュー＋右調整パネル（rough/refined mockups で確定）[refined-mockups]。

## Component Hierarchy

```
MainWindow
├─ Toolbar（開く / 別名で保存 / バッチ適用）
├─ CategoryMenu（左: 基本補正/画質/フィルタ/トリミング/リサイズ/クレジット）
├─ PreviewPane（中央: 加工結果を即時表示）
├─ AdjustmentPanel（右: 選択カテゴリに応じて切替）
│   ├─ BasicAdjustPanel（明るさ/コントラスト/彩度スライダー）
│   ├─ QualityPanel（シャープ/ぼかし/ノイズ除去）
│   ├─ FilterListPanel（プリセット名リスト・ラジオ）
│   ├─ CropPanel（トリミング範囲指定）
│   ├─ ResizePanel（幅・高さ・アスペクト比保持）
│   ├─ CreditPanel（テキスト・位置・サイズ・不透明度）
│   └─ ResetButton（全調整初期化）
├─ StatusBar（元ファイル / 出力先 / この1枚を保存）
└─ BatchDialog（modal: 対象選択・出力先・進捗・実行）
```

## Component Responsibilities（props/state の論理）

| コンポーネント | 主な状態/入力 | 振る舞い |
|---------------|--------------|---------|
| MainWindow | 現在のImageDocument, EditSettings, 選択カテゴリ | 全体の状態管理。coreへの適用要求を仲介 |
| Toolbar | — | 開く/保存/バッチのアクション発火 |
| CategoryMenu | 選択中カテゴリ | カテゴリ選択で右パネル切替（AC1.1.3） |
| PreviewPane | 適用結果画像 | EditSettings変更のたびに即時再描画（リアルタイム） |
| AdjustmentPanel系 | 各調整値 | 値変更→MainWindow経由でcoreに適用→プレビュー更新 |
| ResetButton | — | EditSettingsを初期化（AC1.8.1） |
| BatchDialog | 対象一覧, 出力先, 進捗, 結果件数 | 一括適用の実行と進捗/結果表示（AC2.1.x）。Escで閉じる |

## Interaction Flows

- **カテゴリ選択**: CategoryMenu選択 → AdjustmentPanel を該当パネルに差し替え。
- **調整**: パネルの値変更 → EditSettings更新 → core適用 → PreviewPane更新（デバウンス等はcode-generationで最適化）。
- **保存**: Toolbar/StatusBar → io経由で非破壊保存 → 完了通知。
- **バッチ**: Toolbar → BatchDialog（modal）→ 対象/出力先選択 → 実行（進捗表示）→ 結果件数。

## Form Validation

- クレジットテキスト: 空でも可（未付与）。
- リサイズ寸法: 正の整数。不正値はユーザーに知らせ、適用しない。
- 対象/出力先未選択でのバッチ実行はボタン無効化。

## Accessibility

- キーボードで主要動線（開く→カテゴリ→調整→保存）を操作可、フォーカス可視（ACX.1）。
- BatchDialog は Esc で閉じ、フォーカスが起動元へ戻る（ACX.2）。
- 文字・ボタンは大きめ [NFR4]。

## API Integration Points

- 外部APIなし（ローカル完結）。UIはユニット内の core / io を呼ぶのみ。

## Assumptions & Open Questions

- 具体的なウィジェット・レイアウト実装は選定GUIフレームワークに従い code-generation で確定。
