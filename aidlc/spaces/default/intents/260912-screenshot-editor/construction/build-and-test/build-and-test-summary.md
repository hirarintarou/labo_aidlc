# Build and Test Summary — screenshot-editor（mvp）

単一ユニット（screenshot-editor）の Construction 成果物に対するビルド・テストの総括。
Test Strategy: Standard。実行日: 2026-09-13。

## 全体ビルドステータスと前提

- 前提: Windows / uv（Python 3.11 自動取得）。`app/` で `uv sync --extra dev`。
- ビルド: 依存インストール成功、`compileall` 成功、`uv lock --check` 整合。
- 外部サービス・環境変数・ネットワーク不要（ローカル完結・オフライン）。

## テスト種別インベントリ（生成した指示書）

| ファイル | 種別 | 生成理由 |
|----------|------|----------|
| build-instructions.md | ビルド/環境 | 必須 |
| integration-test-instructions.md | 統合（レイヤー境界） | Standard strategy |
| security-test-instructions.md | セキュリティ | SEC-1〜5 の NFR が存在（軽量・比例） |
| performance-test-instructions.md | 性能 | PERF-1〜4 の NFR が存在（形式試験は Out of Scope、設計確認） |

単体テストは Code Generation でユニット単位に生成済み（`app/tests/`、pytest）。

## ユニットごとのカバレッジ期待

- 単一ユニット screenshot-editor: 中核ロジック層（core/io）で 80% ライン下限。実績 90.15%。

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|-----------|--------|----------|--------|----------|--------------|---------|
| COV-CORE-IO | Testing Contract / team.md | core/io カバレッジ ≥ 80% | 90.15% | pytest --cov（50 passed） | build-and-test | Met |
| TEST-GREEN | team.md Testing Posture | スイート全体 green | 50 passed / 0 failed | pytest 出力 | build-and-test | Met |
| SEC-1 | security-requirements.md | 外部送信なし | NET import 0 件 | `NET IMPORTS: []` | build-and-test | Met |
| SEC-2 | security-requirements.md | 安全デコード・非クラッシュ | 異常系テスト合格 | test_image_io.py | build-and-test | Met |
| SEC-3 | security-requirements.md | 非破壊アトミック保存 | 非破壊/連番テスト合格 | test_image_io.py | build-and-test | Met |
| SEC-4 | security-requirements.md | 依存固定・ロックコミット | lock 整合 | `uv lock --check` | build-and-test | Met |
| SEC-5 | security-requirements.md | ruff S 有効・違反なし | 違反 0 | `uv run ruff check .` | build-and-test | Met |
| PERF-1 | performance-requirements.md | プレビュー体感即時（形式試験 Out of Scope） | 設計反映を確認 | ui/main_window.py | build-and-test（設計確認） | Met |
| PERF-2 | performance-requirements.md | 開く体感 ≤1s（Out of Scope） | 設計反映を確認 | ui/main_window.py | build-and-test（設計確認） | Met |
| PERF-3 | performance-requirements.md | 保存体感 ≤1s（Out of Scope） | 設計反映を確認 | io/image_io.py | build-and-test（設計確認） | Met |
| PERF-4 | performance-requirements.md | バッチ UI 非ブロック・進捗 | 設計反映を確認 | ui/batch_dialog.py | build-and-test（設計確認） | Met |

すべての適用対象ターゲットが `Met`。`N/A` 行なし（適用対象ターゲットが存在するため）。

## Readiness Assessment

- build-ready: Yes
- test-ready: Yes（50 passed、core/io 90.15%）
- deployment-ready（ローカルビルド/配布）: Yes（PyInstaller 手順を記載）

## 既知の限界・残課題

- クレジット GUI 編集は未提供（core は実装済み。UI 拡充候補、レビュー R-01）。
- processor.py の一部分岐は未カバー（下限は充足。補強候補、R-02）。
- GUI 自動 E2E はヘッドレス制約で未実施。骨組み疎通は io 統合テストで担保。
- 性能は形式的な自動計測を行わない（要件どおり）。実機での手動体感確認を推奨。
