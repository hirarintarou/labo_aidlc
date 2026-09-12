# Scope Definition & Prioritization — Clarifying Questions

## Sources

- [desc] Initial description: "finalfantasy14というゲームのキャラクターのスクリーンショット画像があります。これを公開する前に綺麗に加工するツールを作りたい"
- [scope] Workflow-selected scope: `mvp`.

> 前ステージ確定事項：個人利用・Windows専用・ローカル完結・非破壊保存のデスクトップアプリ。加工の柱＝画質補正／多彩な加工手段／複数枚バッチ処理／任意のクレジット付与。ここでmvpの機能境界と優先順位を確定します。

---

## Q1. mvpに「必ず入れたい」加工機能はどれですか（must-have、複数選択可）

まず動く最小限として、確実に入れたい機能を選んでください（select all that apply）。ここで選ばれたものがmvpの中心になります。

- A. 明るさ・コントラスト・彩度などの基本補正
- B. トリミング（切り抜き）・リサイズ
- C. シャープ化・ぼかし・ノイズ除去などの画質調整
- D. フィルタ／プリセット（ワンタッチで雰囲気を変える）
- E. クレジット／ウォーターマークの付与
- F. 複数枚を同じ設定でまとめて処理（バッチ）
- X. Other (please specify)

[Answer]:A.C.D.E.F.

---

## Q2. mvpでは「後回しでよい（nice-to-have）」機能はどれですか（複数選択可）

将来的にはほしいが、最初のバージョンには無くてもよい機能を選んでください（select all that apply）。

- A. 高度なフィルタ／エフェクト（多数のプリセット、細かな調整）
- B. 不要な写り込み（他プレイヤー名・UI等）の消去・修復
- C. レイヤー・テキスト追加などの本格編集
- D. 加工設定の保存・再利用（プリセットの自作）
- E. 特に後回しにしたいものはない
- X. Other (please specify)

[Answer]:B.C.

---

## Q3. mvpの「対象外（やらないこと）」を明確にしたいものはありますか（複数選択可）

最初から範囲外と決めておきたいものを選んでください（select all that apply）。境界を明確にするための質問です。

- A. クラウド保存・オンライン共有機能（ローカル完結を維持）
- B. 複数OS対応（Windows専用を維持）
- C. AIによる自動補正・自動生成
- D. 動画・GIFの加工
- E. 特に明示しておきたい対象外はない / Not identified
- X. Other (please specify)

[Answer]:A.B.C.D.

---

## Q4. 操作の基本スタイルはどちらが近いですか（UIの方向性）

mvpでの使い勝手の方向性を教えてください。

- A. 1枚ずつ画面で見ながら調整して保存する（プレビュー重視）
- B. フォルダを指定して一括で同じ加工をかける（バッチ重視）
- C. 両方できるとよい（まずはどちらか優先があれば記入）
- D. まだ決めていない / Not yet defined
- X. Other (please specify)

[Answer]:A.

---

## Q5. 機能を実装する順序の希望はありますか（シーケンス）

mvpの中で作る順番に希望はありますか。

- A. 価値の高いものから（よく使う加工を先に）
- B. リスク・難しいものから（不安な部分を先に確かめる）
- C. 依存関係の順に（基盤→応用）
- D. おまかせ（適切と思う順で）
- X. Other (please specify)

[Answer]:D.

---

## Q6. mvpに関して守りたい期限や区切りはありますか

- A. 特に期限はない。納得いくまで作り込む
- B. できるだけ早く「まず使える」状態にしたい
- C. 具体的な期限がある（記入してください）
- D. まだ決めていない / Not yet defined
- X. Other (please specify)

[Answer]:A.なので丁寧に進めてください。

---

## Q7. トリミング（切り抜き）・リサイズの扱いを確認させてください（フォローアップ）

Q1の must-have で選択肢B（トリミング・リサイズ）が選ばれておらず、Q2の後回し・Q3の対象外にも入っていませんでした。公開用に整える際は基本的な機能ですが、mvpでの扱いをはっきりさせておきたいです。

- A. mvpの must-have に入れる（基本補正などと同様に最初から入れる）
- B. mvpでは後回し（nice-to-have）でよい
- C. mvpの対象外にする
- D. どちらでもよい／おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
