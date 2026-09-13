# NFR Requirements — Questions (screenshot-editor)

## Sources

- [scope] Workflow-selected scope: `mvp`.

> 自律モードで進行中。NFRは requirements.md の NFR1-6 で確定済みで、本ステージはそれを受け入れ可能な目標に具体化する。新規の人間向け質問はなく、技術スタックの選定はプラクティス（org.md Code Style「言語標準に従う」）と要件（実現しやすい技術におまかせ）に基づき自律的に決定した。

## 自律的に解決した事項（Construction autonomous grant）

- Q1. 技術スタックの選定 → Python 3.11+ / PySide6 / Pillow / pytest / ruff+black / PyInstaller（tech-stack-decisions.md参照）。根拠：画像処理の容易さ・Windows動作・個人開発の手軽さ・ui→core→io分離との相性。
- Q2. 性能目標 → 一般的なPNG/JPEGで体感即時（プレビュー≤300ms目安）、正式SLAは設けない（performance-requirements.md）。
- Q3. セキュリティ範囲 → 依存固定・未検証画像の安全デコード・非破壊保存に集約、Web/サーバ系対策は非該当（security-requirements.md）。

[Answer]: 自律モードにより上記のとおり決定（新規の人間質問なし）

---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]:
