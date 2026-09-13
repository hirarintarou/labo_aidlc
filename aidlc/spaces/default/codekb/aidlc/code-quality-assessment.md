# コード品質評価

## テストカバレッジ

- **テストランナー**: pytest（`addopts = "-q"`, `testpaths = ["tests"]`）+ pytest-cov。
- **カバレッジ設定**: `[tool.coverage.run] source = ["screenshot_editor.core", "screenshot_editor.io"]`, `branch = false`。下限は `--cov-fail-under=80`（**`core`/`io` のみ**が計測対象）。
- **テストファイル**: `test_edit_settings.py`, `test_presets.py`, `test_processor.py`, `test_image_io.py`, `test_batch_processor.py`。フィクスチャは `conftest.py` で合成画像を生成。
- **無試験の層**: `ui/`（`main_window.py` / `panels.py` / `batch_dialog.py`）にはテストが一切なく、カバレッジ計測対象からも外れている。シグナル配線・プレビュー更新（`_update_preview`）は自動テストで検知されない。

## Linting・フォーマット

- **ruff** 0.6.2（`app/pyproject.toml` `[tool.ruff]`、select: E, F, I, S, UP, B。セキュリティ系 `S` を含む）。
- **black** 24.8.0（line-length 100, target py311）。

## ローカル品質ゲート

- リモート CI パイプラインファイルは未検出。
- `app/.pre-commit-config.yaml`: pre-commit で black/ruff、pre-push で pytest+coverage。
- `app/run_checks.py`: `black --check` / `ruff` / `pytest+cov` をローカルで一括実行。

## ドキュメント品質

- `app/README.md` が充実（機能・アーキテクチャ・技術スタック・起動/テスト手順）。
- 各モジュールに日本語 docstring とインラインコメントが手厚い。

## 技術的負債

### 【intent の根因・高確度】シグナル引数不一致（`app/screenshot_editor/ui/panels.py`）

`AdjustmentPanel` と `PresetPanel` はいずれも引数なしの `changed = Signal()` を宣言しているが、上流の Qt シグナル（`int` を伴う）を `self.changed.emit` へ直結している:

- `AdjustmentPanel.__init__`: 各スライダーで `slider.valueChanged.connect(self.changed.emit)`（`QSlider.valueChanged` は `int` を伴って発火）。
- `PresetPanel.__init__`: `self._combo.currentIndexChanged.connect(self.changed.emit)`（`QComboBox.currentIndexChanged` は `int` を伴って発火）。

Qt が上流の `int` 引数を `self.changed.emit` にそのまま渡すため、引数なしで宣言した `changed` に余分な位置引数を渡す形になり、PySide6 実行時にコンソールへエラー（シグネチャ不一致に伴う TypeError/警告）が出る。スライダー操作（調整）とコンボ選択（プリセット/フィルタ）の両方が該当し、ユーザー報告「調整やフィルタ、プリセットを選択するとコンソールにエラー」と一致する。`main_window.py` の `self._adjust.changed.connect(self._update_preview)` / `self._preset.changed.connect(self._update_preview)` を介したプレビュー更新経路上で顕在化する。

- **修正の方向性（実装は後段ステージ）**: `changed = Signal(int)` に合わせるか、`emit` を引数を捨てるスロットで包む（例 `.connect(lambda *_: self.changed.emit())`）。`reset()` は `self.changed.emit()` を引数なしで呼ぶため、後者の「包む」方式なら現行 `Signal()` と `reset()` の両立を維持できる。blast radius は `ui` 層に限定できる見込み。

### UI 層の無試験（回帰すり抜け）

カバレッジ対象が `core`/`io` のみのため、`ui` のシグナル配線・プレビュー更新は緑のゲートを通過してもすり抜ける。本 intent がその典型。回帰防止には UI シグナル配線テストの追加が望ましいが、PySide6（GUI）依存のためテスト環境整備が必要。project.md の Mandated（依存方向 `ui -> core -> io`、`core` は GUI 非 import）を壊さないこと。

### `batch_dialog.py` のスレッド後始末

`_on_finished` で `QThread.quit()/wait()` を行うが、`_choose_and_run` で例外が起きた場合のスレッド後始末が明示的でない（本 intent とは無関係の将来的な debt シグナル）。

### その他

TODO/FIXME/HACK や不当な抑制コメントは実質なし（`run_checks.py` の `# noqa: S603`、`batch_dialog.py` の `# noqa: N802` は正当な限定抑制）。ハードコード資格情報・外部 URL・God クラスは未検出。
