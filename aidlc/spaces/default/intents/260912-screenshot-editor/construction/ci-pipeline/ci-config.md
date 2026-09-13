# CI Configuration — screenshot-editor（mvp）

team.md の方針（CI ゲート Q5=A）に従い、**リモート CI サービスは必須としない**。
ローカルの pre-commit / pre-push フックと単一タスクスクリプト `run_checks.py` で
品質ゲートを機械的に強制することを「CI」と見なす。ローカル完結・オフライン・個人利用の
Windows デスクトップアプリという性質に比例した構成とする。

## パイプラインの位置づけ

- **トリガ**: ローカルの git フック（pre-commit / pre-push）と、任意の手動実行（`run_checks.py`）。
- **実行環境**: 開発者の Windows PC（uv 管理の Python 3.11）。リモートランナー・クラウドは不使用。
- **ブランチ戦略**: 単一リポジトリの trunk-based。短命ブランチ → `main` に squash-merge。

## ステージ（ローカルパイプライン）

`app/` を対象に、次の順で実行する（`app/run_checks.py` が一括実行、`.pre-commit-config.yaml` が git フック連携）:

| # | ステージ | コマンド（`app/` 内、`uv run` 経由） | 失敗時 |
|---|---------|--------------------------------------|--------|
| 1 | 依存同期 | `uv sync --extra dev` | 中断 |
| 2 | フォーマット確認 | `uv run black --check .` | 失敗（pre-commit でブロック） |
| 3 | Lint（セキュリティ S 含む） | `uv run ruff check .` | 失敗（pre-commit でブロック） |
| 4 | テスト＋カバレッジ | `uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-report=term-missing --cov-fail-under=80` | 失敗（pre-push でブロック） |
| 5 | 依存ロック整合 | `uv lock --check` | 失敗（pre-push でブロック） |

- 実体は既にリポジトリに存在: `app/.pre-commit-config.yaml`（black/ruff/pytest フック）、
  `app/run_checks.py`（black --check → ruff → pytest+cov を順に実行する単一タスクスクリプト）。

## ローカルフックの導入手順

`app/` で（初回のみ）:

```
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

以降、コミット時に black/ruff、プッシュ時に pytest+カバレッジが自動実行される。
手動でまとめて確認する場合:

```
uv run python run_checks.py
```

## 参考: リモート CI の任意サンプル（必須ではない）

将来 GitHub でリモート CI を使いたくなった場合の最小サンプル（本 mvp では未導入）。
このリポジトリはローカル完結方針のため、導入は任意。

```yaml
# .github/workflows/ci.yml （任意・未導入のサンプル）
name: ci
on:
  push:
    branches: [main]
  pull_request:
jobs:
  check:
    runs-on: windows-latest
    defaults:
      run:
        working-directory: app
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      - run: uv sync --extra dev
      - run: uv run black --check .
      - run: uv run ruff check .
      - run: uv run pytest tests/ --cov=screenshot_editor.core --cov=screenshot_editor.io --cov-fail-under=80
      - run: uv lock --check
```

## アーティファクト

- ビルド成果物は PyInstaller によるローカル生成物（`dist/` の exe）。アーティファクトリポジトリ
  （ECR/CodeArtifact/S3）は不使用。`dist/`・`build/` はバージョン管理対象外（`app/.gitignore`）。

## Sources

- team.md（Way of Working / Testing Posture / Deployment、CI ゲート Q5=A）
- infrastructure-specification.md（Windows・PyInstaller・オフライン）
- build-and-test-summary.md / test-results.md（ローカルの pytest+coverage・ruff・black の実績）
- 実体: app/.pre-commit-config.yaml, app/run_checks.py, app/pyproject.toml

## Assumptions & Open Questions

- リモート CI は将来任意導入。mvp ではローカルゲートで足りる。
