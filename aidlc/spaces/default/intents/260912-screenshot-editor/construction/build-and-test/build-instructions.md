# Build Instructions — screenshot-editor（mvp）

ローカル完結の Windows デスクトップアプリ。パッケージ管理・仮想環境は **uv**、
アプリコードはワークスペースルート `app/` 配下。ここでの「ビルド」はローカルの
依存インストール・パッケージング（PyInstaller）を指す（infrastructure-specification.md）。

## 前提

- Windows（64bit）
- [uv](https://docs.astral.sh/uv/) がインストール済み（`uv --version` で確認）
- uv が Python 3.11 を自動取得する（`.python-version` で固定）。ユーザー側の Python は不要

## 依存インストール（環境セットアップ）

`app/` ディレクトリで:

```
uv sync --extra dev
```

- 本体依存: PySide6==6.7.2, Pillow==10.4.0
- 開発依存（--extra dev）: pytest, pytest-cov, ruff, black, pre-commit, pyinstaller
- 依存は `pyproject.toml` に宣言し、`uv.lock` でピン留め（コミット対象、SEC-4）
- `.venv/` は uv が作成（バージョン管理対象外）

環境変数・外部サービス・config ファイルは不要（ローカル完結・オフライン、SEC-1）。

## ビルド検証（起動確認）

```
uv run python -m screenshot_editor
```

GUI ウィンドウが起動すれば疎通 OK。ヘッドレス環境では GUI 起動確認は省略し、
下記のモジュール byte-compile と import 確認で代替する:

```
uv run python -m compileall -q screenshot_editor
```

## パッケージング（配布用 exe 生成、任意・mvp）

```
uv run pyinstaller --onefile --windowed --name screenshot-editor screenshot_editor/__main__.py
```

生成物は `dist/` に出力（バージョン管理対象外）。ローカルで実行して配布する。

## トラブルシューティング

- **PySide6 のダウンロードが大きい/遅い**: 初回 `uv sync` は PySide6 が 100MB 超のため
  時間がかかる。2 回目以降はキャッシュされ高速。
- **GUI がヘッドレスで起動しない**: CI/ヘッドレスでは GUI 起動テストは行わない。
  core/io は GUI 非依存のため、テスト・カバレッジは GUI なしで実行できる。
- **`python` が Windows ストアのスタブに解決される**: 直接 `python` を使わず、
  必ず `uv run ...` 経由で実行する（uv 管理の 3.11 が使われる）。

## Sources

- infrastructure-specification.md（PyInstaller・Windows・オフライン）
- tech-stack-decisions.md / code-generation-plan.md（uv / Python 3.11 / PySide6 / Pillow）
- team.md（依存ピン留め・ロックファイルのコミット）

## Assumptions & Open Questions

- インストーラ化（Inno Setup 等）は mvp 外。PyInstaller の exe/フォルダ配布で足りる。
