# CI/CD Pipeline — screenshot-editor（mvp）

リモートCDは持たない（ローカルビルド=リリース）[delivery-planning][team-practices]。CIは**ローカルで機械的に強制する仕組み**を基本とする（Q5=A）。GitHub Actions等のリモートCIは任意（mvp必須ではない）。

## ローカル品質ゲート（必須）

コミット/プッシュ前に自動実行し、失敗時はコミット/プッシュを止める（pre-commit/pre-pushフック）[team-practices]:

| ステップ | 内容 | ツール |
|---------|------|--------|
| Format | コード整形チェック | black --check |
| Lint | 静的解析（セキュリティルール含む） | ruff（`S`ルール有効） |
| Type check | 型チェック（core中心） | mypy（任意） |
| Test | テスト実行＋カバレッジ下限 | pytest + pytest-cov（中核ロジック80%） |

- 仕組み: `pre-commit` フレームワーク、または単一のタスクスクリプト（例 `make test` / `tasks.py`）で「green＋カバレッジ下限」を強制。
- カバレッジ80%下限は**中核ロジック層（core/io）に限定**して計測（GUI/配線層は対象外）[team-practices][Q4]。

## ビルド／リリース

| ステップ | 内容 |
|---------|------|
| Build | PyInstaller で Windows実行ファイルを生成 |
| Release | 生成物をローカルで実行/配置。バージョンはgitタグで管理してよい |

- 本番承認ゲート・複数環境昇格・自動デプロイは適用外（ローカル完結）[delivery-planning]。

## リモートCI（任意・mvp外）

- 将来 GitHub Actions を入れる場合は、上記ローカルゲートと同じ（format/lint/type/test）をpush時に走らせる構成を推奨。mvpでは必須としない。

## Assumptions & Open Questions

- pre-commit設定・タスクスクリプトの具体はコード生成で作成する。
