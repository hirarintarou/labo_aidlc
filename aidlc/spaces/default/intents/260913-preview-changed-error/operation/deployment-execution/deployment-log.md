# デプロイ実行ログ — preview-changed-error（bugfix）

## 概要

ローカル完結アプリのため、デプロイ実行＝`main`（本 bugfix コミットを含む）のローカルインストール／実行環境更新。リモート環境・パイプライン push は非適用（team.md 準拠）。

## 実行内容

| 項目 | 内容 |
|---|---|
| 実行日 | 2026-09-14 |
| 対象 | `main`（`fix(ui): 調整・プリセット操作時のコンソールエラーを解消` を含む） |
| デプロイ先 | ローカル（`app/.venv` 実行環境） |
| 手順 | `cd-config.md` / `deployment-strategy.md` に従いローカル品質ゲート実行→スモークテスト |
| DB マイグレーション | 該当なし（DB を持たないアプリ） |
| 依存サービス | なし（ローカル・オフライン完結） |

## 事前チェック

- 全テスト green（55/55）、core/io カバレッジ 90%、ruff/black clean（Build and Test で確認済み）。
- 依存はピン留め済み（`pyproject.toml` / `uv.lock`）。

## 結果

- デプロイ（ローカル反映）: 成功。
- スモークテスト: 成功（`smoke-test-results.md` 参照）。
- 健全性チェック: 良好（`health-check-report.md` 参照）。

## ロールバック準備

- `rollback-runbook.md` のとおり、問題時は `git revert` または前タグ復帰で戻せる。今回は不要。
