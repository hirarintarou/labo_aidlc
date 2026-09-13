# CI Pipeline — Questions (screenshot-editor)

## Sources

- [scope] Workflow-selected scope: `mvp`.
- [memory:team] team.md Way of Working / Testing Posture / Deployment（trunk-based、ローカル CI ゲート、ローカルビルド）
- [artifact] infrastructure-specification.md（Windows・PyInstaller・オフライン）
- [artifact] build-and-test-summary.md / test-results.md（ローカルの pytest+coverage・ruff・black）

> Construction フェーズのため質問は例外的。以下 4 つの論点は先行ステージ（team.md、
> infrastructure-specification.md）で既に決定済みのため、再質問せず決定内容を記録する。

## Questions

### Q1. 使用する CI ツールは何か
- **[Answer]: X. Other（決定済み）— リモート CI サービスは使用しない。** team.md（CI ゲート Q5=A）に従い、
  ローカルの pre-commit / pre-push フックと単一タスクスクリプト `run_checks.py` で「テスト green ＋
  中核層カバレッジ下限」を機械的に強制する。参考として GitHub Actions の任意サンプルは提示するが必須としない。

### Q2. ブランチ戦略は何か
- **[Answer]: X. Other（決定済み）— 単一リポジトリの trunk-based development。** 短命の作業ブランチを経て
  `main` にマージ（squash-merge）。個人開発のため形式的な PR レビューは省略し、ローカルゲートで品質担保。

### Q3. マージ前に必要な品質ゲートは何か
- **[Answer]: X. Other（決定済み）—** (1) テストスイート全体が green、(2) 中核ロジック層（core/io）の
  ラインカバレッジ ≥ 80%、(3) ruff（セキュリティ系 S ルール含む）違反なし、(4) black フォーマット準拠、
  (5) 依存ロック（uv.lock）整合。これらを pre-push とタスクスクリプトで強制する。

### Q4. 使用するアーティファクトリポジトリは何か
- **[Answer]: X. Other（決定済み）— なし。** ローカル完結・オフライン・個人利用のデスクトップアプリのため、
  ECR/CodeArtifact/S3 等は不使用。配布物は PyInstaller によるローカル生成物（exe）とする。

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
