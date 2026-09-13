# Unit of Work — FF14 スクリーンショット加工ツール（mvp）

単一のWindowsデスクトップアプリとして1ユニットで実装・配布する [Q1][Q2]。ドメイン設計の4コンポーネントはこのユニット内の内部構造として実装される。

## Units

| Unit ID | Directory | 名称 | kind | 説明 |
|---------|-----------|------|------|------|
| U1 | u1-screenshot-editor | screenshot-editor | ui | FF14スクショ加工デスクトップアプリ本体。AppUI / ImageProcessingCore / ImageIO / BatchProcessor を内包する。 |

## Unit Details

### U1: screenshot-editor (kind: ui)

- **責務**: FF14スクリーンショットの単体プレビュー編集（基本補正・画質調整・フィルタ・トリミング/リサイズ・クレジット付与）、非破壊保存、複数枚バッチ処理を提供する単一のデスクトップアプリ [requirements][stories]。
- **内包コンポーネント**: AppUI（画面層）、ImageProcessingCore（画像処理の中核）、ImageIO（読み書き・非破壊保存）、BatchProcessor（一括処理）[components]。
- **デプロイモデル**: standalone（単一のWindows向け実行ファイル/インストーラ、ローカル完結）[Q2]。
- **複雑度見積もり**: M（機能数は複数だが、いずれも標準的な画像処理でロジックは中規模）。
- **実装上の注記・制約**:
  - ui→core→io の一方向依存を守る。coreはGUIを import しない [team-practices]。
  - 画像処理ライブラリ・GUIフレームワークの具体名はこのユニットの機能設計/スタック選定で確定する。
  - 非破壊保存（一時ファイル→リネーム）・壊れた入力のfail-fast・依存バージョン固定を守る [team-practices]。

## Assumptions & Open Questions

- 技術スタックの具体（言語・GUI・画像処理ライブラリ）はConstructionの機能設計で確定する。
