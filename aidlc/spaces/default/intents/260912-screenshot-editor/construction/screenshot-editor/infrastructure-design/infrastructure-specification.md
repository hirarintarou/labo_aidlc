# Infrastructure Specification — screenshot-editor（mvp）

本ツールは**ローカル完結のWindowsデスクトップアプリ**であり、クラウド／サーバインフラは持たない [constraint-register][tech-stack-decisions]。ここでの「インフラ」は、ローカルのビルド・パッケージング・配布環境を指す。

## Deployment Target

- **実行環境**: エンドユーザー（＝制作者本人）のWindows PC。ローカルインストール／実行。
- **サーバ・クラウド**: なし（外部通信なし、SEC-1）。AWS等のクラウドリソースは使用しない。

## Build & Packaging

| 項目 | 内容 |
|------|------|
| ランタイム | Python 3.11+（PyInstallerで同梱するため利用者のPythonインストールは不要） |
| 依存 | PySide6, Pillow（`requirements.txt` にハッシュ付きで固定）[SEC-4] |
| パッケージング | **PyInstaller** で単一のWindows実行ファイル（`.exe`、`--onefile` または `--onedir`）を生成 |
| 配布 | 生成した実行ファイル/フォルダをローカルで実行。インストーラ化は任意（mvpはexe配布で足りる） |
| ビルド環境 | 開発者のWindows環境。仮想環境（venv）で依存を隔離 |

## Runtime Requirements

- OS: Windows（64bit想定）
- 追加ランタイム: なし（PyInstaller同梱）
- ネットワーク: 不要（オフライン動作）

## Cost

- クラウドコストなし（ローカル完結）。

## Assumptions & Open Questions

- インストーラ（Inno Setup等）の採否はmvp外。まずはPyInstallerのexe/フォルダ配布とする。
