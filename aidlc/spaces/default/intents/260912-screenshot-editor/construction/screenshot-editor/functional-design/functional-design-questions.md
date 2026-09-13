# Functional Design — Questions (screenshot-editor)

## Sources

- [scope] Workflow-selected scope: `mvp`.

> 要件・ユーザーストーリー・ドメイン設計で振る舞いはほぼ確定済み。機能設計として詰める細部を確認します（技術スタックはこの次のコード生成の計画で選定します）。

---

## Q1. リサイズのアスペクト比は既定で保持しますか

- A. 既定で保持する（縦横比を保ったままリサイズ。解除も可能）
- B. 既定で保持しない（幅・高さを自由指定）
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q2. トリミングは自由な矩形選択でよいですか（比率固定は不要か）

- A. 自由な矩形でよい（mvpは固定比率プリセット不要）
- B. 固定比率（16:9等）も選べるようにしたい
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q3. 加工の適用順序（複数の調整を重ねたときの順番）に希望はありますか

- A. おまかせ（自然な順序：補正→画質→フィルタ→トリミング/リサイズ→クレジット）
- B. 希望がある（記入してください）
- X. Other (please specify)

[Answer]:A.

---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
