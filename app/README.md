# FF14 スクリーンショット加工ツール（screenshot-editor）

FF14 のスクリーンショットを公開する前に、手軽に綺麗に加工するためのローカル
Windows デスクトップアプリです。すべての処理はローカル・オフラインで完結し、
元画像は非破壊で保持します（加工結果は別ファイルに保存）。

## 主な機能

- PNG / JPEG を開いてプレビュー表示
- 基本補正（明るさ・コントラスト・彩度）、画質調整（シャープ・ぼかし・ノイズ除去）
- フィルタ／プリセット（組み込み 8 種）
- トリミング（自由矩形）・リサイズ（既定でアスペクト比保持）
- テキストクレジット付与（既定「© SQUARE ENIX」）
- 非破壊保存（同フォルダ・`_edited` 接尾辞・元と同形式・一時ファイル → リネームのアトミック保存）
- バッチ処理（複数ファイルに同じ設定を一括適用、失敗はスキップして継続、件数を表示）

## アーキテクチャ

レイヤーは `ui -> core -> io` の一方向依存です。`core`（画像変換ロジック）と
`io`（読み込み・非破壊保存）は GUI（PySide6）に一切依存しない純粋モジュールで、
Pillow の型はこれらの層の内側に閉じ込めています。

```
screenshot_editor/
├─ core/   画像変換ロジック（EditSettings, processor, presets）
├─ io/     安全デコード・非破壊アトミック保存（image_io）
├─ batch/  一括適用・集計（batch_processor）
└─ ui/     PySide6 画面（main_window, panels, batch_dialog）
```

## 技術スタック

- Python 3.11+
- PySide6（GUI） / Pillow（画像処理）
- pytest + pytest-cov（テスト） / ruff + black（lint・format）
- uv（パッケージ管理・仮想環境）
- PyInstaller（配布用 exe 生成）

## セットアップ

[uv](https://docs.astral.sh/uv/) を使います。`app/` ディレクトリで:

```
uv sync --extra dev
```

## 起動

```
uv run python -m screenshot_editor
```

## テスト

中核ロジック層（`core` / `io`）に 80% のラインカバレッジ下限を課しています。
`app/` ディレクトリで:

```
uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80
```

まとめて品質チェック（format 確認 + lint + テスト + カバレッジ）を実行する場合:

```
uv run python run_checks.py
```

## ビルド（Windows 向け単一 exe）

```
uv run pyinstaller --onefile --windowed --name screenshot-editor screenshot_editor/__main__.py
```

生成物は `dist/` 配下に出力されます。ローカルで実行してください。

## 注意（著作権・利用ガイドライン）

FF14 スクリーンショットの著作権はスクウェア・エニックスに帰属します。公開の際は
FF14 公式の画像利用ガイドラインに従ってください。本ツールのクレジット付与機能は
その遵守を助けることを目的としています。
