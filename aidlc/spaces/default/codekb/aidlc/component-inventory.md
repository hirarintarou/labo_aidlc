# コンポーネント一覧

依存方向は一方向 `ui -> core -> io`（`batch` は `core`/`io` を利用）。`core`/`io` は PySide6 非依存。

## screenshot_editor

- **責務**: アプリケーションルートパッケージ。エントリポイント（`__main__.main`）と共通例外（`errors`）を提供。
- **依存**: 配下の各層をまとめる。

## screenshot_editor.core

- **責務**: ドメインロジック層（GUI 非依存）。画像変換ロジックと編集設定・プリセットを提供。
- **主なモジュール**: `edit_settings`（`EditSettings`, `Credit`, `Crop`, `Resize`, `CreditPosition`）, `processor`（`apply`）, `presets`（`BUILTIN_PRESETS` ほか）。
- **依存**: `io`（Pillow `Image` を扱う）、Pillow。PySide6 に非依存。

## screenshot_editor.io

- **責務**: I/O 層（GUI 非依存）。安全デコード、非破壊アトミック保存、出力パス生成、フォーマット判定。
- **主なモジュール**: `image_io`（`detect_format`, `load_image`, `build_output_path`, `save_nondestructive`）。
- **依存**: Pillow のみ。最下層で他レイヤに非依存。

## screenshot_editor.batch

- **責務**: バッチ層。複数ファイルへの一括適用と結果集計。
- **主なモジュール**: `batch_processor`（`process_files -> BatchResult`）。
- **依存**: `core`（`processor`）, `io`（`image_io`）。

## screenshot_editor.ui

- **責務**: プレゼンテーション層（PySide6）。画面表示、プレビュー更新、編集値の入力。
- **主なモジュール**: `main_window`（`MainWindow`, `pil_to_qpixmap`）, `panels`（`AdjustmentPanel`, `PresetPanel`）, `batch_dialog`（`QThread` ワーカー）。
- **依存**: `core`, `batch`, PySide6。Pillow は `pil_to_qpixmap` の変換直前でのみ扱う。

## tests

- **責務**: pytest テストスイート。
- **カバー範囲**: `core`（`test_edit_settings`, `test_presets`, `test_processor`）, `io`（`test_image_io`）, `batch`（`test_batch_processor`）。フィクスチャは `conftest.py` で合成画像を生成。
- **未カバー**: `ui` 層（シグナル配線・プレビュー経路のテストなし）。詳細は `code-quality-assessment.md`。
