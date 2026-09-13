# Units Generation — Decomposition Plan & Questions

## Sources

- [scope] Workflow-selected scope: `mvp`.

> 4コンポーネント（AppUI / ImageProcessingCore / ImageIO / BatchProcessor）を、実装の「ユニット（作業のかたまり）」に分けます。これは「何をどう分けて作るか（依存関係）」を決める段階で、作る順番は次のDelivery Planningで決めます。ここでは配置・デプロイ形態も扱います。

## 分割のたたき台（案）

本ツールは単一のWindowsデスクトップアプリとして1つにまとめてビルド・配布します（ローカル完結・個人利用）。コンポーネントは論理的な内部構造であり、デプロイ単位としては1つです。したがって案は「1ユニット（アプリ全体）」を基本とします。

- **案A（推奨）**: 1ユニット `screenshot-editor`（kind: ui）。4コンポーネントを内包する単一のデスクトップアプリ。
- **案B**: 2ユニットに分割 — `imaging-core`（kind: library、Core+IO）と `desktop-app`（kind: ui、AppUI+Batch、coreに依存）。中核ロジックをライブラリとして分離。

---

## Q1. ユニットの分け方はどれがよいですか

- A. 1ユニット（アプリ全体をまとめて実装・配布）※推奨・シンプル
- B. 2ユニット（画像処理ライブラリ ＋ デスクトップアプリ）に分ける
- C. おまかせ
- X. Other (please specify)

[Answer]:A.

---

## Q2. デプロイ（配布）の形はどうしますか

- A. 単一のWindows向け実行ファイル/インストーラとして配布（ローカル完結）
- B. その他の希望がある（記入してください）
- X. Other (please specify)

[Answer]:A.

---

## Q3. ユニットの粒度・並行開発について希望はありますか

- A. こだわりなし（推奨案に従う）
- B. できるだけ細かく分けたい
- C. できるだけまとめたい
- X. Other (please specify)

[Answer]:A.

---

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct
