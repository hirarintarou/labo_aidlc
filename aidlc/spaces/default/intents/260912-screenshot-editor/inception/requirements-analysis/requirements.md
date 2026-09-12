# Requirements — FF14 スクリーンショット加工ツール（mvp）

## Intent Analysis

制作者本人が、FF14のスクリーンショットを公開する前に手軽に綺麗に加工することを目的とする [intent-statement]。狙いは「手作業では難しい品質を手軽に得る」「多くの加工を試して感性に合う一枚を作る」「増える画像を手作業に追われず処理する」こと [intent-statement][scope-document]。個人利用・Windows専用・ローカル完結・非破壊のデスクトップアプリとして実現する [scope-document][team-practices]。

## Functional Requirements

### FR1. 画像の読み込みと表示
- FR1.1 ローカルのPNG/JPEGファイルを開ける [scope-document]。
- FR1.2 開いた画像を中央プレビューに表示する [scope-document]。
- FR1.3 壊れた/非対応/0バイトのファイルは早期に検出し、日本語の分かりやすいメッセージを表示してクラッシュしない（対応形式はPNG/JPEG）[team-practices]。

### FR2. 基本補正
- FR2.1 明るさを調整できる [scope-document]。
- FR2.2 コントラストを調整できる [scope-document]。
- FR2.3 彩度を調整できる [scope-document]。
- FR2.4 調整はプレビューにリアルタイム反映される [rough-mockups]。

### FR3. 画質調整
- FR3.1 シャープ化を適用できる [scope-document]。
- FR3.2 ぼかしを適用できる [scope-document]。
- FR3.3 ノイズ除去を適用できる [scope-document]。

### FR4. フィルタ／プリセット
- FR4.1 ワンタッチで雰囲気を変えるプリセットを適用できる [scope-document]。
- FR4.2 mvpでは中程度（6〜10種類程度）の代表的なプリセットを用意する [Q1]。

### FR5. トリミング・リサイズ
- FR5.1 画像をトリミング（切り抜き）できる [scope-document]。
- FR5.2 画像をリサイズ（サイズ変更）できる [scope-document]。

### FR6. クレジット／ウォーターマーク付与
- FR6.1 テキストのクレジットを画像に付与できる [scope-document][Q5]。
- FR6.2 クレジットの位置・サイズ（・不透明度）を指定できる [rough-mockups]。
- FR6.3 既定のクレジットテンプレート（例「© SQUARE ENIX」）を用意し、自由に編集できる [Q5]。
- FR6.4 クレジット付与はFF14公式の画像利用ガイドライン遵守を目的とする [intent-statement]。

### FR7. 非破壊保存
- FR7.1 加工結果は元画像を上書きせず、別ファイルとして保存する [team-practices]。
- FR7.2 既定の保存先は元画像と同じフォルダとし、ファイル名末尾に接尾辞を付ける（例 `screenshot001_edited.png`）[Q2]。
- FR7.3 出力形式は元画像と同じ形式とする（PNG→PNG、JPEG→JPEG）[Q3]。
- FR7.4 保存は安全に行い、途中失敗で中途半端な出力を残さない（一時ファイル→リネーム等）[team-practices]。

### FR8. 単体プレビュー編集
- FR8.1 1枚ずつプレビューで確認しながら加工し、保存できる [rough-mockups][Q6]。
- FR8.2 メイン画面は左に加工メニュー、中央にプレビュー、右に調整値を配置する [rough-mockups]。

### FR9. バッチ処理
- FR9.1 1枚で決めた加工設定を、フォルダまたは複数ファイルの複数枚に一括適用できる [scope-document][rough-mockups]。
- FR9.2 バッチ結果も非破壊で保存する（FR7準拠）[team-practices]。
- FR9.3 一部のファイルが失敗した場合はスキップして残りを続行し、完了時に「成功n件／失敗m件」を表示する [Q4]。

## Non-Functional Requirements

- NFR1. 可用性・堅牢性: 想定外入力（破損・非対応・巨大画像）でツールがクラッシュせず、操作を継続できる [team-practices]。
- NFR2. プライバシー・セキュリティ: すべての処理をローカルで完結させ、画像やデータを外部へ送信しない [team-practices]。依存ライブラリはバージョン固定＋ロックファイルをコミットし、読み込む画像は未検証データとして標準ライブラリで安全にデコードする [team-practices]。
- NFR3. データ完全性: 元画像を一切改変・上書きしない（非破壊）[team-practices]。
- NFR4. 使いやすさ・見やすさ: 文字・ボタンを大きめにし、見やすいUIとする [rough-mockups]。
- NFR5. 保守性・テスト容易性: 画像処理コアをUIから分離（依存方向 ui→core→io）し、中核ロジック層で80%のラインカバレッジ下限を満たす [team-practices]。
- NFR6. 応答性: 単体編集の調整はプレビューに実用的な速さでリアルタイム反映される（一般的なPNG/JPEG想定。具体的な性能目標はNFRステージで定める）[rough-mockups][raid-log]。

## Constraints

- C1. 対応OSはWindowsのみ [constraint-register]。
- C2. ローカル完結・オフライン動作（外部送信なし）[constraint-register]。
- C3. 入出力は一般的なPNG/JPEG [constraint-register]。
- C4. 個人開発・個人利用（チーム体制・対外承認なし）[intent-statement]。
- C5. FF14スクリーンショットの著作権はスクウェア・エニックスに帰属。公開時は公式ガイドライン遵守が前提 [constraint-register]。

## Assumptions

- A1. 技術スタック（言語・GUIフレームワーク・画像処理ライブラリ）は未確定で、後続ステージで実現しやすいものを選定する [feasibility-assessment]。
- A2. プリセットの具体的な内容（各6〜10種の効果）は機能設計で確定する [Q1]。

## Out of Scope

- 不要な写り込み（他プレイヤー名・UI等）の消去・修復（将来）[scope-document]。
- レイヤー・テキスト追加などの本格編集（将来）[scope-document]。
- クラウド保存・オンライン共有 [scope-document]。
- 複数OS対応（macOS/Linux等）[scope-document]。
- AIによる自動補正・自動生成 [scope-document]。
- 動画・GIFの加工 [scope-document]。

## Open Questions

- JPEG保存時の品質（圧縮率）の既定値・調整可否は機能設計で確定する。
- プレビューのリアルタイム反映の具体的な性能目標（応答時間）はNFR要件ステージで定める。

## MVP Acceptance Milestone（受け入れの最初の目安）

- 「まず使える」と判断する最初の目安は、(1) 1枚を開いて基本補正・トリミング・クレジット付与を行い非破壊保存できること（FR1, FR2, FR5, FR6, FR7, FR8）、および (2) フィルタ／プリセットを適用できること（FR4）である [Q6]。
- バッチ処理（FR9）はmvpの必須機能として残すが、上記の最初の目安には含めない [Q6]。

## Assumptions & Open Questions

- 上記 Assumptions（A1, A2）および Open Questions のとおり。未解決事項は後続の機能設計・NFRステージで確定する。
