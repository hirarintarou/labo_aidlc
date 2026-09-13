# API ドキュメント

## 外部 API

**なし。** 本アプリはローカル完結のデスクトップアプリケーションであり、外部 HTTP/GraphQL API のエンドポイントや、外部 API への送信は存在しない（ネットワーク送信は禁止方針）。

## 内部モジュール契約（public 関数/クラス）

レイヤ境界を跨ぐ主要な契約は以下。依存方向は `ui -> core -> io`（`batch` は `core`/`io`）。

### `core.edit_settings`

- `EditSettings` — frozen dataclass。`is_identity`（恒等判定）, `copy_with(...)`（部分更新コピー）。
- `Credit`, `Crop`, `Resize` — 編集設定の値オブジェクト。
- `CreditPosition` — クレジット位置の enum。

### `core.processor`

- `apply(image, settings) -> Image` — 固定合成順（補正 → 画質 → フィルタ → トリミング/リサイズ → クレジット）で `Image` に編集を適用。

### `core.presets`

- `list_presets()` — プリセット一覧。
- `preset_names()` — プリセット名の一覧。
- `get_preset(name)` — 名前からプリセット取得。
- `PresetDefinition.merge_into(settings)` — プリセットを既存設定にマージ。
- `BUILTIN_PRESETS` — ビルトインプリセット（8 種）。

### `io.image_io`

- `detect_format(path)` — フォーマット判定。
- `load_image(path, *, max_pixels)` — 画素数上限つきの安全デコード。
- `build_output_path(...)` — 非破壊の出力パス生成。
- `save_nondestructive(...)` — 別ファイルへのアトミック保存。

### `batch.batch_processor`

- `process_files(sources, settings, out_dir, *, progress, max_pixels) -> BatchResult` — 複数ファイルへ同一設定を適用し集計。

### `ui.panels`

- `AdjustmentPanel` — シグナル `changed = Signal()`, `values()`, `reset()`。
- `PresetPanel` — シグナル `changed = Signal()`, `selected_preset()`, `reset()`。

### `ui.main_window`

- `MainWindow` — メインウィンドウ。パネルの `changed` を `_update_preview` に接続。
- `pil_to_qpixmap(image)` — Pillow `Image` → QPixmap 変換（QImage 変換の直前でのみ Pillow を扱う）。

## 契約上の注意（intent 関連）

`ui.panels` の `changed = Signal()`（引数なし）と、上流 Qt シグナル（`QSlider.valueChanged` / `QComboBox.currentIndexChanged`、いずれも `int` を伴う）の直結が、現行 intent の不具合の原因。詳細は `code-quality-assessment.md`。
