# Integration Test Instructions — screenshot-editor（mvp）

Standard strategy の統合テスト方針。本プロジェクトは単一ユニット（screenshot-editor）だが、
内部は ui → core → io + batch の複数レイヤーに分かれる。重要な**レイヤー境界**の結合を検証する。

## フレームワーク・実行

- pytest（`uv run` 経由）。`app/` ディレクトリで実行。
- 統合テストは既存のユニットテストと同じ `tests/` に含める（単一ユニットのため分離不要）。

```
uv run pytest tests/ -q
```

## 検証する結合ポイント（key boundaries）

1. **骨組み疎通（io 境界、US0.1）— 最重点 P0**
   開く → （無加工で）保存 が io を貫通して別ファイルを出力し、元画像がバイト列・mtime
   ともに不変であること。`tests/test_image_io.py` の非破壊・ラウンドトリップテストが
   この結合を担保する（`load_image` → `save_nondestructive` の連結）。

2. **core → io の結合（バッチ経路の一部）**
   `batch_processor.process_files` が io（load/save）と core（processor.apply）を
   連結して呼び、失敗をスキップして継続し件数を集計すること。
   `tests/test_batch_processor.py` が実ファイル（pytest tmp_path）で検証。

3. **core の合成順序の一貫性**
   `processor.apply` が固定合成順序で複数変換を連結適用し、恒等設定で入力一致・
   同一設定で決定的同一出力になること。`tests/test_processor.py` が担保。

4. **プリセット → core の結合**
   プリセット指定が `processor.apply` を通じて決定的に反映されること。
   `tests/test_presets.py` が担保。

## UI 層の結合について

GUI（PySide6）の E2E は最小限に留める（team.md）。UI は core/io をワーカースレッド経由で
呼ぶ薄い配線層であり、ロジックは core/io 側のテストで担保済み。ヘッドレス環境での
GUI 自動起動テストは行わず、`uv run python -m compileall -q screenshot_editor` による
import/コンパイル健全性の確認で代替する。骨組みの端から端（開く→加工→非破壊保存）の
振る舞いは (1) の io 統合テストが最小疎通として担保する（Walking Skeleton と共用）。

## 期待カバレッジ

- 中核ロジック層（core/io）で 80% ライン下限（`--cov-fail-under=80`）。統合経路（batch）も
  この測定対象に含む。

## テストデータ

- 合成フィクスチャ画像（`tests/conftest.py` がプログラム生成）。実ファイル I/O は tmp_path。

## Sources

- functional-spec.md（WF1/WF2/WF3・状態遷移）
- team.md（レイヤー境界 ui→core→io、GUI E2E は最小限）
- code-summary.md（実装済みの結合点）

## Assumptions & Open Questions

- 単一ユニットのためクロスユニット統合は存在しない。結合検証はレイヤー境界に対して行う。
