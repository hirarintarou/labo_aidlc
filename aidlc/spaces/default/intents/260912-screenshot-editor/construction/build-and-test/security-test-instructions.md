# Security Test Instructions — screenshot-editor（mvp）

security-requirements.md（SEC-1〜5）に比例した軽量な検証手順。攻撃面は
「サプライチェーン（依存）」と「未検証画像のデコード」の 2 点に集約される。
重量級 SAST/DAST・常設セキュリティゲートは本スコープでは過剰（Out of Scope）。

## 実行（`app/` ディレクトリ）

### SEC-1 ローカル完結・外部送信なし（静的検査）

ネットワーク I/O ライブラリを import・使用していないことを確認する:

```
uv run python -c "import subprocess,sys; import pathlib; p=list(pathlib.Path('screenshot_editor').rglob('*.py')); import re; bad=[str(f) for f in p if re.search(r'^\s*(import|from)\s+(socket|http|urllib|requests|httpx|aiohttp|ftplib|smtplib)', f.read_text(encoding='utf-8'), re.M)]; print('NET IMPORTS:', bad); sys.exit(1 if bad else 0)"
```

期待: `NET IMPORTS: []`（一致なし）。

### SEC-2 未検証画像の安全デコード（テスト）

`tests/test_image_io.py` の異常系テストが担保する:
- 0 バイト → `CorruptImageError`
- 破損データ → `CorruptImageError`/`UnsupportedImageError`
- 非対応フォーマット（実体 GIF）→ `UnsupportedImageError`
- 画素数上限超過 → `ImageTooLargeError`（デコード爆弾防止）
- いずれもクラッシュせず型付きエラーに変換

```
uv run pytest tests/test_image_io.py -q
```

### SEC-3 非破壊アトミック保存（テスト）

`tests/test_image_io.py` が担保する:
- 保存後、元画像のバイト列・mtime が不変
- `_edited` 接尾辞・衝突時連番・元パスと同一にならない
- 保存失敗時に中途出力（一時ファイル）を残さない（`os.replace` 前で削除）

### SEC-4 依存固定・ロックファイル（静的検査）

```
uv lock --check
```

期待: `pyproject.toml` と `uv.lock` が整合（ドリフトなし）。依存は正確なバージョンで
ピン留め済み（PySide6==6.7.2, Pillow==10.4.0）。導入時にパッケージ名の
タイポスクワッティングを目視確認済み。

### SEC-5 リンタのセキュリティ系ルール（静的検査）

ruff のセキュリティ系ルール（`S` = flake8-bandit 相当）を有効化して実行:

```
uv run ruff check .
```

期待: セキュリティ系を含め違反なし（All checks passed）。

## Out of Scope（過剰）

- 認証/認可・暗号化・監査ログ・DAST・重量級 SAST・コンテナ/IaC スキャン・常設 SBOM。
  ネットワーク・秘密情報・サーバがないため非該当。

## Sources

- security-requirements.md（SEC-1〜5、STRIDE 抜粋）
- security-design.md（安全デコード・アトミック保存・ruff S 有効化）

## Assumptions & Open Questions

None.
