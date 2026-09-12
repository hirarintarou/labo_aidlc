# Requirements Analysis — Clarifying Questions

## Sources

- [desc] Initial description: "finalfantasy14というゲームのキャラクターのスクリーンショット画像があります。これを公開する前に綺麗に加工するツールを作りたい"
- [scope] Workflow-selected scope: `mvp`.

> 多くは前ステージで確定済み（機能セット・UI・非破壊保存・ローカル完結・Windows専用・プラクティス）。ここでは要件を「テスト可能な形」にするための細部だけを確認します。

---

## Q1. フィルタ／プリセットは、mvpではいくつくらい用意しますか（範囲の線引き）

「加工手段が広がりすぎるリスク」を抑えるため、mvpのプリセット数の目安を決めておきたいです。

- A. 少数（3〜5種類程度）の代表的なプリセットで十分
- B. 中程度（6〜10種類程度）
- C. 数にはこだわらない／おすすめに任せる
- D. まだ決めていない / Not yet defined
- X. Other (please specify)

[Answer]:B.

---

## Q2. 加工後ファイルの保存先・名前の既定はどうしますか（テスト可能にするため）

非破壊保存の具体を決めます。既定の挙動として近いものを選んでください。

- A. 元画像と同じフォルダに、末尾に接尾辞を付けて保存（例: `screenshot001_edited.png`）
- B. 元画像のフォルダ内の `edited/` サブフォルダにまとめて保存
- C. 保存のたびに保存先を選ぶ（既定は決めない）
- D. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q3. 出力の形式は選べるようにしますか

- A. 元画像と同じ形式で保存できれば十分（PNG→PNG、JPEG→JPEG）
- B. 保存時にPNG/JPEGを選べるようにしたい
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q4. バッチ処理で一部の画像が失敗したときの挙動はどうしますか

例：壊れた画像や非対応ファイルが混ざっていた場合。

- A. 失敗したファイルはスキップして残りを続行し、最後に「成功n件／失敗m件」を表示
- B. 失敗した時点で中断して知らせる
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q5. クレジット文字列に既定値を用意しますか

- A. 既定のテンプレート（例: 「© SQUARE ENIX」）を用意しつつ、自由に編集できるようにする
- B. 既定は空欄で、毎回自分で入力する
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q6. 「まず使える」と言える最小の完成イメージ（受け入れの目安）はどれですか

mvpとして「これができれば一旦OK」と判断する目安を確認します（複数選択可）。

- A. 1枚を開いて基本補正・トリミング・クレジットを付けて非破壊保存できる
- B. フィルタ／プリセットを適用できる
- C. 同じ設定で複数枚をバッチ保存できる
- D. 上記すべてが一通り動く
- X. Other (please specify)

[Answer]:A.とB.

---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
