# Feasibility & Constraints — Clarifying Questions

## Sources

- [desc] Initial description: "finalfantasy14というゲームのキャラクターのスクリーンショット画像があります。これを公開する前に綺麗に加工するツールを作りたい"
- [scope] Workflow-selected scope: `mvp`.

> 前ステージ（Intent Capture）で確定した事項：課題＝画質補正・複数枚バッチ処理・多彩な加工手段、利用者＝個人、成功基準＝本人の満足、利用形態＝デスクトップアプリ、クレジット付与＝FF14公式ガイドライン遵守目的。ここでは実現可能性・制約・リスクの観点で不足を確認します。

---

## Q1. どのOS・環境で動けばよいですか（技術制約）

デスクトップアプリとのことですが、動かしたい環境を教えてください。実装技術の選定に影響します。

- A. Windows のみ
- B. macOS のみ
- C. Windows と macOS の両方
- D. こだわりはない／おすすめに任せたい / Not yet defined
- X. Other (please specify)

[Answer]:A.

---

## Q2. 実装技術やツールの好み・制約はありますか（技術スタック）

使いたい／使いたくないプログラミング言語やフレームワーク、あるいはあなたが扱いやすい技術があれば教えてください（なければ「おまかせ」で構いません）。

- A. 特にこだわりはない。実現しやすい技術におまかせ
- B. できれば Python 系がよい
- C. できれば Web技術（JavaScript/TypeScript, Electron等）がよい
- D. その他の希望がある（記入してください）
- X. Other (please specify)

[Answer]:A.

---

## Q3. 扱う画像の形式・サイズの想定はありますか（入出力制約）

FF14のスクリーンショットが中心と思われますが、入出力で意識しておきたい点はありますか。

- A. 一般的なPNG/JPEGが読み書きできれば十分
- B. 高解像度（4K等）の大きな画像も快適に扱いたい
- C. 特定の形式（記入してください）
- D. まだ決めていない / Not yet defined
- X. Other (please specify)

[Answer]:A.

---

## Q4. 加工前の元画像・加工結果の保存方針に希望はありますか（データの扱い）

個人利用・ローカル動作を想定していますが、データの扱いで意識したい点はありますか。

- A. すべてローカルPC内で完結（クラウド送信なし）でよい
- B. 元画像は上書きせず、加工結果を別ファイルとして保存したい
- C. AとBの両方（ローカル完結かつ非破壊で別保存）
- D. まだ決めていない / Not yet defined
- X. Other (please specify)

[Answer]:C.

---

## Q5. FF14スクリーンショットの公開ガイドライン遵守について、ツールで担保したい範囲はありますか（コンプライアンス）

FF14のスクリーンショットはスクウェア・エニックスの著作物を含みます。前ステージでクレジット付与は「公式ガイドライン遵守目的」と確定しました。ツールとして意識したい範囲を教えてください。

- A. クレジット（出典・コピーライト等）を任意で付与できれば十分。それ以上の制約チェックは不要
- B. 過度な改変を避ける等、ガイドライン上の注意点も文書やUIで案内してほしい
- C. よく分からないので、注意点があれば教えてほしい / Not identified
- X. Other (please specify)

[Answer]:A.

---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
