# Unit ↔ Story Map — FF14 スクリーンショット加工ツール（mvp）

全ストーリーは単一ユニット U1（screenshot-editor / u1-screenshot-editor）に割り当てられる。

## Story Assignment

| Story ID | ストーリー | Unit ID | Directory |
|----------|-----------|---------|-----------|
| US0.1 | 骨組み（open→no-op→非破壊保存の疎通） | U1 | u1-screenshot-editor |
| US1.1 | 画像を開いてプレビュー | U1 | u1-screenshot-editor |
| US1.2 | 基本補正 | U1 | u1-screenshot-editor |
| US1.3 | 画質調整 | U1 | u1-screenshot-editor |
| US1.4 | フィルタ／プリセット | U1 | u1-screenshot-editor |
| US1.5 | トリミング・リサイズ | U1 | u1-screenshot-editor |
| US1.6 | クレジット付与 | U1 | u1-screenshot-editor |
| US1.7 | 非破壊保存 | U1 | u1-screenshot-editor |
| US1.8 | リセット | U1 | u1-screenshot-editor |
| US1.9 | 加工前と比較（Should・mvp外） | U1 | u1-screenshot-editor |
| US2.1 | バッチ一括適用 | U1 | u1-screenshot-editor |

## Cross-cutting Stories

- なし（単一ユニットのため、複数ユニットにまたがるストーリーは存在しない）。

## Story Implementation Order within U1

- 順序の確定はDelivery Planningで行うが、依存の実態としては US0.1（骨組み）を最初に通し、続いて US1.1（開く）→ 各加工（US1.2〜US1.6, US1.8）→ US1.7（保存）→ US2.1（バッチ）が自然な流れ。US1.9 はmvp外。

## Coverage Verification

- 全11ストーリー（US0.1, US1.1〜US1.9, US2.1）が U1 に割り当て済み。
- U1 には少なくとも1つ以上のストーリーがある（全ストーリーを保持）。

## Assumptions & Open Questions

None.
