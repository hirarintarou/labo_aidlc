"""テスト用の合成フィクスチャ画像をプログラム生成する（バイナリ肥大回避）。

数 px の PNG / JPEG（アルファ有無）を tmp_path 上に作る。ファイル I/O は
pytest の tmp_path を使い、実ファイルで非破壊・アトミック保存を検証する。
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image


def _make_rgb(width: int = 8, height: int = 6) -> Image.Image:
    """決定的なパターンの RGB 画像を作る。"""
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            pixels[x, y] = ((x * 32) % 256, (y * 40) % 256, ((x + y) * 16) % 256)
    return image


def _make_rgba(width: int = 8, height: int = 6) -> Image.Image:
    image = _make_rgb(width, height).convert("RGBA")
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            r, g, b, _ = pixels[x, y]
            pixels[x, y] = (r, g, b, (x * 30) % 256)
    return image


@pytest.fixture
def rgb_image() -> Image.Image:
    return _make_rgb()


@pytest.fixture
def rgba_image() -> Image.Image:
    return _make_rgba()


@pytest.fixture
def png_file(tmp_path: Path) -> Path:
    """小さな PNG フィクスチャを作って返す。"""
    path = tmp_path / "shot001.png"
    _make_rgb().save(path, format="PNG")
    return path


@pytest.fixture
def png_rgba_file(tmp_path: Path) -> Path:
    path = tmp_path / "shot_alpha.png"
    _make_rgba().save(path, format="PNG")
    return path


@pytest.fixture
def jpeg_file(tmp_path: Path) -> Path:
    """小さな JPEG フィクスチャを作って返す。"""
    path = tmp_path / "shot002.jpg"
    _make_rgb().save(path, format="JPEG", quality=95)
    return path
