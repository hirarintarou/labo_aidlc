# デプロイ戦略 — preview-changed-error（bugfix）

## 前提（team.md Deployment に準拠）

本アプリはローカル完結・Windows 専用・個人利用のデスクトップアプリ。**「デプロイ」＝自分向けのローカルビルド/インストール**であり、リモート環境（staging/production）・CD パイプライン・本番承認ゲートは適用外。トランクは 1 本（`main`）。

## デプロイ戦略

- 戦略: **ローカル再ビルド/再インストール**（blue-green / canary / rolling は非適用）。
- 環境昇格: なし（単一環境＝ローカル）。
- リリース単位: `main` にマージ済みの修正コミット。必要に応じてタグ（例 `v0.1.1`）を付与。
- 成果物: 実行可能ファイル/インストーラ（PyInstaller）または `uv sync` 済みのローカル実行環境。

## リリース手順

1. `main` が最新（本 bugfix コミットを含む）であることを確認。
2. `app/` でローカル検証: `QT_QPA_PLATFORM=offscreen python -m pytest -q`（全 green）、`ruff check .` / `black --check .`（clean）。
3. アプリを起動して手動スモークテスト（後述 Deployment Execution）。
4. 配布が必要な場合のみ PyInstaller で exe を生成（任意）。
5. 任意でリリースタグを付与。

## トラフィック切り替え / アボート条件

- 非適用（単一ローカル環境、トラフィック概念なし）。スモークテスト失敗時は起動を中止し、ロールバック手順へ。
