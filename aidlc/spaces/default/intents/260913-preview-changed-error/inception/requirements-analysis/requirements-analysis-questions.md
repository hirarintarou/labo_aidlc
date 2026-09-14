# Requirements Analysis — 確認質問

対象バグ（intent `preview-changed-error`）: 画像を開いて「調整（スライダー）」や「フィルタ／プリセット（コンボ）」を選択すると、コンソールにエラーが出る。

リバースエンジニアリングで根因を高確度に特定済みです（`aidlc/spaces/default/codekb/aidlc/code-quality-assessment.md`）:

- `app/screenshot_editor/ui/panels.py` の `AdjustmentPanel` / `PresetPanel` はいずれも引数なしの `changed = Signal()` を宣言している。
- しかし `slider.valueChanged.connect(self.changed.emit)`（`QSlider.valueChanged` は `int` を伴う）と `self._combo.currentIndexChanged.connect(self.changed.emit)`（`QComboBox.currentIndexChanged` は `int` を伴う）で、上流の `int` 引数を引数なしシグナルの `emit` へ直結している。
- そのため PySide6 実行時にシグネチャ不一致でコンソールへエラーが出る。ユーザー報告の症状と一致。

bugfix スコープの範囲を確定するための質問です。A〜E から選ぶか、`X. Other` で自由記述してください。`[Answer]:` タグに記入してください。

---

## Q1. バグの症状（再現条件）の確認

報告されている症状は「画像を開いた状態で、調整スライダーの操作、またはフィルタ／プリセットのコンボ選択を行うと、コンソールにエラーが出力される」で合っていますか。

- A. その通り（調整・フィルタ／プリセットの両方でコンソールエラー）
- B. 症状はコンソールエラーではなく、機能が動かない（プレビューが更新されない等）ことが主
- C. 調整スライダーのみで発生（フィルタ／プリセットは問題ない）
- D. フィルタ／プリセットのみで発生（調整スライダーは問題ない）
- X. Other (please specify)

[Answer]: A （推奨既定。統合サマリ確認ゲートで上書き可）

## Q2. 期待する修正結果（受け入れ基準）

この修正で「解消した」と判断する基準はどれが最も近いですか。

- A. 調整・フィルタ／プリセット操作時にコンソールへエラーが出なくなり、かつプレビューがこれまで通り更新される
- B. コンソールへエラーが出なくなればよい（プレビュー挙動は現状維持で可）
- C. エラー解消に加えて、`reset()` 経由の再描画も含めシグナル配線全体が正しく動くこと
- X. Other (please specify)

[Answer]: A （推奨既定。統合サマリ確認ゲートで上書き可）

## Q3. 修正アプローチの方針

RE では 2 案が挙がっています。どちらの方針を優先しますか（実装は後段ステージ、ここでは要件レベルの意向確認です）。

- A. シグナルの引数を捨てるスロットで包む（例 `slider.valueChanged.connect(lambda *_: self.changed.emit())`）。現行の `changed = Signal()` と `reset()` の引数なし呼び出しをそのまま維持でき、変更は最小。
- B. シグネチャを合わせる（`changed = Signal(int)` などに変更）。ただし `reset()` の引数なし emit や購読側の見直しが必要。
- C. 実装方針は任せる（エラーが解消し、依存方向 `ui → core → io` を壊さなければ手段は問わない）
- X. Other (please specify)

[Answer]: A （推奨既定。統合サマリ確認ゲートで上書き可）

## Q4. 回帰防止テストの扱い

team 規約では bugfix は「対象バグの回帰テストを追加し、既存スイートをグリーンに保つ」と定めています。一方、現状 `ui/` 層には自動テストがなく、カバレッジ計測対象も `core`/`io` に限定されています（PySide6 の GUI 依存）。今回の回帰防止テストをどうしますか。

- A. UI シグナル配線の回帰テストを追加する（`AdjustmentPanel` / `PresetPanel` の `changed` が余分な引数なしで正しく発火することを検証。GUI 依存のためオフスクリーン等のテスト環境整備を許容する）
- B. 今回はテスト追加を見送り、手動での動作確認のみとする（既存スイートはグリーンを維持）
- C. 判断は後段（build-and-test）に委ねる（要件としては「回帰を防ぐ手段を設ける」とだけ定める）
- X. Other (please specify)

[Answer]: A （推奨既定。統合サマリ確認ゲートで上書き可）

## Q5. スコープ境界の確認

今回の修正対象を、報告バグ（シグナル配線に起因するコンソールエラー）の解消に限定してよいですか。RE で将来的な debt として挙がった `batch_dialog.py` のスレッド後始末など、無関係の改善は含めません。

- A. はい、報告バグの解消のみに限定する
- B. いいえ、あわせて対応してほしい項目がある（`X` で具体的に）
- X. Other (please specify)

[Answer]: A （推奨既定。統合サマリ確認ゲートで上書き可）

---

## Consolidated Summary Confirmation

回答の要約（すべて推奨既定。必要なら変更してください）:

- Q1 症状: 画像を開いた状態で調整スライダー操作、またはフィルタ／プリセット選択を行うと、コンソールにエラーが出る（調整・フィルタ／プリセットの両方）。
- Q2 受け入れ基準: 調整・フィルタ／プリセット操作時にコンソールへエラーが出なくなり、かつプレビューが従来どおり更新されること。
- Q3 修正アプローチの方針: シグナルの引数を捨てるスロットで包む方針を優先（現行 `changed = Signal()` と `reset()` の引数なし emit を維持でき、変更最小）。
- Q4 回帰防止テスト: UI シグナル配線の回帰テストを追加する（GUI 依存のためオフスクリーン等のテスト環境整備を許容）。
- Q5 スコープ: 報告バグ（シグナル配線に起因するコンソールエラー）の解消のみに限定し、無関係の改善（例: `batch_dialog.py` のスレッド後始末）は含めない。

Does this all look correct before I generate the requirements artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
