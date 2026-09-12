---
inclusion: always
---

# AI-DLC 進行時のコミット方針

AI-DLC ワークフローを進める際は、適切なタイミングで**自動的にコミットする**。これは必須のルールとする。

## コミットするタイミング

- **ステージの承認ゲートを通過したとき**（各ステージの成果物・questions ファイルへの回答・memory 更新が確定した時点）でコミットする。
- **フェーズ（ideation / inception / construction / operation）を完了したとき**は、そのフェーズの区切りが分かるようにコミットする。
- Construction フェーズでコード生成が行われた場合は、生成・変更されたアプリケーションコードもコミット対象に含める。
- 1回のコミットは1つの論理的な作業単位（原則として1ステージ、または密接に関連する一連の成果物）にまとめる。無関係な変更を混ぜない。

## コミット対象

AGENTS.md の Git Integration 方針に従う。

- `aidlc/` ワークツリー（intent 記録、`aidlc-state.md`、`audit/` シャード、`intents.json`、memory、codekb、knowledge）はバージョン管理対象に含める。
- アプリケーションコード（ワークスペースルートまたは兄弟リポジトリ）も含める。
- `.gitignore` で除外されるファイル（per-user カーソル、`aidlc/.aidlc-clone-id`、`aidlc/.aidlc-sessions/`、各種スクラッチ／キャッシュ）はコミットしない。

## コミットメッセージ

- グローバルステアリングの規約に従い、**日本語**で記述する。
- どのステージ・フェーズの区切りかが分かる件名にする（例: `chore(aidlc): ideation フェーズ feasibility ステージの成果物を記録`）。

## 進め方

- 破壊的な git 操作（force push、reset --hard など）は行わない。
- 特に指示がない限り main / master に直接プッシュしない。プッシュは明示的な指示があったときのみ行う。
