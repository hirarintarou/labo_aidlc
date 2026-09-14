# ユニットテスト手順 — preview-changed-error（bugfix / zero-Unit）

## テストフレームワークと構成

- ランナー: pytest（`app/pyproject.toml` の `[tool.pytest.ini_options]`、`testpaths = ["tests"]`）。
- GUI 依存: PySide6 の UI ウィジェットを生成するため、ヘッドレス環境変数 `QT_QPA_PLATFORM=offscreen` を設定して実行する（ディスプレイ不要）。
- 追加ランタイム依存なし: `pytest-qt` は導入しない。テスト内（または `conftest.py`）で `QApplication` を 1 つだけ生成する session スコープのフィクスチャを用意する。
- 新規テストファイル: `app/tests/test_ui_panels.py`。

## このユニットのテスト実行コマンド（本ユニットにスコープ）

追加した回帰テストファイルのみを対象にする（プロジェクト全体の `pytest` は使わない）。`app/` ディレクトリで実行:

```bash
QT_QPA_PLATFORM=offscreen python -m pytest tests/test_ui_panels.py -q
```

Windows PowerShell の場合:

```powershell
$env:QT_QPA_PLATFORM = "offscreen"; python -m pytest tests/test_ui_panels.py -q
```

（このコマンドは最初の test-after サイクルの前に実行可能であること。runner 準備ステップで疎通を確認する。）

既存スイートの非退行確認（マージ前、`app/` ディレクトリ）:

```bash
QT_QPA_PLATFORM=offscreen python -m pytest -q
```

## カバレッジ目標

- 本バグ修正の対象層は `ui`（配線層）であり、team.md の測定対象スコープ特化により **80% ラインカバレッジ下限の対象外**（下限は `core`/`io` に限定）。したがって `ui` の追加テストはカバレッジ下限の判定対象ではない。
- ただし bugfix スコープ floor として、報告バグに対する**対象回帰テストを 1 つ以上**含めること、既存スイートを green に保つことは必須。

## モック / スタブ方針

- 実際の `AdjustmentPanel` / `PresetPanel` を offscreen の `QApplication` 上で生成し、`QSlider.setValue(...)` / `QComboBox.setCurrentIndex(...)` で実シグナルを発火させる（モックしない）。
- `changed` の購読側は、**引数を受け取らないスロット**（`def slot(): calls.append(True)` 等）を接続し、余分な位置引数が渡れば `TypeError` で失敗する形にする。これが回帰の機械的検知点（FR3.1 の合格条件）。

## テストデータ管理

- 画像ファイルは不要（パネル単体のシグナル配線検証のため）。`conftest.py` の既存フィクスチャは流用しない。
- `QApplication` はプロセスで 1 インスタンスのみ生成する（`QApplication.instance() or QApplication([])`）。
