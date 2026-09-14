<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-14 — bugfix scope・Minimal 深度。RE で根因が高確度に特定済み（panels.py のシグナル引数不一致）。要件はバグ症状の解消に限定し、機能追加はしない。project-description は末尾が切れているが（「…コンソールに」）、症状は CodeKB とソースで裏取り済み。

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-14 — advisory レビュー（product-lead）は READY。Minor 所見 3 件（FR1.1/1.2 の観測手段、NFR3 の症状への絞り込み、FR3.1 の観測点具体化）を取り込み、testability を強化。over-scope は回避。

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
