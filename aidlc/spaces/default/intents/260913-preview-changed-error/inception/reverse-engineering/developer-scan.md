## Developer Code Scan Results

対象: プロジェクトルート repo（CodeKB 識別子 `aidlc`）。アプリケーション本体は `app/`（Python プロジェクト `screenshot-editor`）。バグ intent `preview-changed-error`（画像を開いて調整・フィルタ・プリセットを選ぶとコンソールにエラーが出る）に関連する preview / adjustment / filter / preset 経路とシグナル配線を重点的に精査した。

### Scan Coverage
- **Analyzed deeply**（`./` の範囲内。repo-relative）:
  - `app/pyproject.toml`
  - `app/.python-version`
  - `app/.pre-commit-config.yaml`
  - `app/run_checks.py`
  - `app/README.md`
  - `app/screenshot_editor/__init__.py`
  - `app/screenshot_editor/__main__.py`
  - `app/screenshot_editor/errors.py`
  - `app/screenshot_editor/core/edit_settings.py`
  - `app/screenshot_editor/core/presets.py`
  - `app/screenshot_editor/core/processor.py`
  - `app/screenshot_editor/io/image_io.py`
  - `app/screenshot_editor/batch/batch_processor.py`
  - `app/screenshot_editor/ui/main_window.py`
  - `app/screenshot_editor/ui/panels.py`
  - `app/screenshot_editor/ui/batch_dialog.py`
  - `app/tests/conftest.py`
  - `app/tests/test_presets.py`
  - `app/tests/test_edit_settings.py`（`changed`/`Signal` 検索の該当確認）
- **Skimmed only**（ディレクトリ粒度で確認、深読みせず）:
  - `app/uv.lock`（依存の固定確認のみ。pyproject との整合は目視せず）
  - `app/tests/test_image_io.py`, `app/tests/test_processor.py`, `app/tests/test_batch_processor.py`（存在とネーミングで対象層を確認。本体は未読）
  - `.kiro/`（AI-DLC ワークフロー scaffolding。テスト対象外の context）
  - `aidlc/`（AI-DLC ワークスペース記録。テスト対象外の context）
  - **除外（未走査）**: `app/.venv/`, `app/.ruff_cache/`（指示どおり deep-analyze しない）

### Packages Found
- `screenshot_editor` — アプリケーションルートパッケージ — Python — FF14 スクリーンショットをローカル・非破壊で加工する Windows デスクトップアプリ
- `screenshot_editor.core` — ドメインロジック層 — Python — 画像変換ロジック（`EditSettings`, `processor`, `presets`）。GUI 非依存の純粋モジュール
- `screenshot_editor.io` — I/O 層 — Python — 安全デコード・非破壊アトミック保存（`image_io`）。GUI 非依存
- `screenshot_editor.batch` — バッチ層 — Python — 複数ファイルへの一括適用と集計（`batch_processor`）
- `screenshot_editor.ui` — プレゼンテーション層 — Python — PySide6 画面（`main_window`, `panels`, `batch_dialog`）
- `tests` — テスト — Python — pytest テストスイート（core / io / batch / edit_settings / presets）

依存方向は `ui -> core -> io`（`batch` は `core`/`io` を利用）の一方向。`core`/`io` は PySide6 を import しない（project.md の Mandated 準拠）。

### Build System
- **Type**: uv（パッケージ管理・仮想環境） + hatchling（ビルドバックエンド）
- **Config Files**: `app/pyproject.toml`, `app/uv.lock`, `app/.python-version`（3.11）
- **Build Dependencies**（`app/pyproject.toml`）:
  - ランタイム: `PySide6==6.7.2`, `Pillow==10.4.0`
  - dev extra: `pytest==8.3.2`, `pytest-cov==5.0.0`, `ruff==0.6.2`, `black==24.8.0`, `pre-commit==3.8.0`, `pyinstaller==6.10.0`
  - build-system: `hatchling`（wheel パッケージは `screenshot_editor`）
  - entry point: `screenshot-editor = "screenshot_editor.__main__:main"`

### APIs Discovered
- 外部 HTTP/GraphQL API: なし（ローカル完結のデスクトップアプリ。ネットワーク送信は project.md で禁止）
- 内部モジュール契約（public 関数/クラス）:
  - `core.edit_settings` — `EditSettings`（frozen dataclass, `is_identity`/`copy_with`）, `Credit`, `Crop`, `Resize`, `CreditPosition`
  - `core.processor` — `apply(image, settings) -> Image`（固定合成順: 補正→画質→フィルタ→トリミング/リサイズ→クレジット）
  - `core.presets` — `list_presets()`, `preset_names()`, `get_preset(name)`, `PresetDefinition.merge_into(settings)`, `BUILTIN_PRESETS`（8 種）
  - `io.image_io` — `detect_format(path)`, `load_image(path, *, max_pixels)`, `build_output_path(...)`, `save_nondestructive(...)`
  - `batch.batch_processor` — `process_files(sources, settings, out_dir, *, progress, max_pixels) -> BatchResult`
  - `ui.panels` — `AdjustmentPanel`（signal `changed = Signal()`, `values()`, `reset()`）, `PresetPanel`（signal `changed = Signal()`, `selected_preset()`, `reset()`）
  - `ui.main_window` — `MainWindow`, `pil_to_qpixmap(image)`
- UI → core → io の層境界: Pillow の `Image` は io/core 内に閉じ込め、ui は `pil_to_qpixmap` で QImage 変換の直前でのみ扱う

### Frameworks & Libraries
- Python — 3.11 — 言語/ランタイム（`requires-python = ">=3.11"`）
- PySide6 — 6.7.2 — GUI フレームワーク（Qt for Python）
- Pillow — 10.4.0 — 画像処理（デコード・変換・保存）
- pytest — 8.3.2 — テストランナー
- pytest-cov — 5.0.0 — カバレッジ計測
- ruff — 0.6.2 — lint（select: E, F, I, S, UP, B）
- black — 24.8.0 — フォーマッタ（line-length 100, py311）
- pre-commit — 3.8.0 — ローカルフック
- pyinstaller — 6.10.0 — 配布用 exe 生成
- uv — （lock 管理）— パッケージ管理・仮想環境

### Test Coverage
- **Test Directories**: `app/tests/`
- **Test Frameworks**: pytest（`addopts = "-q"`, `testpaths = ["tests"]`）+ pytest-cov
- **Coverage Config**: あり。`[tool.coverage.run] source = ["screenshot_editor.core", "screenshot_editor.io"]`, `branch = false`。カバレッジ下限は `--cov-fail-under=80`（core/io のみ）
- テストファイル: `test_edit_settings.py`, `test_presets.py`, `test_processor.py`, `test_image_io.py`, `test_batch_processor.py`。**`ui/` 層を対象とするテストは存在しない**（`main_window.py` / `panels.py` / `batch_dialog.py` のシグナル配線・プレビュー経路は無試験）。フィクスチャは `conftest.py` で合成画像をプログラム生成

### Code Quality Indicators
- **Linting**: ruff（`app/pyproject.toml` `[tool.ruff]`、セキュリティ系 `S` 規則を含む）+ black（format check）
- **CI/CD**: リモート CI パイプラインファイルは未検出。品質ゲートは `app/.pre-commit-config.yaml`（pre-commit: black/ruff、pre-push: pytest+coverage）と `app/run_checks.py`（black --check / ruff / pytest+cov）でローカル強制
- **Documentation**: `app/README.md` が充実（機能・アーキテクチャ・技術スタック・起動/テスト手順）。各モジュールに日本語 docstring とインラインコメントが手厚い

### Technical Debt Signals
- **【intent の根因・高確度】シグナル引数不一致（`app/screenshot_editor/ui/panels.py`）**: `AdjustmentPanel` と `PresetPanel` はどちらも引数なしの `changed = Signal()` を宣言している。しかし
  - `AdjustmentPanel.__init__`: `slider.valueChanged.connect(self.changed.emit)`（`QSlider.valueChanged` は `int` を引数に発火）
  - `PresetPanel.__init__`: `self._combo.currentIndexChanged.connect(self.changed.emit)`（`QComboBox.currentIndexChanged` は `int` を引数に発火）

  Qt が上流シグナルの `int` 引数を `self.changed.emit` へそのまま渡すため、引数なしで宣言した `changed` シグナルに対して余分な位置引数を渡す形になる。PySide6 では実行時にコンソールへエラー（シグネチャ不一致に伴う TypeError/警告）が出る。これはユーザー報告「調整やフィルタ、プリセットを選択するとコンソールにエラー」と一致する。スライダー操作（調整）とコンボ選択（プリセット/フィルタ）の両方が該当し、症状の範囲（調整・フィルタ・プリセット）とも合致する。
  - 参考修正の方向性（実装は後段ステージ）: `changed = Signal(int)` に合わせるか、`emit` を引数を捨てるラムダ/スロットで包む（例 `.connect(lambda *_: self.changed.emit())`）。`reset()` 側は `self.changed.emit()` を引数なしで呼んでおり、後者の包む方式なら両立する。
- **UI 層の無試験（`app/tests/`）**: カバレッジ計測対象が `core`/`io` のみのため、`ui/` のシグナル配線・プレビュー更新（`_update_preview`）は自動テストで検知されない。緑の品質ゲートを通過してもこのクラスのバグはすり抜ける（本 intent がまさにその例）。
- **`batch_dialog.py` のスレッド後始末**: `_on_finished` で `QThread.quit()/wait()` を行うが、`_choose_and_run` の各所で例外が起きた場合のスレッド後始末は明示的でない（本 intent とは無関係だが将来の debt シグナル）。
- TODO/FIXME/HACK コメントや抑制コメントは実質なし（`run_checks.py` の `# noqa: S603`、`batch_dialog.py` の `# noqa: N802` は正当な限定抑制）。ハードコード資格情報・外部 URL・God クラスは未検出。

## Handoff Summary
- **Intent-relevant finding**: バグの根因は `app/screenshot_editor/ui/panels.py` のシグナル配線にある。`AdjustmentPanel.changed` と `PresetPanel.changed` は引数なしの `Signal()` として宣言されているのに、`QSlider.valueChanged`（`int`）と `QComboBox.currentIndexChanged`（`int`）を `self.changed.emit` へ直結している（`AdjustmentPanel.__init__` の `slider.valueChanged.connect(self.changed.emit)`、`PresetPanel.__init__` の `self._combo.currentIndexChanged.connect(self.changed.emit)`）。上流の `int` 引数が引数なしシグナルの emit に渡り、PySide6 実行時にコンソールへエラーが出る。これは「調整（スライダー）」「フィルタ／プリセット（コンボ）」の両操作で発生し、`main_window.py` の `self._adjust.changed.connect(self._update_preview)` / `self._preset.changed.connect(self._update_preview)` を介したプレビュー更新経路上で顕在化する。ユーザー報告の症状と一致。
- **Risks / follow-up**:
  - `panels.py` の `reset()` は `self.changed.emit()` を**引数なし**で呼ぶ。修正で `changed` のシグネチャを変える場合、`reset()` 経路と両立させること（引数を捨てるスロットで包む方式なら現行 `Signal()` と `reset()` の両方をそのまま維持できる）。
  - `core`/`io`/`batch` 側は本症状の原因ではない（`processor.apply` と `EditSettings` は決定的・恒等既定で健全、`presets.merge_into` も問題なし）。修正は ui 層に限定できる見込みで blast radius は小さい。
  - `ui/` 層に自動テストが一切なく、カバレッジ計測対象からも外れている（`pyproject.toml` の coverage source は `core`/`io` のみ）。回帰防止には UI シグナル配線のテスト追加が望ましいが、PySide6（GUI）依存のためテスト環境整備が必要。project.md の Mandated「依存方向 ui → core → io」「core は GUI を import しない」を壊さないこと。
