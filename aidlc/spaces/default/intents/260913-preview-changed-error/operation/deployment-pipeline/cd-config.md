# CD 構成 — preview-changed-error（bugfix）

## 方針

team.md に従い、リモート CD パイプライン（GitHub Actions / CodePipeline 等）は構築しない。品質ゲートは**ローカルフック**で機械強制する（Q5=A）。「CD 構成」はローカルのリリース準備手順として定義する。

## ローカル品質ゲート（既存構成の踏襲）

- `app/.pre-commit-config.yaml`: pre-commit（black / ruff）、pre-push（pytest＋coverage）。
- `app/run_checks.py`: `black --check` / `ruff` / `pytest`＋coverage を一括実行する単一スクリプト。
- 本 bugfix で追加した UI 回帰テストはヘッドレス実行（`QT_QPA_PLATFORM=offscreen`）を要する。`run_checks.py` / フック経由で実行する際は当該環境変数が設定されることを確認する（未設定だと UI テストが表示接続で失敗しうる）。

## リリース準備コマンド（`app/` ディレクトリ）

```bash
# 品質ゲート一括（ヘッドレス）
QT_QPA_PLATFORM=offscreen python run_checks.py
# 配布物（任意）
python -m PyInstaller --noconfirm --windowed --name screenshot-editor screenshot_editor/__main__.py
```

## 環境昇格マトリクス

| 環境 | 用途 | 昇格ゲート |
|---|---|---|
| local | 開発・利用（唯一の環境） | ローカル品質ゲート green ＋手動スモーク |

（staging / production は存在しない。）
