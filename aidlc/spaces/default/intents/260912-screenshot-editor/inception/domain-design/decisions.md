# Architecture Decision Records — FF14 スクリーンショット加工ツール（mvp）

## ADR-001: ui→core→io の3層分離を採用する

- **Context**: 確定プラクティス（team-practices）で「画像処理コアをUIから分離（依存方向 ui→core→io）」が硬い制約（Mandated）。中核ロジックに80%カバレッジを課すため、GUIを起動せずにテストできる境界が必要 [team-practices][requirements NFR5]。
- **Decision**: AppUI（画面）／ImageProcessingCore（純粋な画像処理）／ImageIO（副作用のある入出力）の3層に分離し、依存を一方向に限定する。coreはGUIも I/O も import しない。
- **Consequences**: (＋) coreを単体テストで検証可能、非破壊保存・ラウンドトリップのP0テストが現実的。(＋) 変更頻度の高いUIと安定した画像処理を分離。(−) 層をまたぐ受け渡し（EditSettings・結果画像）の設計が必要で、小規模ツールとしてはやや構造が増える。
- **Alternatives Rejected**: UIと画像処理を一体化した単層構成 — 実装は速いが、確定プラクティスに反し、GUI抜きの単体テストが困難になるため却下。

## ADR-002: BatchProcessor を独立コンポーネントにする

- **Context**: バッチ処理は「1つの設定を複数ファイルに反復適用し、部分失敗をスキップして集計する」という、単体編集とは異なる関心・ライフサイクルを持つ [requirements FR9][stories US2.1]。
- **Decision**: BatchProcessor を独立コンポーネントとし、ImageProcessingCore と ImageIO を再利用させる。
- **Consequences**: (＋) 反復・集計・部分失敗ハンドリングを1箇所に集約でき、単体編集ロジックを汚さない。(＋) core/io を再利用しつつバッチ固有の振る舞い（進捗・集計）を明確化。(−) コンポーネントが1つ増える。
- **Alternatives Rejected**: BatchProcessor を ImageProcessingCore に含める（Q1-B）— core の純粋変換に反復・集計・I/O調整という別関心が混ざり、core の純粋性とテスト容易性を損なうため却下 [Q1]。

## ADR-003: EditSettings と PresetDefinition を ImageProcessingCore が所有する

- **Context**: 加工設定は単体編集でもバッチでも使う中心データ。それを解釈して画像を変換するのは core である [Q2][Q3]。
- **Decision**: EditSettings（加工設定の集合）と PresetDefinition（組み込みプリセット、mvpは6〜10種）を ImageProcessingCore が所有する。
- **Consequences**: (＋) 設定の定義と、それを適用する変換ロジックが同じ境界にあり凝集度が高い。(＋) 単体編集とバッチが同一の EditSettings 型を共有できる。(−) core が設定モデルの変更にも影響を受ける（許容範囲）。
- **Alternatives Rejected**: 独立した設定コンポーネント（Q2-B）— 小規模mvpでは過剰な分割で、core と密結合な設定を別部品にする利点が薄いため却下。外部ファイル/ユーザー定義プリセット（Q3-B）はmvp外とした。

## Assumptions & Open Questions

None.
