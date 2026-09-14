# スモークテスト結果 — preview-changed-error（bugfix）

## 目的

報告バグ（画像を開いて調整・フィルタ・プリセットを操作するとコンソールにエラー）が解消していることを、ランタイムで確認する。

## 実行方法（ヘッドレス）

`app/` ディレクトリ、`QT_QPA_PLATFORM=offscreen`、`.venv` の python で、修正対象のバグ再現経路を駆動:

- `AdjustmentPanel` を生成し `changed` を引数なしスロットへ接続、全スライダーを `setValue(40)` / `setValue(-40)` で操作。
- `PresetPanel` を生成し `changed` を接続、コンボを `setCurrentIndex(1)` / `setCurrentIndex(0)` で変更。
- 両パネルの `reset()` を実行。
- 実行中の `stderr`（コンソール出力）を捕捉。

## 結果

| 項目 | 期待 | 実測 | 判定 |
|---|---|---|---|
| `changed` の発火 | 操作ごとに引数なしで発火 | 16 回発火 | PASS |
| コンソール（stderr）出力 | シグネチャ不一致エラーなし（0） | stderr 長 0 | PASS |
| 例外 | なし | なし | PASS |

**総合: PASS**。修正前に発生していたシグネチャ不一致に伴うコンソールエラーは発生しない。バグ解消をランタイムで実証（FR1.1 / FR1.2 / FR1.3 / NFR3）。

## 補足

- 完全な GUI 起動（ウィンドウ表示・実画像の読み込み）は表示環境を要するため、ヘッドレスで同一のシグナル配線経路を駆動して代替検証した。プレビュー更新経路（`main_window._update_preview` は `changed` を購読）も同じ配線のため、コンソールエラー解消とあわせて健全。
