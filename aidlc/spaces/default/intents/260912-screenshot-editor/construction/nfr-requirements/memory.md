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

## Interpretation
- 2026-09-13T09:11:00Z 自律モード。NFRは requirements.md の NFR1-6 で確定済みなので、それを具体的な受け入れ可能な目標に落とす。技術スタックをここで選定：Python 3.x + PySide6(Qt) + Pillow(画像処理) + pytest。根拠：成熟した画像処理(Pillow)、Windowsで安定動作するGUI(Qt/PySide6)、PyInstallerで単一exe配布可、個人開発で扱いやすい、ui→core→io分離もモジュールで自然に実現。
## Tradeoff
- 2026-09-13T09:11:00Z Electron/Tauri(Web技術)やC#/WPFも候補だが、画像処理の容易さ(Pillow)と個人開発の手軽さでPythonを選択。性能面は一般的PNG/JPEG想定で十分。

## Open question
- 2026-09-13T09:18:00Z [code-generationで確定] 保存時に同名の `_edited` ファイルが既に存在する場合の挙動（上書き/連番付与/確認）。非破壊保証を損なわないポリシーをコード生成で明示する（レビューR-02）。
- 2026-09-13T09:18:00Z [code-generationで確定] バッチ/保存の別スレッド実行時のスレッド境界（Pillowオブジェクト受け渡し・PySide6シグナルでの進捗更新）（レビューR-03）。
