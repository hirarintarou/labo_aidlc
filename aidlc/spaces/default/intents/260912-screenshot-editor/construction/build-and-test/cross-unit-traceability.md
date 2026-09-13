# Cross-Unit Final Coverage — screenshot-editor（mvp）

Construction 段階のクロスユニット最終カバレッジゲート（stage-level gate）。単一ユニット
（screenshot-editor）のため「クロスユニット」は 1 ユニット内のレイヤーを対象とする。
要件（FR/NFR）と 3 セグメント AC を列挙し、実装/テストファイル（実在確認済み）で被覆を検証する。

## 判定: PASS（mvp 必須スコープ）

すべての Must（mvp 必須）要件・AC が実装/テストで被覆され、対象ファイルは実在する。
Should（US1.9）のみ意図的に mvp 範囲外（未実装）。詳細は下表と末尾の所見を参照。

## Functional Requirements 被覆

| ID | 被覆 | 対象ファイル（実在） |
|----|------|-------------------|
| FR1.1 PNG/JPEG を開く | OK | app/screenshot_editor/io/image_io.py |
| FR1.2 中央プレビュー表示 | OK | app/screenshot_editor/ui/main_window.py |
| FR1.3 破損/非対応/0バイトの日本語エラー・非クラッシュ | OK | app/screenshot_editor/errors.py, app/tests/test_image_io.py |
| FR2.1 明るさ調整 | OK | app/screenshot_editor/core/processor.py |
| FR2.2 コントラスト調整 | OK | app/screenshot_editor/core/processor.py |
| FR2.3 彩度調整 | OK | app/screenshot_editor/core/processor.py |
| FR2.4 リアルタイム反映 | OK | app/screenshot_editor/ui/main_window.py |
| FR3.1 シャープ化 | OK | app/screenshot_editor/core/processor.py |
| FR3.2 ぼかし | OK | app/screenshot_editor/core/processor.py |
| FR3.3 ノイズ除去 | OK | app/screenshot_editor/core/processor.py |
| FR4.1 プリセット適用 | OK | app/screenshot_editor/core/presets.py |
| FR4.2 6〜10種のプリセット | OK | app/screenshot_editor/core/presets.py, app/tests/test_presets.py |
| FR5.1 トリミング | OK | app/screenshot_editor/core/processor.py |
| FR5.2 リサイズ | OK | app/screenshot_editor/core/processor.py |
| FR6.1 テキストクレジット付与 | OK | app/screenshot_editor/core/processor.py |
| FR6.2 位置・サイズ・不透明度指定 | OK | app/screenshot_editor/core/edit_settings.py (Credit) |
| FR6.3 既定テンプレート編集可 | Partial | app/screenshot_editor/core/edit_settings.py（既定「© SQUARE ENIX」は core 側。GUI 編集欄は未提供＝R-01） |
| FR6.4 ガイドライン遵守目的 | OK | app/README.md |
| FR7.1 非破壊・別ファイル保存 | OK | app/screenshot_editor/io/image_io.py |
| FR7.2 同フォルダ・接尾辞 | OK | app/screenshot_editor/io/image_io.py |
| FR7.3 同形式で出力 | OK | app/screenshot_editor/io/image_io.py, app/tests/test_image_io.py |
| FR7.4 中途出力を残さない | OK | app/screenshot_editor/io/image_io.py, app/tests/test_image_io.py |
| FR8.1 単体プレビュー編集 | OK | app/screenshot_editor/ui/main_window.py |
| FR8.2 左メニュー/中央プレビュー/右調整 | OK | app/screenshot_editor/ui/main_window.py |
| FR9.1 バッチ一括適用 | OK | app/screenshot_editor/batch/batch_processor.py |
| FR9.2 バッチも非破壊 | OK | app/screenshot_editor/batch/batch_processor.py |
| FR9.3 スキップ継続・件数表示 | OK | app/screenshot_editor/batch/batch_processor.py, app/tests/test_batch_processor.py |

## Non-Functional Requirements 被覆

| ID | 被覆 | 対象ファイル（実在） |
|----|------|-------------------|
| NFR1 想定外入力で非クラッシュ | OK | app/screenshot_editor/errors.py, app/tests/test_image_io.py |
| NFR2 ローカル完結・外部送信なし・依存固定 | OK | app/screenshot_editor/io/image_io.py, app/pyproject.toml, app/uv.lock |
| NFR3 元画像を非破壊 | OK | app/screenshot_editor/io/image_io.py, app/tests/test_image_io.py |
| NFR4 見やすい UI・キーボード操作 | OK | app/screenshot_editor/ui/panels.py, app/screenshot_editor/ui/main_window.py |
| NFR5 core を UI から分離・80% 下限 | OK | app/tests/test_processor.py（core/io 90.15%） |
| NFR6 プレビューのリアルタイム反映 | OK | app/screenshot_editor/ui/main_window.py |

## 3 セグメント AC 被覆

| ID | 被覆 | 対象ファイル（実在） |
|----|------|-------------------|
| AC0.1.1 骨組み疎通 | OK | app/tests/test_image_io.py, app/screenshot_editor/io/image_io.py |
| AC0.1.2 PNG 画素完全一致 | OK | app/tests/test_image_io.py (test_png_roundtrip_pixel_exact) |
| AC0.1.3 JPEG 許容誤差 | OK | app/tests/test_image_io.py (test_jpeg_roundtrip_dims_and_channels) |
| AC0.1.4 元画像バイト列・mtime 不変 | OK | app/tests/test_image_io.py (test_save_is_nondestructive_bytes_and_mtime) |
| AC1.1.1 プレビュー表示 | OK | app/screenshot_editor/ui/main_window.py |
| AC1.1.2 日本語エラー・非クラッシュ | OK | app/screenshot_editor/errors.py, app/tests/test_image_io.py |
| AC1.1.3 カテゴリでパネル切替 | OK | app/screenshot_editor/ui/main_window.py |
| AC1.2.1 明るさ恒等・単調増加 | OK | app/tests/test_processor.py (test_brightness_increases_luminance) |
| AC1.2.2 コントラスト恒等・決定的 | OK | app/screenshot_editor/core/processor.py, app/tests/test_processor.py |
| AC1.2.3 彩度恒等・決定的 | OK | app/tests/test_processor.py |
| AC1.3.1 シャープ化 | OK | app/screenshot_editor/core/processor.py |
| AC1.3.2 ぼかし恒等・決定的 | OK | app/screenshot_editor/core/processor.py |
| AC1.3.3 ノイズ除去決定的 | OK | app/screenshot_editor/core/processor.py |
| AC1.4.1 プリセット再現性 | OK | app/tests/test_presets.py (test_preset_application_is_deterministic) |
| AC1.4.2 6〜10種 | OK | app/tests/test_presets.py (test_builtin_preset_count_in_range) |
| AC1.5.1 トリミング寸法一致 | OK | app/tests/test_processor.py (test_crop_dimensions) |
| AC1.5.2 リサイズ寸法・恒等・1px 境界 | OK | app/tests/test_processor.py (test_resize_*, test_resize_one_pixel_boundary) |
| AC1.6.1 クレジット合成 | OK | app/tests/test_processor.py (test_credit_changes_image) |
| AC1.6.2 既定テンプレート編集可 | Partial | app/screenshot_editor/core/edit_settings.py（既定値は core。GUI 編集欄は未提供＝R-01） |
| AC1.6.3 ガイドライン遵守目的 | OK | app/README.md |
| AC1.7.1 別ファイル保存 | OK | app/tests/test_image_io.py (test_save_uses_edited_suffix) |
| AC1.7.2 元画像不変 | OK | app/tests/test_image_io.py (test_save_is_nondestructive_bytes_and_mtime) |
| AC1.7.3 同形式出力 | OK | app/screenshot_editor/io/image_io.py |
| AC1.7.4 中途出力なし | OK | app/tests/test_image_io.py (test_save_failure_leaves_no_partial_file) |
| AC1.7.5 PNG 画素完全一致 | OK | app/tests/test_image_io.py (test_png_roundtrip_pixel_exact) |
| AC1.7.6 JPEG 許容誤差 | OK | app/tests/test_image_io.py (test_jpeg_roundtrip_dims_and_channels) |
| AC1.8.1 リセットで初期化 | OK | app/screenshot_editor/ui/main_window.py, app/screenshot_editor/ui/panels.py |
| AC1.8.2 リセットで元画像不変 | OK | app/screenshot_editor/io/image_io.py |
| AC1.9.1 加工前と比較 | Not covered (out of mvp) | — (Should。mvp 必須外・最初の目安外。意図的に未実装) |
| AC2.1.1 一括適用・非破壊 | OK | app/screenshot_editor/batch/batch_processor.py, app/tests/test_batch_processor.py |
| AC2.1.2 失敗スキップ・全件失敗非クラッシュ | OK | app/tests/test_batch_processor.py (test_partial_failure_*, test_all_failure_*) |
| AC2.1.3 成功n/失敗m・n+m=総数 | OK | app/tests/test_batch_processor.py (test_all_failure_does_not_crash, summary_ja) |
| AC2.1.4 進捗表示 | OK | app/screenshot_editor/ui/batch_dialog.py, app/tests/test_batch_processor.py (test_progress_callback_invoked) |
| ACX.1 キーボード主要動線 | Partial | app/screenshot_editor/ui/main_window.py（大きめボタン・objectName 付与。完全な WCAG 準拠は支援技術での手動検証が別途必要） |
| ACX.2 Esc でダイアログを閉じる | OK | app/screenshot_editor/ui/batch_dialog.py (keyPressEvent) |

## 所見（承認ゲートで要判断）

- **F-1（Partial）FR6.3 / AC1.6.2 クレジットの既定テンプレート編集**: core（EditSettings.Credit）に
  実装済みだが、GUI 上の編集欄が未提供（現状はメイン画面で既定 Credit 固定）。mvp の「最初の目安」には
  クレジット付与は含まれるが、編集 UI の充足は build-and-test 以降 / 将来拡充候補（レビュー R-01）。
- **F-2（Not covered・意図的）AC1.9.1 加工前と比較**: US1.9 は Should で mvp 必須外・最初の目安外。
  意図的に未実装。ゲートの判断材料として明記。
- **F-3（Partial）ACX.1 キーボード主要動線**: 大きめ UI・objectName 付与で配慮済みだが、
  完全な WCAG 準拠の確証には支援技術での手動検証と専門レビューが別途必要（stories.md の但し書きどおり）。

上記はいずれも mvp 必須スコープのブロッカーではない。Must 要件・Must AC はすべて OK。

## Sources

- requirements.md（FR1.1〜FR9.3、NFR1〜6）
- stories.md（AC0.1.x〜AC2.1.x、ACX.1/2、US1.9）
- code-generation/traceability.json（ユニット被覆の起点）
- app/ 配下の実装・テスト（実在確認済み）
