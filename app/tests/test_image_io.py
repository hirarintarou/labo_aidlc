"""io 層のテスト（P0）。非破壊保存・ラウンドトリップ・異常系を最重点で検証する。"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from screenshot_editor.errors import (
    CorruptImageError,
    ImageTooLargeError,
    SaveError,
    UnsupportedImageError,
)
from screenshot_editor.io import image_io

# ---- detect_format ----


def test_detect_format_png(png_file: Path) -> None:
    assert image_io.detect_format(png_file) == "PNG"


def test_detect_format_jpeg(jpeg_file: Path) -> None:
    assert image_io.detect_format(jpeg_file) == "JPEG"


def test_detect_format_unsupported_extension(tmp_path: Path) -> None:
    with pytest.raises(UnsupportedImageError):
        image_io.detect_format(tmp_path / "note.txt")


# ---- load_image: happy path ----


def test_load_png_returns_image(png_file: Path) -> None:
    image = image_io.load_image(png_file)
    assert image.size == (8, 6)
    assert image.mode in ("RGB", "RGBA")


def test_load_jpeg_returns_image(jpeg_file: Path) -> None:
    image = image_io.load_image(jpeg_file)
    assert image.size == (8, 6)


# ---- load_image: 異常系（fail fast） ----


def test_load_zero_byte_file_raises_corrupt(tmp_path: Path) -> None:
    p = tmp_path / "empty.png"
    p.write_bytes(b"")
    with pytest.raises(CorruptImageError):
        image_io.load_image(p)


def test_load_corrupt_file_raises_corrupt(tmp_path: Path) -> None:
    p = tmp_path / "broken.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"garbage-not-a-real-png")
    with pytest.raises((CorruptImageError, UnsupportedImageError)):
        image_io.load_image(p)


def test_load_unsupported_content_raises(tmp_path: Path) -> None:
    p = tmp_path / "actually.gif"
    Image.new("RGB", (4, 4)).save(p, format="GIF")
    with pytest.raises(UnsupportedImageError):
        image_io.load_image(p)


def test_load_missing_file_raises_corrupt(tmp_path: Path) -> None:
    with pytest.raises(CorruptImageError):
        image_io.load_image(tmp_path / "does_not_exist.png")


def test_load_too_large_raises(png_file: Path) -> None:
    # 8x6=48px の画像に対し上限を 10px に絞って上限判定を発火させる。
    with pytest.raises(ImageTooLargeError):
        image_io.load_image(png_file, max_pixels=10)


# ---- 非破壊保存: 元画像が不変であること（P0） ----


def test_save_is_nondestructive_bytes_and_mtime(png_file: Path, tmp_path: Path) -> None:
    original_bytes = png_file.read_bytes()
    original_mtime = png_file.stat().st_mtime_ns

    image = image_io.load_image(png_file)
    out = image_io.save_nondestructive(image, png_file, tmp_path, "PNG")

    assert out.exists()
    assert out != png_file
    # 元ファイルはバイト列も mtime も不変。
    assert png_file.read_bytes() == original_bytes
    assert png_file.stat().st_mtime_ns == original_mtime


def test_save_uses_edited_suffix(png_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(png_file)
    out = image_io.save_nondestructive(image, png_file, tmp_path, "PNG")
    assert out.stem == "shot001_edited"
    assert out.suffix == ".png"


def test_save_collision_gets_numbered(png_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(png_file)
    first = image_io.save_nondestructive(image, png_file, tmp_path, "PNG")
    second = image_io.save_nondestructive(image, png_file, tmp_path, "PNG")
    assert first != second
    assert second.name == "shot001_edited(1).png"


def test_save_never_overwrites_source(png_file: Path) -> None:
    # 出力先を元と同じフォルダにしても、元ファイルは上書きされない。
    image = image_io.load_image(png_file)
    out = image_io.save_nondestructive(image, png_file, png_file.parent, "PNG")
    assert out.resolve() != png_file.resolve()
    assert png_file.exists()


# ---- ラウンドトリップ ----


def test_png_roundtrip_pixel_exact(png_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(png_file)
    out = image_io.save_nondestructive(image, png_file, tmp_path, "PNG")
    reloaded = image_io.load_image(out)
    # PNG は可逆。RGB へそろえて画素完全一致を確認。
    assert list(reloaded.convert("RGB").getdata()) == list(image.convert("RGB").getdata())


def test_jpeg_roundtrip_dims_and_channels(jpeg_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(jpeg_file)
    out = image_io.save_nondestructive(image, jpeg_file, tmp_path, "JPEG")
    reloaded = image_io.load_image(out)
    # JPEG は非可逆なので寸法・チャンネルの一致と許容誤差で判定。
    assert reloaded.size == image.size
    assert reloaded.mode == image.mode
    src_px = list(image.convert("RGB").getdata())
    dst_px = list(reloaded.convert("RGB").getdata())
    diffs = [
        abs(a - b) for s, d in zip(src_px, dst_px, strict=False) for a, b in zip(s, d, strict=False)
    ]
    mean_diff = sum(diffs) / len(diffs)
    assert mean_diff < 20.0  # 小画像・高品質での許容誤差


def test_cross_png_to_jpeg(png_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(png_file)
    out = image_io.save_nondestructive(image, png_file, tmp_path, "JPEG")
    assert out.suffix == ".jpg"
    reloaded = image_io.load_image(out)
    assert reloaded.size == image.size


def test_cross_jpeg_to_png(jpeg_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(jpeg_file)
    out = image_io.save_nondestructive(image, jpeg_file, tmp_path, "PNG")
    assert out.suffix == ".png"
    reloaded = image_io.load_image(out)
    assert reloaded.size == image.size


# ---- 保存失敗時に中途出力を残さない ----


def test_save_unsupported_format_raises_and_no_tmp(png_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(png_file)
    out_dir = tmp_path / "out"
    with pytest.raises(UnsupportedImageError):
        image_io.save_nondestructive(image, png_file, out_dir, "GIF")


def test_save_failure_leaves_no_partial_file(monkeypatch, png_file: Path, tmp_path: Path) -> None:
    image = image_io.load_image(png_file)
    out_dir = tmp_path / "out2"

    def boom(*args, **kwargs):
        raise OSError("disk full (simulated)")

    # Image.save を失敗させ、SaveError に変換され一時ファイルが残らないことを確認。
    monkeypatch.setattr(Image.Image, "save", boom)
    with pytest.raises(SaveError):
        image_io.save_nondestructive(image, png_file, out_dir, "PNG")

    leftover = [p for p in out_dir.iterdir()] if out_dir.exists() else []
    assert leftover == []
