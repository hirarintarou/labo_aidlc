# Delivery Planning — Questions

## Sources

- [scope] Workflow-selected scope: `mvp`.

> ここでは Construction（実装）の進め方を決めます。「Bolt（ボルト）」＝ 一区切りの実装のかたまりで、終わると何か動くものができる単位です。単一ユニット・個人開発なので計画はシンプルになります。

---

## Q1. 何から作りますか（最初のBolt）

確定プラクティスでは「ウォーキングスケルトン（＝端から端まで動く最小の骨組み）を最初に作る」方針です。これに沿うと、最初のBoltは「画像を開く→無加工→非破壊保存が通る骨組み（US0.1）」になります。

- A. その方針でよい（骨組みを最初のBoltにして、以降で各機能を足す）
- B. 別の進め方がよい（記入してください）
- X. Other (please specify)

[Answer]:A.

---

## Q2. Bolt（実装のかたまり）の大きさはどれくらいがよいですか

- A. 機能ごとに小さめのBoltに分ける（例：骨組み→基本補正→画質→フィルタ→トリミング/リサイズ→クレジット→バッチ）
- B. まとめて少数の大きなBoltにする（例：骨組み→単体編集一式→バッチ）
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q3. Construction（実装）の進め方（体制）はどちらですか

- A. このセッションで私（AI）が1つずつ作り、あなたが都度承認する（個人開発の標準）
- B. 複数チームで分担する（※複数ユニットが前提。本件は単一ユニットなので通常はA）
- X. Other (please specify)

[Answer]:A.

---

## Q4. 実装で特に不安な点・優先して確かめたい点はありますか

- A. 特にない（骨組みで疎通を確かめる方針で十分）
- B. ある（記入してください）
- X. Other (please specify)

[Answer]:A.

---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
