# Deployment Pipeline — 確認質問

本 intent は bugfix であり、team.md の Deployment 方針（デプロイ＝ローカルビルド/インストール、CD パイプライン・複数環境・本番承認ゲートは適用外）が既に確定しています。以下は方針の確認です。

## Q1. デプロイ戦略の確認

デプロイ戦略は「ローカル再ビルド/再インストール」（CD パイプライン・環境昇格なし）で確定してよいですか。

- A. はい（team.md の方針どおり、ローカルビルド/インストール）
- B. いいえ（別途 CD/環境を設けたい）
- X. Other (please specify)

[Answer]: A

## Q2. ロールバック手順の確認

ロールバックは `git revert`（または前リリースタグへの復帰）＋ローカル再検証・再起動で確定してよいですか。

- A. はい（rollback-runbook.md のとおり）
- B. いいえ（別手順を希望）
- X. Other (please specify)

[Answer]: A

---

## Consolidated Summary Confirmation

- デプロイ戦略: ローカル再ビルド/再インストール（CD パイプライン・複数環境・本番承認ゲートなし）。team.md 準拠。
- 品質ゲート: ローカルフック（pre-commit / pre-push / `run_checks.py`）。UI 回帰テストはヘッドレス実行（`QT_QPA_PLATFORM=offscreen`）に注意。
- ロールバック: `git revert` または前タグ復帰＋ローカル再検証・スモーク。元画像は非破壊で保護。

Does this all look correct before I generate the requirements artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
