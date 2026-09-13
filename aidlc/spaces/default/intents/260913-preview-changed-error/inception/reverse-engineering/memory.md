<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-14 — bugfix scope のため走査は `app/`（screenshot-editor 本体）を deep、`.kiro/`・`aidlc/` はワークフロー scaffolding として shallow に区分。root repo 識別子は `aidlc`。
- 2026-09-14 — developer link がバグ根因を高確度で特定: `app/screenshot_editor/ui/panels.py` の `AdjustmentPanel`/`PresetPanel` が引数なし `changed = Signal()` を宣言しつつ `QSlider.valueChanged`（int）/`QComboBox.currentIndexChanged`（int）を `self.changed.emit` に直結。PySide6 実行時にシグネチャ不一致でコンソールエラー。ユーザー報告症状と一致。requirements-analysis へ引き継ぐ。

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-14 — codekb-snapshot の `--paths app` は fingerprint 不可（tool は project-root repo で `./` のみ受理）。full 走査の `./` を採用。

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-09-14 — `ui/` 層に自動テストが皆無、カバレッジ計測対象も core/io のみ。回帰防止のため UI シグナル配線テストの追加是非を後段（build-and-test）で判断する。
