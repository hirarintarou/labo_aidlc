# Code Generation — Plan Approval

## Plan Approval

対象: `code-generation-plan.md`（埋め込みの Testing Contract を含む）および `unit-test-instructions.md`。

このプランは `app/screenshot_editor/ui/panels.py` のシグナル配線バグを最小変更で修正し（引数を捨てるスロットで `changed` を発火）、回帰防止の UI テスト `app/tests/test_ui_panels.py` を 1 ファイル追加する内容です。依存方向 `ui → core → io` は不変、修正対象は `ui` 層に限定します。

Approve this exact Code Generation plan?

[Approval Fingerprint]: sha256:v3:64cafa63f96f05e1373cac3d15daefd88ed88f43f9283ecba1a45560aa27a321
[Planned Source]: 1bc8056527dcacff097ca69535fef3e23c37a2d0d448772507443a33a323ccda

- Approve Plan
- Request Changes

[Answer]: Approve Plan
