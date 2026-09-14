# 要件定義 — preview-changed-error（bugfix）

## Sources

- [desc] Initial description: 「画像を開いて調整やフィルタ、プリセットを選択するとコンソールに（エラーが出る）」（`aidlc engine workspace project-description`、末尾切れだが症状は下記で裏取り済み）
- [scope] Workflow-selected scope: bugfix（Minimal 深度 / Minimal テスト戦略）
- リバースエンジニアリング成果物: `aidlc/spaces/default/codekb/aidlc/code-quality-assessment.md`（根因特定）, `architecture.md`, `code-structure.md`, `business-overview.md`
- 対象ソース: `app/screenshot_editor/ui/panels.py`, `app/screenshot_editor/ui/main_window.py`
- 質問回答: `requirements-analysis-questions.md`（Q1〜Q5＝すべて A、統合サマリ確認で承認済み）

## Intent Analysis（意図）

利用者は FF14 スクリーンショット編集アプリ（`screenshot-editor`）で、画像を開いた状態で「調整（明るさ・コントラスト等のスライダー）」や「フィルタ／プリセット（コンボ選択）」を操作している。その際にコンソールへエラーが出力される。利用者が達成したいのは、**これらの操作を行ってもコンソールにエラーが出ず、プレビューが従来どおり正しく更新される**こと。

根因はリバースエンジニアリングで高確度に特定済み: `app/screenshot_editor/ui/panels.py` の `AdjustmentPanel` と `PresetPanel` が、引数を伴わない `changed = Signal()` を宣言しつつ、`int` 引数を伴う Qt シグナル（`QSlider.valueChanged` / `QComboBox.currentIndexChanged`）を `self.changed.emit` に直結している。上流の `int` 引数が引数なしシグナルの `emit` に渡り、PySide6 実行時にシグネチャ不一致のエラーがコンソールへ出力される。

本 intent は **bugfix スコープ**であり、報告バグの解消に範囲を限定する（機能追加・無関係のリファクタリングは行わない）。

## Functional Requirements（機能要件）

### FR1. コンソールエラーの解消

- **FR1.1** 画像を開いた状態で調整スライダー（明るさ・コントラスト・彩度・シャープ・ぼかし・ノイズ除去）を操作したとき、コンソールにシグネチャ不一致に起因するエラー（TypeError／警告）が出力されないこと。合否の観測手段は、ヘッドレス実行下で `changed` の購読ハンドラが余分な位置引数なしで呼び出されること、および Qt のシグナル発火時に stderr／Qt ログへシグネチャ不一致メッセージが出ないことで判定する（具体手段は build-and-test で確定）。
- **FR1.2** 画像を開いた状態でフィルタ／プリセットのコンボ選択を変更したとき、コンソールに同種のエラーが出力されないこと（観測手段は FR1.1 と同様）。
- **FR1.3** `AdjustmentPanel.reset()` および `PresetPanel.reset()` を経由した通知でも、コンソールにエラーが出力されないこと（現行の引数なし emit 経路を壊さない）。

### FR2. プレビュー更新の維持

- **FR2.1** 調整スライダー操作時に、`MainWindow` のプレビュー（`_update_preview`）がこれまでどおり更新されること（`AdjustmentPanel.changed` → `_update_preview` の購読経路が機能する）。
- **FR2.2** フィルタ／プリセット選択変更時に、プレビューがこれまでどおり更新されること（`PresetPanel.changed` → `_update_preview` の購読経路が機能する）。
- **FR2.3** リセット操作時に、プレビューが初期（恒等）状態へ更新されること。

### FR3. 回帰防止

- **FR3.1** `AdjustmentPanel.changed` および `PresetPanel.changed` が、上流シグナル（`valueChanged` / `currentIndexChanged`）の発火を契機に、購読ハンドラへ引数 0 個で通知されることを検証する自動回帰テストを追加すること（本バグの再発を機械的に検知できるようにする）。合格条件は「接続したスロットが例外・エラー出力なしに、位置引数 0 個で呼び出される」こととする。
- **FR3.2** 追加テストは GUI（PySide6）依存であるため、オフスクリーン等のヘッドレス実行環境の整備を許容する。
- **FR3.3** 既存のテストスイートはグリーンを維持すること（`app/tests/` の core/io/batch テストを退行させない）。

## Non-Functional Requirements（非機能要件）

- **NFR1（アーキテクチャ制約の維持）** 修正は依存方向 `ui → core → io` の一方向を維持し、`core` は GUI（PySide6）を一切 import しないこと。修正対象は `ui` 層に限定する。
- **NFR2（非破壊・オフライン維持）** 本修正は既存の非破壊保存・ローカル/オフライン完結の挙動に一切影響を与えないこと（プレビュー・保存のデータ経路を変更しない）。
- **NFR3（堅牢性）** シグナル配線起因のコンソールエラーが解消され、調整・フィルタ／プリセット・リセットの通常操作を繰り返してもエラー出力や不安定化が生じないこと（本バグはクラッシュではなくコンソールへのエラー出力であり、その解消と操作の安定性を基準とする）。
- **NFR4（最小変更・低リスク）** 変更の blast radius を最小化する。報告バグに関係しないコードの改変を行わない。

## Constraints（制約）

- 技術スタック: Python 3.11 / PySide6==6.7.2 / Pillow==10.4.0（既存構成を変更しない）。
- team 規約: bugfix は「対象バグの回帰テストを追加し、既存スイートをグリーンに保つ」。カバレッジ計測対象は現状 `core`/`io` のみ（`ui` は対象外）。
- project 規約（Mandated/Forbidden）: 元画像の非破壊、外部送信の禁止、依存方向 `ui → core → io`、日本語のユーザー向けメッセージ、依存ライブラリのピン留め等を遵守する。
- コミットメッセージは日本語。

## Assumptions（前提）

- 修正アプローチは「シグナルの引数を捨てるスロットで包む」方針を優先する（例: `slider.valueChanged.connect(lambda *_: self.changed.emit())`、`self._combo.currentIndexChanged.connect(lambda *_: self.changed.emit())`）。現行の `changed = Signal()` と `reset()` の引数なし emit をそのまま維持でき、変更が最小で済むため（Q3=A）。最終的な実装手段は後段（code-generation / build-and-test）で確定するが、エラー解消と依存方向の維持が満たされれば手段は問わない。
- 症状は調整・フィルタ／プリセットの両方で発生する（Q1=A）。RE の解析およびソース確認と一致。
- project-description の末尾（「…コンソールに」）は「…コンソールにエラーが出る」の意である（症状の裏取り済み）。

## Out of Scope（スコープ外）

- 新機能の追加、UI レイアウトの改善、既存機能の挙動変更。
- 報告バグに無関係な技術的負債の解消（例: `app/screenshot_editor/ui/batch_dialog.py` の `_on_finished` 周りのスレッド後始末の明示化）。
- `ui` 層全体への網羅的なテスト整備（今回は本バグの回帰テストに限定）。
- カバレッジ計測対象への `ui` 層の恒久的な追加（今回のテスト追加とは別判断）。

## Open Questions（残課題 / 後段へ）

- 回帰テストの具体的な実行環境（PySide6 のオフスクリーンプラットフォーム `QT_QPA_PLATFORM=offscreen` 等）の設定詳細は build-and-test で確定する。
- 追加する回帰テストを CI/ローカルゲート（pre-commit / pre-push / `run_checks.py`）にどう組み込むかは build-and-test / deployment-pipeline で確定する。

## Assumptions & Open Questions

上記「Assumptions」および「Open Questions」を参照。未解決の矛盾はなし。
