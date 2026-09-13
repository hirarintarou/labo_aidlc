# 技術スタック

すべてのバージョンは `app/pyproject.toml` に固定（`app/uv.lock` で lock 管理）。

## 言語・ランタイム

- **Python** — 3.11（`requires-python = ">=3.11"`、`app/.python-version` = 3.11）

## ランタイム依存

- **PySide6** — 6.7.2 — GUI フレームワーク（Qt for Python）。`ui` 層のみが使用。
- **Pillow** — 10.4.0 — 画像処理（デコード・変換・保存）。`core`/`io` 層が使用。

## 開発・品質ツール（dev extra）

- **pytest** — 8.3.2 — テストランナー
- **pytest-cov** — 5.0.0 — カバレッジ計測
- **ruff** — 0.6.2 — lint（select: E, F, I, S, UP, B）
- **black** — 24.8.0 — フォーマッタ（line-length 100, target py311）
- **pre-commit** — 3.8.0 — ローカルフック
- **pyinstaller** — 6.10.0 — 配布用 exe 生成

## ビルド・パッケージ管理

- **uv** — パッケージ管理・仮想環境（`app/uv.lock` を管理）
- **hatchling** — ビルドバックエンド（build-system）。wheel パッケージは `screenshot_editor`
- **entry point**: `screenshot-editor = "screenshot_editor.__main__:main"`

依存の階層マッピング・利用方向は `dependencies.md` を参照。
