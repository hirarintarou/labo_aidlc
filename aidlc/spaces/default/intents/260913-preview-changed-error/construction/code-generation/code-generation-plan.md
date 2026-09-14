# コード生成プラン — preview-changed-error（bugfix / zero-Unit）

## 概要

`app/screenshot_editor/ui/panels.py` のシグナル配線バグを最小変更で修正し、回帰を防ぐ UI テストを 1 ファイル追加する。方針は要件（Q3=A）に従い「上流シグナルの引数を捨てるスロットで包む」。依存方向 `ui → core → io` は不変、修正対象は `ui` 層に限定する（NFR1/NFR4）。

- 対象バグ: `AdjustmentPanel` / `PresetPanel` が引数なし `changed = Signal()` を宣言しつつ、`int` を伴う `QSlider.valueChanged` / `QComboBox.currentIndexChanged` を `self.changed.emit` へ直結 → PySide6 実行時にコンソールへシグネチャ不一致エラー。
- 対応要件: FR1.1, FR1.2, FR1.3, FR2.1, FR2.2, FR2.3, FR3.1, FR3.2, FR3.3, NFR1, NFR2, NFR3, NFR4。

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "テスト対象となる各レイヤー（画像処理コア・入出力・保存を優先）を",
  "scope": "bugfix",
  "test_strategy": "minimal",
  "project_type": "brownfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: test-after\n- **Ordering**: テスト対象となる各レイヤー（画像処理コア・入出力・保存を優先）を\n  実装し、その直後に当該レイヤーのテストを記述・実行し、`main` へのマージ前に\n  ローカルでスイート全体がグリーンであることを確認する。\n- カバレッジ（測定対象スコープを特化、Q4=A）: **80% のラインカバレッジ下限を、\n  画像処理の中核ロジック層（補正・フィルタ・入出力・保存）に限定して適用する**。\n  GUI / 配線層（画面・イベントハンドラ・OS ダイアログ連携）は下限の対象外とする。\n  これは `org.md` の mvp 80% 下限を、solo mvp で実現可能な測定対象スコープに\n  特化させたものであり、団体規約と矛盾しない範囲での特化として本 team.md に明記する。\n- テスト種別: 画像処理ロジック（補正・画質調整・フィルタ・トリミング/リサイズ・\n  クレジット付与・入出力）の単体テストを中心とする。非破壊保存（元画像のバイト列・\n  mtime が不変であること）と PNG/JPEG のラウンドトリップ（PNG は画素完全一致、\n  JPEG は寸法・チャンネル・許容誤差内、PNG↔JPEG のクロスも各 1 ケース）を\n  最重点（P0）でテストする。恒等操作・境界（1px、極端なサイズ、アルファ有無、\n  EXIF 回転）や、破損・巨大・非対応入力の異常系（1〜2 件）を含める。GUI 全体の\n  E2E は最小限（1〜2 本、Walking Skeleton の疎通と共用）に留める。\n- CI ゲート（Q5=A）: リモート CI は必須としない。**pre-commit / pre-push フック\n  （または単一のタスクスクリプト）で「テスト green ＋ カバレッジ下限」をローカルで\n  機械的に強制する仕組みを 1 つ用意する**。手動のローカル実行のみには依存しない\n  （個人開発ではすり抜けやすいため）。\n- ツール: 技術スタック未確定のため、選定した言語・フレームワークの標準的な\n  テストランナーとカバレッジ計測ツールに従う（例: .NET は `dotnet test`＋coverlet、\n  Python は pytest＋pytest-cov、JS/TS は Vitest/Jest＋c8/nyc）。確定時に\n  プロジェクト設定へ記録する。"
    }
  ],
  "obligations": {
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Include a targeted regression for the bug or vulnerability.",
      "Keep the existing test suite green."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:9f135e3552081d46efa6210659fbb0d48e879ef7aa412735ceae85f797bc164b",
  "contract_sha256": "sha256:4ce368de1ce94a0d225f7c1f2402241c9295ac9668ad9ed3b52b65be525f6bc2"
}
```

方法論は **test-after**。本バグは `ui`（Frontend behavior）層に限局するため、契約の `plan_profile.steps` のうち `ui` に該当する層のみを適用し、data-model / repository / business logic / API の各層は本バグに無関係なので割愛する（契約の methodology は維持）。runner 準備ステップは最初の実行系テストの前に置く。

## 実装ステップ

- [ ] **Step 1: テストランナーの確認と実行コマンドの記録（runner_step）**
  既存の pytest 構成（`app/pyproject.toml` の `[tool.pytest.ini_options]`）を確認し、UI テストをヘッドレス実行するための環境（`QT_QPA_PLATFORM=offscreen`）を確認する。本ユニットのテストを実行する正確なコマンドを `unit-test-instructions.md` に記録する（プロジェクト全体の `pytest` ではなく、追加テストファイルにスコープしたコマンド）。新規ランタイム依存は追加しない（標準の `pytest` と PySide6 の offscreen プラットフォームのみ）。

- [ ] **Step 2: Frontend behavior — 実装（本バグの修正）**
  `app/screenshot_editor/ui/panels.py` を in-place で修正する（重複ファイルを作らない）。
  - `AdjustmentPanel.__init__`: `slider.valueChanged.connect(self.changed.emit)` を、上流の `int` 引数を捨てて引数なしで `changed` を発火するスロット接続へ変更（例: `slider.valueChanged.connect(lambda *_: self.changed.emit())`）。全スライダーに適用。（FR1.1, FR2.1）
  - `PresetPanel.__init__`: `self._combo.currentIndexChanged.connect(self.changed.emit)` を同様に引数を捨てる接続へ変更。（FR1.2, FR2.2）
  - `changed = Signal()`（引数なし）と `reset()` の `self.changed.emit()`（引数なし呼び出し）は現状維持（FR1.3, FR2.3）。
  - `core` / `io` を import しない（NFR1）。プレビュー・保存のデータ経路には手を加えない（NFR2）。変更は `panels.py` のシグナル接続 2 箇所のみに限定（NFR4）。

- [ ] **Step 3: Frontend behavior — テストの記述と実行（実装直後、回帰防止）**
  UI シグナル配線の回帰テストファイル `app/tests/test_ui_panels.py` を新規作成する（FR3.1, FR3.2）。
  - ヘッドレス `QApplication` を用意するフィクスチャ（`QT_QPA_PLATFORM=offscreen` 前提。`conftest.py` に session スコープの `qapp` フィクスチャを追加、または当該テスト内で生成）。
  - `AdjustmentPanel`: 各スライダーの `setValue(...)`（`valueChanged` 発火）で、購読スロットが **位置引数 0 個** で呼ばれること、例外・エラー出力が出ないことを検証（合格条件 = FR3.1）。`changed` を受けるスロットは `def slot(): ...`（引数なし）とし、余分な引数が渡れば `TypeError` になることで回帰を機械的に検知する。
  - `PresetPanel`: `setCurrentIndex(...)`（`currentIndexChanged` 発火）で同様に検証。
  - `reset()` 経路でも `changed` が引数なしで発火し、スロットがエラーなく呼ばれること（FR1.3, FR2.3）。
  - 追加テストを実行し green を確認。既存スイート（core/io/batch）も退行しないこと（FR3.3）。

- [ ] **Step 4: ドキュメントとトレーサビリティ**
  `code-summary.md`（変更ファイル・実装判断・テスト概要・プランからの逸脱）、`source-manifest.json`（変更した application-source パス）、`traceability.json`（FR/NFR → 実装/テストファイルの対応）を作成する。

## Story-to-code トレーサビリティ

- FR1.1 / FR2.1 → `app/screenshot_editor/ui/panels.py`（`AdjustmentPanel.__init__` の接続修正） / `app/tests/test_ui_panels.py`
- FR1.2 / FR2.2 → `app/screenshot_editor/ui/panels.py`（`PresetPanel.__init__` の接続修正） / `app/tests/test_ui_panels.py`
- FR1.3 / FR2.3 → `app/screenshot_editor/ui/panels.py`（`reset()` は現状維持で検証） / `app/tests/test_ui_panels.py`
- FR3.1 / FR3.2 / FR3.3 → `app/tests/test_ui_panels.py`（新規回帰テスト、ヘッドレス実行、既存スイート green 維持）
- NFR1 / NFR2 / NFR4 → `app/screenshot_editor/ui/panels.py`（`ui` 層限定・依存方向不変・最小変更）
- NFR3 → `app/tests/test_ui_panels.py`（操作の反復でエラー出力・不安定化がないことを検証）

## スコープ外

- `core` / `io` / `batch` の変更、新機能、UI レイアウト変更。
- `batch_dialog.py` のスレッド後始末など報告バグに無関係な負債。
- `ui` 層のカバレッジ計測対象への恒久追加（`pyproject.toml` の coverage source は変更しない）。
