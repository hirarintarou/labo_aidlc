# Code Generation — Questions (screenshot-editor)

## Sources

- [scope] Workflow-selected scope: `mvp`.
- [artifact] `code-generation-plan.md`（実装計画・Testing Contract 埋め込み済み）
- [artifact] `unit-test-instructions.md`（このユニットのテスト方針・実行コマンド）

---

## Plan Approval

以下 2 つの成果物をレビューし、このままコード生成へ進んでよいか承認をお願いします。

- `code-generation-plan.md` — 実装ステップ（Step 1〜14）、ディレクトリ構成、Story→Code トレーサビリティ、埋め込み済み Testing Contract（methodology: test-after、中核ロジック層に 80% カバレッジ下限）
- `unit-test-instructions.md` — pytest + pytest-cov、このユニット限定の実行コマンド、非破壊保存・PNG/JPEG ラウンドトリップを P0 とするテスト範囲

技術スタック: Python 3.11+ / PySide6 / Pillow / pytest。アプリコードはワークスペースルート `app/` 配下、レイヤーは ui → core → io の一方向依存。

[Approval Fingerprint]: sha256:v3:7bab3414c8a9fedf2bf5a827d289c4e4f5f3676391e1925e687fb417bf6bcae6
[Planned Source]: b702f7a6dc3529d7b35c56513af12df20334d38f794e01fc5e212ce22d81ee80

- Approve Plan — コード生成へ進む
- Request Changes — 計画を修正する

[Answer]: Approve Plan
