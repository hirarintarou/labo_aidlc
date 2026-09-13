"""画像の安全な読み込みと非破壊アトミック保存（io 層）。

security-design.md / functional-spec.md に対応:
- 読み込む画像は未検証データとして扱い、Pillow の標準 API（open + verify/load）で
  安全にデコードする（独自パーサは書かない）。
- Image.MAX_IMAGE_PIXELS 相当の上限でデコード爆弾（巨大画像）を防ぐ。
- 破損 / 非対応 / 0 バイト / 巨大は型付きドメインエラーへ変換する（fail fast）。
- 保存は元画像を壊さず、同フォルダに `_edited` 接尾辞・元と同形式で、
  一時ファイル -> os.replace のアトミック書き出しを行う。衝突時は連番。
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from screenshot_editor.errors import (
    CorruptImageError,
    ImageTooLargeError,
    SaveError,
    UnsupportedImageError,
)

#: 対応する画像フォーマット（拡張子小文字 -> Pillow フォーマット名）
_SUPPORTED_EXT_TO_FORMAT: dict[str, str] = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
}

#: 対応 Pillow フォーマット名の集合
_SUPPORTED_FORMATS: frozenset[str] = frozenset({"PNG", "JPEG"})

#: デコード爆弾防止の画素数上限（幅 x 高さ）。一般的なスクリーンショットに十分な上限。
#: 例: 15360 x 8640 (16K 相当) を超える画素数の画像は拒否する。
DEFAULT_MAX_IMAGE_PIXELS: int = 15360 * 8640  # = 132,710,400 px

#: JPEG 保存時の既定品質
DEFAULT_JPEG_QUALITY: int = 95


def detect_format(path: str | os.PathLike[str]) -> str:
    """パスの拡張子から対応フォーマット名（"PNG" / "JPEG"）を返す。

    非対応拡張子は UnsupportedImageError。拡張子だけで判定し、実体の検証は
    load_image で行う（拡張子と実体の不一致は load_image が捕捉する）。
    """
    ext = Path(path).suffix.lower()
    fmt = _SUPPORTED_EXT_TO_FORMAT.get(ext)
    if fmt is None:
        raise UnsupportedImageError(
            f"unsupported extension: {ext!r}",
            user_message="このファイルは開けませんでした（対応形式は PNG / JPEG です）。",
        )
    return fmt


def load_image(
    path: str | os.PathLike[str],
    *,
    max_pixels: int = DEFAULT_MAX_IMAGE_PIXELS,
) -> Image.Image:
    """画像を安全に読み込み、RGB/RGBA の Pillow Image を返す。

    入力境界での早期検証（fail fast）:
    - 0 バイト / 破損 / デコード失敗 -> CorruptImageError
    - 非対応フォーマット -> UnsupportedImageError
    - 画素数上限超過 -> ImageTooLargeError

    返す Image はメモリ上に load 済みで、元ファイルのハンドルは保持しない。
    """
    p = Path(path)
    if not p.is_file():
        raise CorruptImageError(
            f"not a file: {p!r}",
            user_message="このファイルは開けませんでした（ファイルが見つかりません）。",
        )
    if p.stat().st_size == 0:
        raise CorruptImageError(
            "empty file (0 bytes)",
            user_message="このファイルは中身が空のため、画像として読み込めませんでした。",
        )

    # verify() 用に一度開く（verify 後の Image は使えないため開き直す）。
    try:
        with Image.open(p) as probe:
            fmt = probe.format
            probe.verify()
    except UnidentifiedImageError as exc:
        raise UnsupportedImageError(
            f"unidentified image: {p!r}",
            user_message="このファイルは開けませんでした（対応形式は PNG / JPEG です）。",
        ) from exc
    except (OSError, SyntaxError, ValueError) as exc:
        raise CorruptImageError(
            f"verify failed: {p!r}: {exc}",
            user_message="このファイルは壊れているか、画像として読み込めませんでした。",
        ) from exc

    if fmt not in _SUPPORTED_FORMATS:
        raise UnsupportedImageError(
            f"unsupported format: {fmt!r}",
            user_message="このファイルは開けませんでした（対応形式は PNG / JPEG です）。",
        )

    # 実際に画素を読み込む。巨大画像はここで上限チェック。
    try:
        image = Image.open(p)
        width, height = image.size
        if width * height > max_pixels:
            image.close()
            raise ImageTooLargeError(
                f"image too large: {width}x{height} > {max_pixels}px",
            )
        image.load()
    except ImageTooLargeError:
        raise
    except Image.DecompressionBombError as exc:
        raise ImageTooLargeError(
            f"decompression bomb: {p!r}: {exc}",
        ) from exc
    except (OSError, SyntaxError, ValueError) as exc:
        raise CorruptImageError(
            f"load failed: {p!r}: {exc}",
            user_message="このファイルは壊れているか、画像として読み込めませんでした。",
        ) from exc

    # 加工に扱いやすいよう RGB / RGBA へ正規化する（元ファイルは一切変更しない）。
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
    return image


def _normalize_output_dir(out_dir: str | os.PathLike[str]) -> Path:
    """出力ディレクトリを絶対パスへ正規化する（`..` トラバーサルを解決）。"""
    return Path(out_dir).expanduser().resolve()


def build_output_path(
    src_path: str | os.PathLike[str],
    out_dir: str | os.PathLike[str],
    fmt: str,
    *,
    suffix: str = "_edited",
) -> Path:
    """非破壊保存の出力パスを決める。

    元ファイル名に `_edited` 接尾辞を付け、拡張子はフォーマットに合わせる。
    既存ファイルと衝突する場合は `_edited(1)`, `_edited(2)` ... と連番を付け、
    決して既存を上書きしない。元画像パスと同一になる場合も連番で回避する。
    """
    src = Path(src_path)
    out_directory = _normalize_output_dir(out_dir)
    ext = ".png" if fmt == "PNG" else ".jpg"
    stem = src.stem

    candidate = out_directory / f"{stem}{suffix}{ext}"
    src_resolved = src.resolve()
    counter = 1
    while candidate.exists() or candidate.resolve() == src_resolved:
        candidate = out_directory / f"{stem}{suffix}({counter}){ext}"
        counter += 1
    return candidate


def save_nondestructive(
    image: Image.Image,
    src_path: str | os.PathLike[str],
    out_dir: str | os.PathLike[str],
    fmt: str,
    *,
    suffix: str = "_edited",
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
) -> Path:
    """加工済み画像を非破壊・アトミックに保存し、出力パスを返す。

    - 出力先と同じディレクトリに一時ファイルを書き、os.replace で最終名へリネーム
      （原子的置換）。途中失敗で中途半端な出力を残さない。
    - 元画像（src_path）は一切書き換えない。
    - 保存失敗は SaveError に変換する。
    """
    if fmt not in _SUPPORTED_FORMATS:
        raise UnsupportedImageError(
            f"unsupported save format: {fmt!r}",
            user_message="この形式では保存できません（対応形式は PNG / JPEG です）。",
        )

    out_directory = _normalize_output_dir(out_dir)
    try:
        out_directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SaveError(f"cannot create output dir: {out_directory!r}: {exc}") from exc

    dest = build_output_path(src_path, out_directory, fmt, suffix=suffix)

    # JPEG はアルファを持てないため RGB へ落とす（元画像は変更しない）。
    to_save = image
    if fmt == "JPEG" and image.mode not in ("RGB", "L"):
        to_save = image.convert("RGB")

    save_kwargs: dict[str, object] = {}
    if fmt == "JPEG":
        save_kwargs["quality"] = jpeg_quality

    tmp_fd, tmp_name = tempfile.mkstemp(
        prefix=".screenshot_editor_", suffix=".tmp", dir=str(out_directory)
    )
    os.close(tmp_fd)
    tmp_path = Path(tmp_name)
    try:
        to_save.save(tmp_path, format=fmt, **save_kwargs)
        os.replace(tmp_path, dest)  # アトミックなリネーム（同一ボリューム内）
    except (OSError, ValueError) as exc:
        # 中途半端な一時ファイルを残さない。
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except OSError:
            pass
        raise SaveError(f"save failed: {dest!r}: {exc}") from exc

    return dest
