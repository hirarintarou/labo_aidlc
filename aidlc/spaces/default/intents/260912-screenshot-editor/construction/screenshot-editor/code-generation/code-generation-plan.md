# Code Generation Plan — screenshot-editor（mvp）

技術スタック: Python 3.11+ / PySide6 / Pillow / pytest（[tech-stack-decisions]）。パッケージ管理・仮想環境は **uv** に統一（環境依存の低減・再現性向上のためユーザー要望で採用）。依存は `pyproject.toml` に宣言し、ロックは `uv.lock`（コミット対象）。レイヤーは ui→core→io の一方向依存。アプリコードはワークスペースルート `app/` 配下に配置する。テスト方針は test-after、中核ロジック層（core/io）に80%カバレッジ下限。骨組み（US0.1）を最初に通す。

## ディレクトリ構成（ワークスペースルート `app/`）

```
app/
├─ screenshot_editor/
│  ├─ __init__.py
│  ├─ __main__.py            # エントリポイント（python -m screenshot_editor）
│  ├─ errors.py              # 型付きドメインエラー
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ edit_settings.py    # EditSettings データモデル
│  │  ├─ presets.py          # PresetDefinition（組み込み6-10種）
│  │  └─ processor.py        # 画像変換（補正/画質/フィルタ/トリミング/リサイズ/クレジット合成）
│  ├─ io/
│  │  ├─ __init__.py
│  │  └─ image_io.py         # 安全デコード・フォーマット判定・非破壊アトミック保存
│  ├─ batch/
│  │  ├─ __init__.py
│  │  └─ batch_processor.py  # 複数ファイルへの一括適用・集計
│  └─ ui/
│     ├─ __init__.py
│     ├─ main_window.py      # MainWindow（メニュー/プレビュー/調整/保存）
│     ├─ panels.py           # 各調整パネル
│     └─ batch_dialog.py     # バッチ適用ダイアログ
├─ tests/
│  ├─ __init__.py
│  ├─ conftest.py            # 合成フィクスチャ画像
│  ├─ test_image_io.py       # 非破壊保存・ラウンドトリップ・異常系（P0）
│  ├─ test_processor.py      # 各変換の決定性・恒等・境界
│  ├─ test_edit_settings.py
│  ├─ test_presets.py
│  └─ test_batch_processor.py # スキップ継続・件数集計
├─ pyproject.toml            # 依存宣言・ruff/black/pytest設定（uv 管理）
├─ uv.lock                   # uv による依存ロック（コミット対象・ピン留め）
├─ .python-version           # uv が使う Python バージョン固定
├─ .pre-commit-config.yaml   # black/ruff/pytest ローカルゲート（uv run 経由）
├─ run_checks.py             # 単一タスクスクリプト（uv run で green+カバレッジ）
└─ README.md
```

## 実装ステップ（順序＝骨組み優先→core→io→batch→ui、test-after）

- [x] Step 1: プロジェクト雛形を **uv** で作成（`pyproject.toml` に依存宣言、`uv.lock`・`.python-version` を固定、pytest/pytest-cov/ruff/black 設定、pre-commit・run_checks.py はいずれも `uv run` 経由）。`uv sync` 後にテストランナーが `uv run pytest` で起動できる状態にする（test-after前提の実行可能コマンド確立）。依存導入時は類似名/タイポスクワッティングを目視確認する。[cicd-pipeline][tech-stack-decisions]
- [x] Step 2: errors.py — ImageEditorError 基底と UnsupportedImageError/CorruptImageError/ImageTooLargeError/SaveError。[security-design]
- [x] Step 3: io/image_io.py — `load_image(path)`（verify+MAX_IMAGE_PIXELS上限、型付きエラー変換）、`detect_format`, `save_nondestructive(image, src_path, out_dir, fmt)`（一時ファイル→os.replace、`_edited`接尾辞、衝突時連番、元は不変）。[US0.1][US1.7][SEC-2][SEC-3]
- [x] Step 4: tests/test_image_io.py — 非破壊（元バイト列・mtime不変）、PNG画素完全一致/JPEG許容誤差ラウンドトリップ、破損/非対応/0バイト/巨大の異常系、衝突時連番。（P0）[team-practices]
- [x] Step 5: core/edit_settings.py — EditSettings（brightness/contrast/saturation/sharpen/blur/denoise/preset/crop/resize/credit、恒等既定）。[functional-spec §3]
- [x] Step 6: core/processor.py — 各変換を決定的な純粋関数で実装し、固定合成順序（補正→画質→フィルタ→トリミング/リサイズ→クレジット）で `apply(image, settings)` を提供。GUI非依存。[functional-spec §3.5][Q3]
- [x] Step 7: core/presets.py — 組み込みプリセット6〜10種（例: ナチュラル/ビビッド/シネマティック/モノクロ/セピア/ソフト等）を EditSettings ベースで定義。[US1.4]
- [x] Step 8: tests/test_processor.py, test_edit_settings.py, test_presets.py — 恒等一致・決定性・寸法（トリミング/リサイズ、1px境界）・クレジット合成・プリセット再現性。[team-practices]
- [x] Step 9: batch/batch_processor.py — 対象一覧に settings を適用、失敗スキップ継続、成功/失敗集計（n+m=総数）、進捗コールバック。[US2.1]
- [x] Step 10: tests/test_batch_processor.py — 部分失敗スキップ・件数一致・全件失敗の非クラッシュ。[team-practices]
- [x] Step 11: ui/main_window.py, panels.py, batch_dialog.py — PySide6でメイン画面（左メニュー＋中央プレビュー＋右調整、リアルタイム反映、大きめ文字/ボタン）、リセット、非破壊保存、バッチダイアログ（進捗・件数、Escで閉じる）。重処理はワーカースレッド。[functional-spec][frontend-components][performance-design]
- [x] Step 12: __main__.py エントリポイント（`python -m screenshot_editor` でGUI起動）。[US0.1]
- [x] Step 13: ローカルで全テスト実行＋カバレッジ（`uv run pytest ... --cov-fail-under=80`、core/io層80%下限）を確認し green にする。data-testid相当（Qtの objectName）を主要操作要素に付与。[NFR5]
- [x] Step 14: README に起動（`uv run python -m screenshot_editor`）・ビルド（`uv run pyinstaller ...`）・セットアップ（`uv sync`）手順を記載。[infrastructure-specification]

## Story → Code Step トレーサビリティ

| Story/AC | 実装ステップ |
|----------|-------------|
| US0.1（骨組み疎通） | Step 3, 4, 12 |
| US1.1（開く/プレビュー/カテゴリ切替） | Step 3, 11 |
| US1.2（基本補正） | Step 6, 8, 11 |
| US1.3（画質調整） | Step 6, 8, 11 |
| US1.4（フィルタ/プリセット） | Step 7, 8, 11 |
| US1.5（トリミング/リサイズ） | Step 6, 8, 11 |
| US1.6（クレジット付与） | Step 6, 8, 11 |
| US1.7（非破壊保存） | Step 3, 4, 11 |
| US1.8（リセット） | Step 5, 11 |
| US2.1（バッチ） | Step 9, 10, 11 |

## Testing Contract
```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "テスト対象となる各レイヤー（画像処理コア・入出力・保存を優先）を",
  "scope": "mvp",
  "test_strategy": "standard",
  "project_type": "greenfield",
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
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Meet an 80% line-coverage floor.",
      "Run the selected tests in CI before merge."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
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
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
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
  "input_sha256": "sha256:4e51643f526624b72fb39d420a5566a5a7c7d17b4a9161d695183ca1756496b4",
  "contract_sha256": "sha256:719c5a4ec3fda89440b884b741066c98d4450b58d5bd34a02d2667930327b89a"
}
```

> Testing Contract の methodology は `test-after`。上記の `plan_profile.steps` は
> 一般レイヤーのベースライン順序であり、本ユニット（デスクトップ GUI・API/DB 層なし）
> では実際の実装レイヤーへ次のように対応させる（順序＝test-after で「実装→当該テスト」）:
> io（Data model/Repository 相当の入出力・非破壊保存）→ core（Business logic 相当の
> 変換ロジック）→ batch → ui（Frontend 相当）。DB/API レイヤーは本ユニットに存在しない
> ため省略する（methodology は変更しない）。runner 準備（Step 1）は最初のテスト実行前に
> 完了させる。

## Assumptions & Open Questions

- パッケージ管理・仮想環境は uv を採用（ユーザー要望、2026-09-13）。依存ロックは uv.lock をコミット。uv はローカル・オフラインで完結利用可能。
- プリセットの具体的な効果値は実装時に調整（6〜10種の代表セット）。
- MAX_IMAGE_PIXELS の上限値・デバウンス値は実装時に設定。
