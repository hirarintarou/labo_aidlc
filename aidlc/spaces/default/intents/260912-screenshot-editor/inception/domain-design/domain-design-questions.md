# Domain Design — Questions

## Sources

- [scope] Workflow-selected scope: `mvp`.

> 確定プラクティスで ui→core→io の分離が硬い制約。ここでは論理的な構成部品（コンポーネント）の境界と、加工設定などのデータの持ち主を確認します。技術スタックは未確定なので、ここでは「どんな部品に分けるか」だけを決めます（配置やデプロイ形態は次のUnits Generationで扱います）。

## 設計のたたき台（案）

- **AppUI**（ui層）: ウィンドウ・左メニュー・プレビュー・右調整パネル・バッチダイアログ。coreを呼ぶだけで画像処理は持たない。
- **ImageProcessingCore**（core層）: 明るさ/コントラスト/彩度、シャープ/ぼかし/ノイズ除去、フィルタ/プリセット、トリミング/リサイズ、クレジット合成。GUI非依存の純粋ロジック。
- **ImageIO**（io層）: PNG/JPEGの読み込み・フォーマット判定・非破壊の安全な書き出し（一時ファイル→リネーム）。
- **BatchProcessor**: 1つの加工設定を複数ファイルに適用し、成功/失敗を集計。coreとioを使う。
- **エンティティ（データ）案**: `EditSettings`（加工設定の集合。単体編集・バッチで共有）、`PresetDefinition`（プリセットの定義）、`ImageDocument`（開いている画像とそのメタ）。

---

## Q1. コンポーネントの分け方はこの案（AppUI / ImageProcessingCore / ImageIO / BatchProcessor）でよいですか

- A. はい、この4コンポーネントでよい
- B. BatchProcessor は ImageProcessingCore に含めて3コンポーネントにしたい
- C. その他の分け方がよい（記入してください）
- X. Other (please specify)

[Answer]:A.

---

## Q2. 「加工設定（EditSettings）」の持ち主はどこがよいですか

加工設定は単体編集でもバッチでも使う中心データです。

- A. ImageProcessingCore が持つ（設定を受け取って変換するのが core なので自然）
- B. 独立した設定コンポーネントを作る
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q3. プリセット定義（PresetDefinition）の持ち方に希望はありますか

- A. ImageProcessingCore が既定のプリセット群を持つ（mvpは組み込みの6〜10種）
- B. 外部ファイルやユーザー定義から読み込めるようにする（mvp外でよい）
- C. おまかせ
- X. Other (please specify)

[Answer]:A.


---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
