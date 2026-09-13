"""EditSettings のテスト: 既定値=恒等、複製の不変性。"""

from __future__ import annotations

from screenshot_editor.core.edit_settings import Credit, CreditPosition, EditSettings


def test_default_settings_is_identity() -> None:
    assert EditSettings().is_identity is True


def test_nonzero_adjustment_is_not_identity() -> None:
    assert EditSettings(brightness=0.2).is_identity is False


def test_credit_with_text_is_not_identity() -> None:
    s = EditSettings(credit=Credit(text="© SQUARE ENIX"))
    assert s.is_identity is False


def test_empty_credit_is_identity() -> None:
    assert EditSettings(credit=Credit(text="   ")).is_identity is True


def test_copy_with_is_immutable() -> None:
    original = EditSettings()
    changed = original.copy_with(contrast=0.3)
    assert original.contrast == 0.0  # 元は不変
    assert changed.contrast == 0.3
    assert changed is not original


def test_credit_default_position_is_bottom_right() -> None:
    assert Credit().position is CreditPosition.BOTTOM_RIGHT
    assert Credit().is_empty is True
