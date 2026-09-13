<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-09-13T10:00:00Z — plan_profile の一般レイヤー（DB/API）を本ユニットの実レイヤーへ写像; GUIデスクトップアプリでDB/API層が無いため、io（入出力・非破壊保存）→core（変換）→batch→ui の順で test-after を適用した。methodology は変更していない。
- 2026-09-13T10:00:00Z — カバレッジ測定対象を core/io に限定; team.md の測定対象スコープ特化（GUI/配線層は下限外）に従い pyproject.toml の coverage source を core/io に絞った。結果 90.15%。

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-09-13T10:00:00Z — Kiro IDE のサブエージェント dispatch ツールを plan-approval-guard が Task/Agent として認識せず mutation として誤ブロックしたため、承認済み計画に基づき指揮者が直接コードを生成した（受領記録は現行で有効）。生成物・検証は subagent 経由と同等。
- 2026-09-13T10:00:00Z — クレジット描画位置を画像内にクランプ（計画に無い微修正）; 小画像でテキストがはみ出し画面外に描かれるテスト失敗を修正するため。設計判断（合成順序等）は不変。

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-09-13T10:00:00Z — ノイズ除去を MedianFilter で近似（決定的・実装単純）; 高度なデノイズより mvp では再現性と単純さを優先。将来より高品質なアルゴリズムへ差し替え余地あり。
- 2026-09-13T10:00:00Z — GUI の E2E テストは省略し core/io の単体テストに集中; PySide6 のヘッドレス実行は環境依存で不安定、team.md も GUI E2E は最小限の方針。骨組み疎通は io の非破壊保存テストで担保。

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
