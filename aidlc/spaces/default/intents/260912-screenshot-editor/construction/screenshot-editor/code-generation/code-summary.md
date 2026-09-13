# Code Summary — screenshot-editor（mvp）

承認済み計画（code-generation-plan.md）に沿って、ワークスペース直下 `app/` に
FF14 スクリーンショット加工ツールを実装した。レイヤーは ui → core → io の一方向依存で、
core / io は GUI（PySide6）に依存しない純粋モジュール。

## 生成したファイル

### アプリケーションコード（`app/screenshot_editor/`）
| ファイル | 役割 |
|----------|------|
| `__init__.py` | パッケージ定義（バージョン） |
| `__main__.py` | エントリポイント（`python -m screenshot_editor` で GUI 起動） |
| `errors.py` | 型付きドメインエラー（ImageEditorError 基底＋ Unsupported/Corrupt/ImageTooLarge/SaveError、日本語 user_message 保持） |
| `core/edit_settings.py` | EditSettings（加工設定、既定=恒等）、Crop/Resize/Credit/CreditPosition |
| `core/processor.py` | 決定的な純粋変換。固定合成順序（補正→画質→フィルタ→トリミング/リサイズ→クレジット）で `apply()` |
| `core/presets.py` | 組み込みプリセット 8 種、`merge_into`（ユーザー明示値を優先） |
| `io/image_io.py` | 安全デコード（verify+load、MAX_IMAGE_PIXELS 上限）、フォーマット判定、非破壊アトミック保存（一時ファイル→os.replace、`_edited` 接尾辞、衝突連番） |
| `batch/batch_processor.py` | 複数ファイルへ一括適用、失敗スキップ継続、成功/失敗集計、進捗コールバック |
| `ui/main_window.py` | メイン画面（左メニュー＋中央プレビュー＋右調整、リアルタイム反映、非破壊保存、リセット、バッチ起動）。プレビューは縮小版に適用、保存は原寸に適用 |
| `ui/panels.py` | 調整パネル（明るさ等スライダー）・プリセット選択パネル。主要要素に objectName 付与 |
| `ui/batch_dialog.py` | バッチ適用ダイアログ。処理はワーカースレッド（QThread）、進捗・件数を表示、Esc で閉じる |

### テスト（`app/tests/`）
| ファイル | 内容 |
|----------|------|
| `conftest.py` | 合成フィクスチャ画像（数 px の PNG/JPEG、アルファ有無）をプログラム生成 |
| `test_image_io.py`（P0） | 非破壊（元バイト列・mtime 不変）、PNG 画素完全一致/JPEG 許容誤差ラウンドトリップ、PNG↔JPEG クロス、破損/非対応/0バイト/巨大の異常系、保存衝突連番、中途出力なし |
| `test_processor.py` | 恒等一致・決定性・非破壊（入力不変）・明るさ単調増加・トリミング/リサイズ寸法（1px 境界）・クレジット合成・固定合成順序・RGBA 保持 |
| `test_edit_settings.py` | 既定値=恒等、copy_with の不変性、Credit 既定 |
| `test_presets.py` | プリセット 6〜10 種の存在・名称一意・決定的同一出力・ユーザー値優先 |
| `test_batch_processor.py` | 全件成功・部分失敗スキップ・全件失敗の非クラッシュ・既定出力先・進捗通知 |

### 設定・配布・ゲート（`app/`）
`pyproject.toml`（依存宣言・pytest/coverage/ruff/black 設定）、`uv.lock`（依存ロック・コミット対象）、
`.python-version`（3.11）、`.pre-commit-config.yaml`（black/ruff/pytest ローカルゲート）、
`run_checks.py`（単一タスクスクリプト）、`README.md`（起動・テスト・ビルド手順）。

## 主要な実装判断

- **合成順序を固定**（functional-spec §3.5 / Q3）: 補正 → 画質 → フィルタ → トリミング/リサイズ → クレジット。同じ設定なら常に同じ出力（決定的）、クレジットは最後に載せるためリサイズで文字がぼけない。
- **非破壊アトミック保存**（SEC-3 / FR7）: 出力先と同一ディレクトリに一時ファイルを書き、`os.replace` で最終名へリネーム。`_edited` 接尾辞、既存衝突時は `_edited(1)…` 連番、元パスと同一になる場合も連番で回避。保存失敗時は一時ファイルを削除し `SaveError` へ変換。
- **安全デコード**（SEC-2 / FR1.3）: Pillow の `Image.open` + `verify()`/`load()`。`MAX_IMAGE_PIXELS` は 15360×8640（16K 相当、= 132,710,400 px）を上限とし、超過は `ImageTooLargeError`。破損/非対応/0バイトは型付きエラーへ変換（fail fast）。
- **型付きエラー階層＋日本語メッセージ**: core/io は技術例外を `ImageEditorError` 系へ変換し、`user_message` に日本語文言を保持。UI 層はこれを表示する（1 枚の失敗でツールを落とさない）。
- **プリセット 8 種**: ナチュラル / ビビッド / シネマティック / モノクロ / セピア / ソフト / シャープネス / クール。`merge_into` は補正/画質が 0（未調整）の項目のみプリセット値で埋め、ユーザーの明示値を優先。
- **クレジット位置のクランプ**: 小さな画像でテキストがはみ出す場合でも、左上座標を画像内にクランプし少なくとも一部が描画されるようにした（実装時に発見・修正）。
- **性能**（PERF-1/2/3）: プレビューは表示解像度に合わせた縮小版（最大 900px）へ適用、原寸適用は保存時のみ。バッチは QThread のワーカーで実行し UI をブロックしない。
- **カバレッジ測定の限定**: `pyproject.toml` の `[tool.coverage.run] source` を `screenshot_editor.core` と `screenshot_editor.io` に限定（team.md の測定対象スコープ特化。GUI/配線層は下限対象外）。

## テスト実行結果

`app/` で次を実行:

```
uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80
```

- 結果: **50 passed, 0 failed**
- カバレッジ（中核ロジック層 core/io）: **90.15%**（下限 80% を充足）
  - `core/edit_settings.py` 100% / `core/presets.py` 96% / `core/processor.py` 88% / `io/image_io.py` 87%
- Lint: `uv run ruff check .` → All checks passed（セキュリティ系 `S` ルール含む）
- Format: `uv run black --check .` → 差分なし
- 全モジュールの byte-compile（GUI 含む）成功

## 計画からの逸脱

- 逸脱なし。計画の Step 1〜14 をすべて実施した。
- 実装時の微修正: クレジット描画位置を画像内にクランプ（テストで発見した小画像時のはみ出しに対応）。合成順序・非破壊保存・レイヤー分離など設計上の判断は計画どおり。

## 検証コマンド（このユニット限定）

```
cd app
uv sync --extra dev
uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80
uv run ruff check .
uv run black --check .
```
