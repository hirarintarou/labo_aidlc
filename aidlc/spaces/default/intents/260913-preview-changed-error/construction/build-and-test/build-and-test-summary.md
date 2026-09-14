# ビルド・テストサマリ — preview-changed-error（bugfix / Minimal）

## 全体ステータスと前提

- ビルド（相当）: 成功（lint / format / import 健全性すべて green）。
- テスト: 全 55 件 pass、失敗 0。core/io カバレッジ 90%（80% floor 超過）。
- 前提: Python 3.11 / `app/.venv` / `QT_QPA_PLATFORM=offscreen`。ローカル・オフライン完結。

## テスト種別インベントリ

- **単体テスト**: Code Generation で per-stage 生成済み（`app/tests/`）。本バグの回帰テスト `test_ui_panels.py`（5 件）を含む。
- **統合テスト指示 / 性能テスト指示 / セキュリティテスト指示**: **N/A（生成せず）**。本 intent は Minimal 戦略の bugfix であり、団体規約（Testing Posture）に従い追加テスト指示ファイルは生成しない。NFR の性能・セキュリティ設計成果物も bugfix でスキップ済みのため対象測定目標が存在しない。

## カバレッジ期待

- カバレッジ下限 80% は team.md により `core`/`io` に限定。実測 90%（`edit_settings` 100% / `presets` 96% / `processor` 88% / `image_io` 87%）。
- `ui` 層はカバレッジ計測対象外（team.md の測定対象スコープ特化）。本バグ修正の対象層だが、bugfix floor の「対象回帰テスト追加」は `test_ui_panels.py` で満たす。

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| COV-core-io | team.md > Testing Posture（80% 下限を core/io に限定） | ≥ 80% line coverage (core/io) | 90% | `pytest --cov`（TOTAL 90%, 55 passed） | build-and-test | Met |
| REG-bugfix | org.md/team.md 由来の bugfix scope floor（対象回帰テスト） | 本バグの回帰テストを 1 件以上追加、既存スイート green | 回帰 5 件追加・全 55 件 green | `app/tests/test_ui_panels.py`、`pytest -q` | build-and-test | Met |
| LINT | pyproject.toml `[tool.ruff]`（S 規則含む） | ruff / black clean | clean（ruff: All checks passed / black: 24 files unchanged） | `ruff check .` / `black --check .` | build-and-test | Met |

（NFR performance/security の測定目標はソースインベントリに存在しないため、それらに対する行は設けない。上記 3 目標がこのステージの適用対象。）

## Readiness 評価

- **build-ready**: Yes（lint/format/import すべて green）
- **test-ready**: Yes（全テスト green、カバレッジ floor 超過）
- **deployment-ready**: Yes（次ステージ Deployment Pipeline へ）

## 既知の制約・残項目

- リモート CI は未使用（team.md の方針）。ローカルゲート（pre-commit / pre-push / `run_checks.py`）でテスト green＋カバレッジ下限を機械強制する構成は既存。今回の回帰テストはヘッドレス実行（`QT_QPA_PLATFORM=offscreen`）を要する点を `unit-test-instructions.md` に記録済み。
