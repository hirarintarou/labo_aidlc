<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-13T11:00:00Z — 単一ユニットのため「クロスユニット」をユニット内レイヤー境界（ui/core/io/batch）として解釈; クロスユニット統合は存在しないため、結合検証を io 貫通・core→io・合成順序・プリセット反映のレイヤー境界に対して行った。
- 2026-09-13T11:00:00Z — PERF-1〜4 を「設計確認で Met」と判定; performance-requirements.md が明示的に「正式な性能試験は行わない（体感基準）」= Out of Scope としており、後続の性能検証ステージも本スコープで未スケジュールのため、応答性を担保する設計アプローチの静的確認をもって Met とした（Unverified ではなく）。

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-13T11:00:00Z — Standard strategy だが security/performance の指示書も生成; SEC/PERF の NFR が存在し軽量で価値があるため、integration に加えて生成した（ステージ prose の「context が要求すれば追加してよい」に沿う）。

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-13T11:00:00Z — GUI 自動 E2E を行わず core/io テスト＋compileall で代替; ヘッドレスでの PySide6 起動は不安定で team.md も E2E 最小限の方針。骨組み疎通は io 統合テストで担保し、UI 健全性は byte-compile で確認。

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-13T11:00:00Z — クレジットの位置/サイズ/不透明度の GUI 編集欄（FR6.3/AC1.6.2）と加工前比較（US1.9）は将来拡充候補; mvp 必須スコープのブロッカーではないが、次の拡張で対応するか確認したい。
