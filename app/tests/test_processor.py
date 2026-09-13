"""processor のテスト: 恒等一致・決定性・寸法（境界含む）・クレジット合成・合成順序。"""

from __future__ import annotations

from PIL import Image

from screenshot_editor.core import processor
from screenshot_editor.core.edit_settings import (
    Credit,
    CreditPosition,
    Crop,
    EditSettings,
    Resize,
)


def test_identity_settings_produce_equal_image(rgb_image: Image.Image) -> None:
    out = processor.apply(rgb_image, EditSettings())
    assert list(out.getdata()) == list(rgb_image.getdata())
    assert out.size == rgb_image.size


def test_apply_is_deterministic(rgb_image: Image.Image) -> None:
    settings = EditSettings(brightness=0.2, contrast=0.1, saturation=0.3)
    out1 = processor.apply(rgb_image, settings)
    out2 = processor.apply(rgb_image, settings)
    assert list(out1.getdata()) == list(out2.getdata())


def test_apply_does_not_mutate_input(rgb_image: Image.Image) -> None:
    before = list(rgb_image.getdata())
    processor.apply(rgb_image, EditSettings(brightness=0.5))
    assert list(rgb_image.getdata()) == before  # 入力は不変


def test_brightness_increases_luminance(rgb_image: Image.Image) -> None:
    brighter = processor.apply(rgb_image, EditSettings(brightness=0.5))
    base_sum = sum(sum(px) for px in rgb_image.getdata())
    bright_sum = sum(sum(px) for px in brighter.getdata())
    assert bright_sum > base_sum


def test_crop_dimensions(rgb_image: Image.Image) -> None:
    out = processor.apply(rgb_image, EditSettings(crop=Crop(x=1, y=1, width=4, height=3)))
    assert out.size == (4, 3)


def test_crop_clamped_to_bounds(rgb_image: Image.Image) -> None:
    # 画像 (8x6) を超える矩形は境界にクランプされる。
    out = processor.apply(rgb_image, EditSettings(crop=Crop(x=0, y=0, width=100, height=100)))
    assert out.size == (8, 6)


def test_resize_keep_aspect(rgb_image: Image.Image) -> None:
    # 8x6 を 4x4 の枠にアスペクト比保持で収める -> 4x3。
    settings = EditSettings(resize=Resize(width=4, height=4, keep_aspect=True))
    out = processor.apply(rgb_image, settings)
    assert out.size == (4, 3)


def test_resize_no_keep_aspect(rgb_image: Image.Image) -> None:
    out = processor.apply(
        rgb_image, EditSettings(resize=Resize(width=4, height=4, keep_aspect=False))
    )
    assert out.size == (4, 4)


def test_resize_one_pixel_boundary(rgb_image: Image.Image) -> None:
    out = processor.apply(
        rgb_image, EditSettings(resize=Resize(width=1, height=1, keep_aspect=False))
    )
    assert out.size == (1, 1)


def test_credit_changes_image(rgb_image: Image.Image) -> None:
    out = processor.apply(
        rgb_image,
        EditSettings(credit=Credit(text="© SQUARE ENIX", position=CreditPosition.BOTTOM_RIGHT)),
    )
    assert out.size == rgb_image.size
    assert list(out.getdata()) != list(rgb_image.getdata())


def test_empty_credit_no_change(rgb_image: Image.Image) -> None:
    out = processor.apply(rgb_image, EditSettings(credit=Credit(text="")))
    assert list(out.getdata()) == list(rgb_image.getdata())


def test_fixed_order_credit_after_resize(rgb_image: Image.Image) -> None:
    # 合成順序が固定（リサイズ -> クレジット）なので、リサイズ後の寸法で出力される。
    settings = EditSettings(
        resize=Resize(width=4, height=3, keep_aspect=False),
        credit=Credit(text="test"),
    )
    out = processor.apply(rgb_image, settings)
    assert out.size == (4, 3)


def test_rgba_image_preserved(rgba_image: Image.Image) -> None:
    out = processor.apply(rgba_image, EditSettings(brightness=0.1))
    assert out.mode == "RGBA"
    assert out.size == rgba_image.size
