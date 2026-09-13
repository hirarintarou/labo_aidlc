"""プリセットのテスト: 6〜10種の存在、決定的な同一出力。"""

from __future__ import annotations

from PIL import Image

from screenshot_editor.core import presets, processor
from screenshot_editor.core.edit_settings import EditSettings


def test_builtin_preset_count_in_range() -> None:
    names = presets.preset_names()
    assert 6 <= len(names) <= 10


def test_preset_names_unique() -> None:
    names = presets.preset_names()
    assert len(names) == len(set(names))


def test_get_preset_known_and_unknown() -> None:
    assert presets.get_preset("ビビッド") is not None
    assert presets.get_preset("存在しない") is None


def test_preset_application_is_deterministic(rgb_image: Image.Image) -> None:
    settings = EditSettings(preset_name="シネマティック")
    out1 = processor.apply(rgb_image, settings)
    out2 = processor.apply(rgb_image, settings)
    assert list(out1.getdata()) == list(out2.getdata())


def test_different_presets_differ(rgb_image: Image.Image) -> None:
    vivid = processor.apply(rgb_image, EditSettings(preset_name="ビビッド"))
    mono = processor.apply(rgb_image, EditSettings(preset_name="モノクロ"))
    assert list(vivid.getdata()) != list(mono.getdata())


def test_user_value_overrides_preset(rgb_image: Image.Image) -> None:
    # ユーザーが brightness を明示指定したらプリセット値ではなくユーザー値が優先。
    preset = presets.get_preset("ナチュラル")
    assert preset is not None
    merged = preset.merge_into(EditSettings(brightness=0.5))
    assert merged.brightness == 0.5
