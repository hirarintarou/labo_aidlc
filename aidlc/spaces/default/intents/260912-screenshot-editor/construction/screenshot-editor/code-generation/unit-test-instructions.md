# Unit Test Instructions — screenshot-editor（mvp）

テスト方針: test-after。中核ロジック層（core/io）に80%ラインカバレッジ下限。非破壊保存とPNG/JPEGラウンドトリップを最重点（P0）[team-practices]。

## フレームワーク・設定

- パッケージ管理・仮想環境: **uv**（`uv sync` で `.venv` と依存を再現、`uv.lock` でピン留め）。
- テストランナー: **pytest**、カバレッジ: **pytest-cov**（いずれも `uv run` 経由で実行）。
- 設定は `app/pyproject.toml` の `[tool.pytest.ini_options]` と `[tool.coverage.run]`（`source = ["screenshot_editor.core", "screenshot_editor.io"]` でカバレッジ対象を中核層に限定）。

## このユニットのテスト実行コマンド（このユニット限定）

`app/` ディレクトリで（初回のみ `uv sync`）:

```
uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80
```

（プロジェクトは単一ユニットのため tests/ 全体がこのユニットのテスト。中核層のみカバレッジ判定。）

## テスト範囲（Standard strategy＋mvp floor）

- **test_image_io.py（P0）**: 非破壊（元画像バイト列・mtime不変）、PNG→PNG画素完全一致、JPEG→JPEG寸法/チャンネル一致＋許容誤差、PNG↔JPEGクロス各1、破損/非対応/0バイト/巨大入力の異常系、保存衝突時の連番、一時ファイル→リネームで中途出力なし。
- **test_processor.py**: 各変換の恒等一致・決定性、明るさ等の単調変化、トリミング/リサイズの寸法（1px境界含む）、クレジット合成、固定合成順序。
- **test_edit_settings.py**: 既定値=恒等、シリアライズ/複製。
- **test_presets.py**: 6〜10種の存在、同一入力・同一プリセットで決定的同一出力。
- **test_batch_processor.py**: 部分失敗スキップ継続、成功/失敗件数（n+m=総数）、全件失敗の非クラッシュ、進捗通知。
- コンポーネントあたり概ね5〜8テスト（Standard）。GUIのE2Eは最小限（骨組み疎通と共用）。

## モッキング・テストデータ

- 合成フィクスチャ画像（数pxのPNG/JPEG、アルファ有無）を `tests/conftest.py` でプログラム生成（バイナリ肥大回避）。
- ファイルI/Oは `tmp_path`（pytest）を使い、実ファイルで非破壊・アトミック保存を検証。
- GUIはユニットテスト対象外（core/ioを直接テスト）。

## カバレッジ目標

- 中核ロジック層（screenshot_editor.core, screenshot_editor.io）で **80%ライン下限**（`--cov-fail-under=80`）。GUI/配線層は対象外。
