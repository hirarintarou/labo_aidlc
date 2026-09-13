# Tech Stack Decisions — screenshot-editor（mvp）

技術スタックが未確定（「実現しやすい技術におまかせ」[requirements A1]）であったため、本ステージで確定する。

## 決定

| 項目 | 選定 | 根拠 |
|------|------|------|
| 言語 | **Python 3.11+** | 成熟した画像処理エコシステム、個人開発での扱いやすさ、Windowsで動作 |
| GUIフレームワーク | **PySide6（Qt for Python）** | Windowsで安定した高品質GUI、大きめの文字/ボタン等の調整が容易（NFR4）、単一ウィンドウ・プレビュー中心UIに適する |
| 画像処理ライブラリ | **Pillow (PIL)** | PNG/JPEGの読み書き・補正・フィルタ・トリミング/リサイズ・テキスト合成を標準的に提供。広く使われ活発に保守（サプライチェーン健全）[team-practices] |
| テスト | **pytest + pytest-cov** | test-after方針、中核ロジック80%カバレッジ計測（NFR5）。プロパティテストは pytest+Hypothesis を任意で |
| Lint/Format | **ruff（lint）+ black（format）** | Python標準的。ruffはセキュリティ系ルールも一部カバー |
| 型チェック | **mypy**（任意、coreに適用） | core層の型安全性 |
| パッケージング | **PyInstaller** | 単一のWindows向け実行ファイル/インストーラを生成（ローカル配布）[delivery-planning] |
| 依存管理 | **pip + requirements.txt（ハッシュ付き）** or poetry | バージョン固定＋ロックファイルをコミット（NFR2）[team-practices] |

## レイヤーとモジュール対応（ui→core→io）

- `ui/`（PySide6）: ウィンドウ・メニュー・パネル・プレビュー。core を呼ぶのみ。
- `core/`（純粋Python + Pillowをラップ）: EditSettings、各変換（補正/画質/フィルタ/トリミング/リサイズ/クレジット合成）、プリセット定義。GUI非依存。
- `io/`（Pillow）: 読み込み・フォーマット判定・非破壊のアトミック保存（一時ファイル→リネーム）。
- Pillow型は core/io の内側に閉じ込め、ui へ漏らさない [team-practices]。

## Assumptions & Open Questions

- 具体的なバージョンピンはコード生成時に requirements.txt で固定する。
