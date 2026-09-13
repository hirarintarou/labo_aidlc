# Security Requirements — screenshot-editor（mvp）

ローカル完結・オフライン・個人利用・秘密情報や個人データの収集なし。実質的な攻撃面は「サプライチェーン（依存ライブラリ）」と「未検証の画像ファイルのデコード」の2点に集約される [team-practices][constraint-register]。比例原則に沿って要件を定める。

## Threat Model（STRIDE 抜粋・該当のみ）

| 脅威 | 該当 | 対応 |
|------|------|------|
| Tampering（改ざん） | 元画像の破壊 | 非破壊保存で元画像を保護（SEC-3） |
| Denial of Service | 細工/巨大画像でのクラッシュ・メモリ枯渇 | 安全なデコードと入力検証（SEC-2） |
| Elevation/Injection 等（Web/サーバ系） | 非該当 | ネットワーク・認証・DBがないため対象外 |

## Security Requirements

| ID | 要件 | 根拠 |
|----|------|------|
| SEC-1 | すべての処理をローカルで完結させ、画像やデータを外部へ送信しない | NFR2 [team-practices] |
| SEC-2 | 入力画像は未検証データとして扱い、Pillowの標準APIで安全にデコードする。独自パーサを書かない。破損/非対応/巨大入力はエラーとして扱い、クラッシュ・過大メモリ確保を避ける | NFR1, team-practices（fail-fast） |
| SEC-3 | 非破壊保存：元画像を上書き・破壊しない。出力は一時ファイル→リネームのアトミック書き出し。出力パスのディレクトリトラバーサル（`..`）を避け、既存ファイル上書きに注意 | NFR3, team-practices |
| SEC-4 | 依存ライブラリ（Pillow, PySide6等）は正確なバージョンで固定し、ロックファイルをコミット。導入時に類似名（タイポスクワッティング）を目視確認する | team-practices |
| SEC-5 | リンタのセキュリティ系ルール（ruff）を有効化する。秘密情報は扱わないが、誤コミット防止に軽量なsecretスキャンを任意で導入してよい | team-practices |

## Out of Scope（過剰なもの）

- 認証/認可・暗号化・監査ログ・レート制限・WAF・KMS（ネットワーク・秘密情報がないため非該当）。
- DAST・重量級SAST・常設セキュリティゲート・コンテナ/IaCスキャン・常設SBOM（本スコープでは過剰）。

## Assumptions & Open Questions

None.
