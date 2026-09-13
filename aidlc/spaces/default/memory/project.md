# Project-Level Rules

> Project-specific specialisation and corrections. Loaded after `org.md` and
> `team.md` as strict-additive guidance; contradictions with broader policy
> are rejected. Populated by practices-discovery and the self-learning loop.
>
> Use sparingly: most teams don't need a project layer. Reach for it
> only when this specific project needs stable, durable guidance beyond the
> team practice (for example, package-specific release checks or an additional
> regression suite for a legacy component).

## Way of Working

<!-- Project-specific specialisation. Example: -->
<!-- This monorepo requires package-scoped branch names and a package owner -->
<!-- review in addition to the team's normal merge policy. -->

## Walking Skeleton

<!-- Project-specific specialisation. Example: -->
<!-- The walking skeleton must exercise the legacy service adapter as well -->
<!-- as the new service boundary. -->

## Testing Posture

<!-- Project-specific specialisation. -->

## Change Control

<!-- Project-specific. Mode: strict or relaxed. Strict here holds for every intent and cannot be changed from chat. -->

## Deployment

<!-- Project-specific specialisation. -->

## Code Style

<!-- Project-specific specialisation. -->

## Tech Stack

<!-- Technology choices locked for this project. -->

## Decided

<!-- Decisions made in earlier stages that should not be re-asked. -->
<!-- Format: DECIDED: [decision] (Stage [slug], [date]) -->

## Scope Overrides

<!-- Custom scope rules for this project. -->

## Forbidden

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: NEVER [behavior] (affirmed [date]) -->
<!-- Example: NEVER throw exceptions across service layer boundaries (affirmed 2026-05-17) -->

- NEVER 元画像ファイルを上書き・破壊する。 (affirmed 2026-09-12)

- NEVER 画像やユーザーデータを外部ネットワーク・第三者サービスへ送信する。 (affirmed 2026-09-12)

## Mandated

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: ALWAYS [behavior] (affirmed [date]) -->
<!-- Example: ALWAYS use Result<T,E> for fallible operations in service layer (affirmed 2026-05-17) -->

- ALWAYS 画像処理をローカル・オフラインで完結させる（外部サーバーへ画像やデータを (affirmed 2026-09-12)

送信しない）。 (affirmed 2026-09-12)

- ALWAYS 元画像を保持したまま非破壊で保存する（加工結果は別ファイルとして出力する）。 (affirmed 2026-09-12)

- ALWAYS git のコミットメッセージを日本語で記述する（ワークスペースのコミット (affirmed 2026-09-12)

メッセージ規約に従う）。 (affirmed 2026-09-12)

- ALWAYS PNG および JPEG の入出力をサポートする。 (affirmed 2026-09-12)

- ALWAYS 画像処理コアを UI から分離する（core は GUI に依存しない。依存方向は (affirmed 2026-09-12)

ui → core → io の一方向とし、コアは GUI を import しない）。 (affirmed 2026-09-12)

- ALWAYS 壊れた/非対応の入力を入力境界で早期に検証し、クラッシュさせず、ユーザー (affirmed 2026-09-12)

向けの日本語メッセージに変換する（fail fast）。 (affirmed 2026-09-12)

- ALWAYS 依存ライブラリを正確なバージョンで固定（ピン留め）し、ロックファイルを (affirmed 2026-09-12)

リポジトリにコミットする（導入時に類似名／タイポスクワッティングを目視確認する）。 (affirmed 2026-09-12)

- ALWAYS 読み込む画像を未検証データとして扱い、標準ライブラリ/選定ライブラリの (affirmed 2026-09-12)

API で安全にデコードする（独自パーサを書かない）。 (affirmed 2026-09-12)

- ALWAYS 保存は元画像を壊さず安全に書き出す（出力先の書き込み可否を検証し、可能なら (affirmed 2026-09-12)

一時ファイル → リネームのアトミック書き出しで中途半端な出力を残さない）。 (affirmed 2026-09-12)

## Corrections

<!-- Project-specific corrections from human feedback. -->
<!-- Format: NEVER/ALWAYS [behavior] (learned [date]) -->
- ALWAYS 会話言語（人が読む成果物・レビュー・質問・エージェントの応答）を日本語とする。 (learned 2026-09-14) (learned 2026-09-13) <!-- cid:260913-preview-changed-error:reverse-engineering:083a39932d1f4700783cd9d5b950d10dd18003a28d1853d6ff6d9aff5fa31580 -->
