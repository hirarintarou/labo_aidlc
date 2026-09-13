# Security Design — screenshot-editor（mvp）

security-requirements.md（SEC-1〜5）を満たす技術的アプローチ。ローカル完結・オフライン・個人利用 [security-requirements]。

## 設計

| 要件 | 設計アプローチ |
|------|--------------|
| SEC-1 ローカル完結 | ネットワークI/Oを行うコードを一切持たない。HTTP/socket等の外部通信ライブラリを import しない。 |
| SEC-2 未検証画像の安全デコード | `io` 層で Pillow の標準API（`Image.open` + `verify()`/`load()`）を用いる。独自パーサ非採用。`Image.MAX_IMAGE_PIXELS` を妥当な上限に設定しデコード爆弾（巨大画像）を防ぐ。破損/非対応は例外を捕捉し型付きドメインエラー（例 `UnsupportedImageError`, `CorruptImageError`）に変換、UI層で日本語メッセージへ。 |
| SEC-3 非破壊アトミック保存 | `io` 層で 同一ディレクトリに一時ファイル（例 `.tmp`）へ書き出し→`os.replace` でリネーム（原子的）。出力パスは `os.path` で正規化し `..` 等のトラバーサルを排除。元画像パスと出力パスの同一性チェックで上書き防止。既存 `_edited` 衝突時は連番付与（`_edited(1)` 等）で上書きしない（R-02対応）。 |
| SEC-4 依存固定 | `requirements.txt`（ハッシュ付き）または poetry lock をコミット。Pillow/PySide6等は実績あるパッケージを正確なバージョンで固定。導入時にパッケージ名を目視確認。 |
| SEC-5 リンタセキュリティルール | ruff のセキュリティ系ルール（`S`＝flake8-bandit相当）を有効化。任意で pre-commit に gitleaks。 |

## Error Type Hierarchy（core/io の型付きエラー）

```
ImageEditorError (基底)
├─ UnsupportedImageError   # 非対応フォーマット
├─ CorruptImageError       # 破損・デコード失敗
├─ ImageTooLargeError      # 上限超過（デコード爆弾防止）
└─ SaveError               # 書き込み失敗（ディスク/権限）
```
（≤15行の設計スニペット。実装はコード生成）

## Assumptions & Open Questions

- `MAX_IMAGE_PIXELS` の具体上限値はコード生成で設定。
