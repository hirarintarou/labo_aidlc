# テスト結果 — preview-changed-error（bugfix / Minimal）

## ビルドステータス

- lint: `ruff check .` → `All checks passed!`（成功）
- format: `black --check .` → 24 files unchanged（成功）
- import 健全性: `import screenshot_editor.ui.panels` → 成功
- 総合: **成功**

## テスト結果

- 実行コマンド（`app/` ディレクトリ、`.venv` の python、`QT_QPA_PLATFORM=offscreen`）:
  - `python -m pytest -q`
  - `python -m pytest --cov --cov-report=term-missing`
- 合計: **55**、passed: **55**、failed: **0**、skipped: 0
- うち本バグの回帰テスト `tests/test_ui_panels.py`: 5 件すべて pass。

### 失敗の詳細

- なし。

## カバレッジレポート（core/io、80% 下限）

| Module | Stmts | Miss | Cover |
|---|---|---|---|
| screenshot_editor/core/edit_settings.py | 46 | 0 | 100% |
| screenshot_editor/core/presets.py | 24 | 1 | 96% |
| screenshot_editor/core/processor.py | 113 | 14 | 88% |
| screenshot_editor/io/image_io.py | 91 | 12 | 87% |
| **TOTAL** | **274** | **27** | **90%** |

下限 80% に対し 90%。**Met**。

## Target Verification Matrix（最終）

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| COV-core-io | team.md > Testing Posture | ≥ 80%（core/io） | 90% | `pytest --cov` 出力 | build-and-test | Met |
| REG-bugfix | bugfix scope floor | 回帰テスト 1 件以上＋既存 green | 5 件追加・55/55 green | `tests/test_ui_panels.py` / `pytest -q` | build-and-test | Met |
| LINT | pyproject.toml `[tool.ruff]` | ruff/black clean | clean | `ruff check .` / `black --check .` | build-and-test | Met |

`Pending` 残なし。適用対象すべて **Met**。失敗述語（コマンド失敗、または適用対象が Not Met / Unverified）に該当なし → **成功**。
