# Implementation Brief — screenshot-editor（mvp）

> このファイルは、code-generation を実行するエージェント（フックが動くAI-DLC環境）向けの実装申し送りです。設計・プラン・テスト方針は確定済み。Plan Approval 後、`app/` 配下に実装してください。

## 技術スタック（確定）
- Python 3.11+ / PySide6（GUI）/ Pillow（画像処理）/ pytest + pytest-cov / ruff + black / mypy（任意）/ PyInstaller（配布）
- 依存はバージョン固定＋ロックファイルをコミット（requirements.txt ハッシュ付き or poetry）

## ディレクトリ（ワークスペースルート `app/`）
```
app/
├─ screenshot_editor/
│  ├─ __init__.py, __main__.py   # python -m screenshot_editor でGUI起動
│  ├─ errors.py                  # ImageEditorError / Unsupported/Corrupt/ImageTooLarge/SaveError
│  ├─ core/  edit_settings.py, presets.py, processor.py   # GUI非依存の純粋ロジック
│  ├─ io/    image_io.py         # 安全デコード・フォーマット判定・非破壊アトミック保存
│  ├─ batch/ batch_processor.py  # 一括適用・スキップ継続・集計・進捗
│  └─ ui/    main_window.py, panels.py, batch_dialog.py   # PySide6
├─ tests/  conftest.py, test_image_io.py, test_processor.py, test_edit_settings.py, test_presets.py, test_batch_processor.py
├─ pyproject.toml, requirements.txt, .pre-commit-config.yaml, run_checks.py, README.md
```

## 実装ルール（Mandated / 設計由来）
1. **ui→core→io の一方向依存**。core は PySide6 を一切 import しない純粋モジュール。Pillow型は core/io の内側に閉じ込め ui へ漏らさない。
2. **非破壊保存**: 元画像を上書きしない。同フォルダに `_edited` 接尾辞・元と同形式で、一時ファイル→`os.replace` のアトミック書き出し。既存 `_edited` 衝突時は連番（`_edited(1)`…）。保存後、元画像のバイト列・mtime は不変。
3. **安全デコード**: `Image.open`＋`verify()`/`load()`、`Image.MAX_IMAGE_PIXELS` に上限。破損/非対応/0バイト/巨大は型付きエラーに変換し、UI で日本語メッセージ表示、クラッシュしない（fail fast）。
4. **合成順序は固定**（UI操作は自由）: 補正 → 画質 → フィルタ → トリミング/リサイズ → クレジット。core の `apply(image, settings)` が決定的に適用。恒等パラメータでは入力と一致。
5. **ローカル完結・オフライン**: ネットワークI/Oを行わない。

## 機能（FR / US 対応）
- 画像を開く（PNG/JPEG）→中央プレビュー、左メニューでカテゴリ選択→右パネル切替（US1.1）
- 基本補正（明るさ/コントラスト/彩度、リアルタイム反映）（US1.2）
- 画質調整（シャープ/ぼかし/ノイズ除去）（US1.3）
- フィルタ/プリセット（**組み込み6〜10種**、名前リスト表示、決定的）（US1.4）
- トリミング（**自由矩形**）・リサイズ（**既定でアスペクト比保持**、解除可）（US1.5）
- クレジット付与（テキスト＋位置/サイズ/不透明度、既定「© SQUARE ENIX」編集可）（US1.6）
- 非破壊保存（US1.7）／リセット（全調整初期化、元画像不変）（US1.8）
- バッチ（フォルダ/複数ファイルに同設定を一括適用、失敗スキップ継続、「成功n/失敗m（n+m=総数）」、進捗表示、ワーカースレッドでUI非ブロック、途中キャンセルなし）（US2.1）
- UI: 文字/ボタン大きめ、主要動線キーボード操作可、モーダルはEscで閉じる（NFR4）

## EditSettings（core 所有・単体/バッチ共有）
`brightness, contrast, saturation, sharpen, blur, denoise, preset_name, crop, resize(size+keep_aspect), credit(text,pos,size,opacity)`。各既定値=恒等（無変化）。

## テスト（test-after、中核層80%カバレッジ、P0重点）
- P0: 非破壊（元バイト列・mtime不変）、PNG画素完全一致/JPEG許容誤差のラウンドトリップ、PNG↔JPEGクロス、破損/非対応/0バイト/巨大の異常系、保存衝突連番、中途出力なし。
- 各変換の恒等・決定性・寸法（1px境界含む）、プリセット再現性、バッチの件数一致/全件失敗の非クラッシュ。
- 実行: `python -m pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80`（`app/` で）。
- pre-commit/pre-push で black --check / ruff（`S`）/ pytest+cov をローカル強制。

## 配布
- PyInstaller で単一のWindows実行ファイルを生成（ローカル配布）。README に起動・ビルド手順。

## 参照（この unit の設計成果物）
- functional-spec.md / frontend-components.md（`../functional-design/`）
- performance-design.md / security-design.md / logical-components.md（`../nfr-design/`）
- performance-requirements.md / security-requirements.md / tech-stack-decisions.md（`../nfr-requirements/`）
- infrastructure-specification.md / monitoring-design.md / cicd-pipeline.md（`../infrastructure-design/`）
- code-generation-plan.md / unit-test-instructions.md（同ディレクトリ）
