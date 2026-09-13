# Test Results — screenshot-editor（mvp）

Build and Test の実行結果（`app/` ディレクトリ、uv 経由）。実行日: 2026-09-13。

## Build ステータス

- 依存インストール: `uv sync --extra dev` 成功（PySide6==6.7.2 / Pillow==10.4.0 ほか、`uv.lock` 整合）
- ビルド検証: `uv run python -m compileall -q screenshot_editor` 成功（全モジュール byte-compile OK）
- 依存ロック整合: `uv lock --check` 成功（ドリフトなし）

## テスト結果

| 項目 | 値 |
|------|----|
| 実行コマンド | `uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80` |
| 合計 | 50 |
| 成功 | 50 |
| 失敗 | 0 |
| スキップ | 0 |
| 中核層カバレッジ（core/io） | 90.15%（下限 80% 充足） |

### 失敗詳細

なし（全件成功）。

### カバレッジ内訳（中核ロジック層）

| モジュール | Cover |
|-----------|-------|
| core/edit_settings.py | 100% |
| core/presets.py | 96% |
| core/processor.py | 88% |
| io/image_io.py | 87% |
| **TOTAL（core/io）** | **90.15%** |

GUI / 配線層（ui）は team.md の測定対象スコープ特化によりカバレッジ下限の対象外。

### 実行したコマンド一覧（重複排除）

- 単体・統合（同一 `tests/` 一括、単一ユニットのため 1 コマンド）:
  `uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80` → 50 passed
- Lint（SEC-5）: `uv run ruff check .` → All checks passed
- Format: `uv run black --check .` → 差分なし
- ネットワーク非依存（SEC-1）: `NET IMPORTS: []`
- 依存ロック（SEC-4）: `uv lock --check` → 整合

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|-----------|--------|----------|--------|----------|--------------|---------|
| COV-CORE-IO | code-generation-plan.md Testing Contract / team.md Testing Posture | core/io ラインカバレッジ ≥ 80% | 90.15% | pytest --cov 出力（50 passed） | build-and-test | Met |
| TEST-GREEN | team.md Testing Posture | ローカルでスイート全体が green | 50 passed / 0 failed | pytest 出力 | build-and-test | Met |
| SEC-1 | security-requirements.md | ネットワーク I/O を持たない（外部送信なし） | 該当 import 0 件 | `NET IMPORTS: []` | build-and-test | Met |
| SEC-2 | security-requirements.md | 未検証画像を安全デコード、破損/非対応/巨大は型付きエラー・非クラッシュ | 異常系テスト合格 | test_image_io.py（0バイト/破損/非対応/巨大） | build-and-test | Met |
| SEC-3 | security-requirements.md | 非破壊アトミック保存・元画像不変・中途出力なし | 非破壊/連番/中途出力なしテスト合格 | test_image_io.py | build-and-test | Met |
| SEC-4 | security-requirements.md | 依存をバージョン固定・ロックをコミット | 固定済み・lock 整合 | `uv lock --check` / pyproject.toml / uv.lock | build-and-test | Met |
| SEC-5 | security-requirements.md | リンタのセキュリティ系ルール（ruff S）有効・違反なし | S ルール有効・違反 0 | `uv run ruff check .` All checks passed | build-and-test | Met |
| PERF-1 | performance-requirements.md | プレビュー反映が体感即時（目安 ≤300ms、形式試験は Out of Scope） | 設計反映を確認（縮小版プレビュー適用、原寸は保存時のみ） | performance-test-instructions.md / ui/main_window.py（_PREVIEW_MAX, _update_preview） | build-and-test（設計確認） | Met |
| PERF-2 | performance-requirements.md | 開くのが体感 ≤1s（形式試験は Out of Scope） | 設計反映を確認（縮小プレビュー生成） | performance-design.md / ui/main_window.py | build-and-test（設計確認） | Met |
| PERF-3 | performance-requirements.md | 保存が体感 ≤1s（形式試験は Out of Scope） | 設計反映を確認（原寸1パス適用＋アトミック保存） | io/image_io.py save_nondestructive | build-and-test（設計確認） | Met |
| PERF-4 | performance-requirements.md | バッチは枚数比例・UI 非ブロック・進捗表示 | 設計反映を確認（QThread ワーカー＋進捗シグナル） | ui/batch_dialog.py（_BatchWorker） | build-and-test（設計確認） | Met |

> PERF-1〜4 は performance-requirements.md により「正式な性能試験は行わない（体感的に実用的を基準）」と
> 明記された Out of Scope 目標であり、自動化された数値計測の対象外。応答性を担保する設計アプローチが
> 実装に反映されていることの静的確認をもって Met とした（後続の性能検証ステージは本スコープで未スケジュール）。
> 任意で実機の手動体感確認を推奨（performance-test-instructions.md 参照）。

## Readiness Assessment

- build-ready: Yes（依存インストール・byte-compile 成功）
- test-ready: Yes（50 passed、core/io 90.15%）
- deployment-ready（ローカルビルド/配布）: Yes（PyInstaller 手順を build-instructions.md / README に記載）

すべての適用対象ターゲットが `Met`。`Not Met`・`Unverified` のターゲットなし。ビルド・テストの
失敗コマンドなし。失敗ラダー（loop-back / halt-and-ask）は発火せず、`## Loop-Back Log` は不要。

## 既知の限界・残課題

- クレジット付与の位置/サイズ/不透明度の GUI 編集は未提供（core は実装済み）。UI 拡充候補（レビュー R-01）。
- processor.py の一部分岐は未カバー（core/io 全体 90%、下限は充足）。将来のテスト補強候補（R-02）。
- GUI の自動 E2E はヘッドレス制約により未実施。骨組み疎通は io 統合テストで担保。
