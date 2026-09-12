# RAID Log — FF14 スクリーンショット加工ツール

RAID = Risks（リスク）/ Assumptions（前提）/ Issues（課題）/ Dependencies（依存）

## Risks

| ID | リスク | 影響 | 可能性 | 対応方針 | Source |
|----|--------|------|--------|----------|--------|
| R-1 | 「多彩な加工手段」の範囲が広がり、mvpの境界を越えて肥大化する | 中（納期・完成性） | 中 | scope-definitionで加工機能セットの最小限を明確に線引きする。 | [intent-statement] |
| R-2 | 加工結果が公式ガイドラインに反する形（過度な改変等）で公開される | 低〜中（法務・アカウント） | 低 | クレジット付与機能を提供し、ガイドライン遵守は利用者の判断に委ねる（自動チェックは範囲外と合意済み）。 | [Q5] |
| R-3 | 高解像度画像のバッチ処理で処理時間・メモリが増大する | 低 | 低 | mvpでは一般的なPNG/JPEG想定。性能目標はNFRステージで扱う。 | [Q3] |

## Assumptions

| ID | 前提 | 検証方法・確定時期 | Source |
|----|------|-------------------|--------|
| A-1 | 実装技術は実現しやすいものに任せてよい | Units Generation / Functional Designで具体選定・確定 | [Q2] |
| A-2 | 加工機能の具体セットはmvp範囲確定で決める | scope-definition / requirements-analysisで確定 | [intent-statement] |

## Issues

| ID | 課題 | 状態 | Source |
|----|------|------|--------|
| I-1 | 現時点で未解決の障害・課題はなし | Open（なし） | [intent-statement] |

## Dependencies

| ID | 依存 | 内容 | Source |
|----|------|------|--------|
| D-1 | 画像処理ライブラリ | 成熟した外部ライブラリに画像の読み書き・補正・合成を依存する（具体選定は後続） | [Q3][Q2] |

## Assumptions & Open Questions

None.
