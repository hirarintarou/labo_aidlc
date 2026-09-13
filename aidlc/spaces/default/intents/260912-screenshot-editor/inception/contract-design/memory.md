<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->

## Deviation
- 2026-09-12T15:30:00Z contract-design はスキップ。理由：本システムは単一ユニット `screenshot-editor` で、ユニット間の境界が存在せず（依存DAGは1ノード・エッジなし）、外部に公開・消費されるAPIも持たない（ローカル完結のデスクトップアプリ）。ステージ条件「Skip only for a single self-contained unit with no inter-unit boundaries and no externally consumed API」に合致。内部コンポーネント間インターフェース（ui→core→io）はFunctional Designで扱う。
