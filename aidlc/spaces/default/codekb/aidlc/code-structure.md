# コード構成

## リポジトリ構成

- `app/` — アプリケーション本体（Python プロジェクト `screenshot-editor`）。
- `.kiro/` — AI-DLC ワークフローの scaffolding（プロダクト外、コンテキストのみ）。
- `aidlc/` — AI-DLC ワークスペース記録（プロダクト外、コンテキストのみ）。

## パッケージ／モジュール構成（`app/screenshot_editor/`）

- `__init__.py` — パッケージ初期化。
- `__main__.py` — エントリポイント（`main`）。`screenshot-editor` コマンドから起動。
- `errors.py` — アプリ共通の例外定義。
- `core/` — ドメインロジック層（GUI 非依存）。
  - `edit_settings.py` — 編集設定の値オブジェクト群。
  - `processor.py` — 画像変換の合成適用。
  - `presets.py` — ビルトインプリセット定義と参照。
- `io/` — I/O 層（GUI 非依存）。
  - `image_io.py` — 安全デコード・非破壊アトミック保存・出力パス生成。
- `batch/` — バッチ層。
  - `batch_processor.py` — 複数ファイル一括適用と集計。
- `ui/` — プレゼンテーション層（PySide6）。
  - `main_window.py` — メインウィンドウ、プレビュー更新、`pil_to_qpixmap`。
  - `panels.py` — 調整パネル・プリセットパネル。
  - `batch_dialog.py` — バッチ実行ダイアログ（`QThread` ワーカー）。
- `tests/` — pytest スイート（`conftest.py`, `test_edit_settings.py`, `test_presets.py`, `test_processor.py`, `test_image_io.py`, `test_batch_processor.py`）。

各コンポーネントの責務・依存の詳細は `component-inventory.md` を参照。

## ファイル分類

- **設定/ビルド**: `app/pyproject.toml`, `app/uv.lock`, `app/.python-version`, `app/.pre-commit-config.yaml`, `app/run_checks.py`。
- **ドキュメント**: `app/README.md`。
- **ソース**: `app/screenshot_editor/**`。
- **テスト**: `app/tests/**`。

## コードパターン・慣習

- **レイヤード + 一方向依存**: `ui -> core -> io`（`batch` は `core`/`io` を利用）。`core`/`io` は PySide6 を import しない。
- **不変値オブジェクト**: `EditSettings` は frozen dataclass（`is_identity`/`copy_with`）で恒等既定・イミュータブル。
- **決定的処理**: `processor.apply` は固定合成順で再現性を確保。
- **UI シグナル駆動**: パネルは `changed = Signal()` を発火し、`main_window` が `_update_preview` を接続。
- **objectName 付与**: 主要 UI 要素に `data-testid` 相当の `objectName` を設定。
- **国際化コメント**: モジュールに日本語 docstring・インラインコメントが手厚い。
- **抑制コメント**: 限定的（`run_checks.py` の `# noqa: S603`、`batch_dialog.py` の `# noqa: N802`）。
