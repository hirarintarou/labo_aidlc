# Quality Gates — screenshot-editor（mvp）

`main` への統合（および pre-push）前に満たすべき品質ゲート。すべてローカルで機械的に
強制する（team.md CI ゲート Q5=A）。手動実行のみには依存しない。

## ゲート定義

| Gate ID | 内容 | 判定コマンド（`app/` 内） | 強制ポイント | 実績 |
|---------|------|---------------------------|-------------|------|
| QG-1 フォーマット | black 準拠（差分なし） | `uv run black --check .` | pre-commit | Pass（差分なし） |
| QG-2 Lint/セキュリティ | ruff 違反なし（`S`=flake8-bandit 相当を含む） | `uv run ruff check .` | pre-commit | Pass（All checks passed） |
| QG-3 テスト green | テストスイート全体が成功 | `uv run pytest tests/` | pre-push | Pass（50 passed / 0 failed） |
| QG-4 カバレッジ下限 | 中核ロジック層（core/io）ラインカバレッジ ≥ 80% | `uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-fail-under=80` | pre-push | Pass（90.15%） |
| QG-5 依存ロック整合 | `pyproject.toml` と `uv.lock` にドリフトがない | `uv lock --check` | pre-push | Pass（整合） |

## 運用ルール

- **下限は緩めない**: QG-4 のカバレッジ下限（80%）や QG-1〜3 の合格基準を、通過のために
  引き下げ・無効化しない（team.md / org.md Testing Posture）。満たせない場合はギャップを是正する。
- **GUI/配線層はカバレッジ対象外**: QG-4 の測定対象は core/io に限定（team.md の測定対象スコープ特化）。
  GUI（ui 層）は E2E 最小限の方針で、カバレッジ下限の対象外。
- **セキュリティ**: QG-2 の ruff `S` ルールでソースレベルのセキュリティを担保。ネットワーク非依存
  （外部送信なし）はコードレビュー/静的確認で維持（build-and-test の SEC-1 検査）。
- **マージ**: ゲート通過後、短命ブランチを `main` へ squash-merge（trunk-based）。

## Build and Test 記録コマンドとの対応

Build and Test（test-results.md）で実行・green を確認した以下のコマンドを、そのまま品質ゲートとして固定する:

- `uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80`（QG-3, QG-4）
- `uv run ruff check .`（QG-2）
- `uv run black --check .`（QG-1）
- `uv lock --check`（QG-5）

これらは `app/run_checks.py` と `app/.pre-commit-config.yaml` に実装済みで、CI（ローカルゲート）が
Build and Test の記録コマンドを強制することを保証する。

## Sources

- team.md（Testing Posture / CI ゲート）、org.md（Testing Posture: 下限を緩めない）
- test-results.md / build-and-test-summary.md（実績値）
- 実体: app/run_checks.py, app/.pre-commit-config.yaml, app/pyproject.toml

## Assumptions & Open Questions

None.
