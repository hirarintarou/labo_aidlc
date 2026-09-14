# ビルド手順 — preview-changed-error（bugfix / Minimal）

## 前提

- 本アプリはローカル完結の Python デスクトップアプリ（`app/` ディレクトリ）。コンパイル型のビルド成果物は通常不要（配布時のみ PyInstaller）。
- Python 3.11、依存は `app/pyproject.toml` にピン留め（PySide6==6.7.2, Pillow==10.4.0）。dev 依存に pytest / pytest-cov / ruff / black を含む。
- 仮想環境は `app/.venv`。パッケージ管理は uv。

## 依存インストール

`app/` ディレクトリで:

```bash
uv sync --extra dev
```

（本環境では `app/.venv` が既に構築済み。以降のコマンドは `.venv/Scripts/python.exe` を用いて実行する。）

## 環境設定

- GUI（PySide6）を含むテストはヘッドレスで実行する。環境変数を設定:
  - bash: `export QT_QPA_PLATFORM=offscreen`
  - PowerShell: `$env:QT_QPA_PLATFORM = "offscreen"`
- 外部サービス・ネットワーク・シークレットは不要（ローカル・オフライン完結）。

## ビルド / 検証コマンド

コンパイル不要のため、ビルド検証は import 健全性・lint・format・テストで代替する（`app/` ディレクトリ）:

```bash
# lint（セキュリティ系 S 規則を含む）
python -m ruff check .
# format 検証
python -m black --check .
# import 健全性（アプリのエントリが読み込めること）
python -c "import screenshot_editor; import screenshot_editor.ui.panels"
```

## ビルド検証ステップ

- `ruff check .` が `All checks passed!` を返すこと。
- `black --check .` が全ファイル unchanged を返すこと。
- `import screenshot_editor.ui.panels` が例外なく成功すること。

## トラブルシューティング

- Qt 実行時に「could not connect to display」等が出る場合: `QT_QPA_PLATFORM=offscreen` の設定漏れ。
- `python` が Windows Store スタブに解決される場合: `app/.venv/Scripts/python.exe` を明示的に使う。
