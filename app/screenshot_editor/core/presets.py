"""組み込みプリセット（core 層）。US1.4 / FR4 に対応。

各プリセットは EditSettings ベースの色調・画質パラメータの集合。適用は決定的で、
同じ入力・同じプリセットなら必ず同じ出力になる。mvp では代表 8 種を用意する。
"""

from __future__ import annotations

from dataclasses import dataclass

from screenshot_editor.core.edit_settings import EditSettings


@dataclass(frozen=True)
class PresetDefinition:
    """プリセット定義。name（表示名）と、適用する色調/画質パラメータ。"""

    name: str
    brightness: float = 0.0
    contrast: float = 0.0
    saturation: float = 0.0
    sharpen: float = 0.0
    blur: float = 0.0
    denoise: float = 0.0

    def merge_into(self, settings: EditSettings) -> EditSettings:
        """プリセットの効果を EditSettings に反映する。

        ユーザーが明示的に非ゼロへ設定した補正/画質はユーザー値を優先し、
        0（未調整）の項目のみプリセット値で埋める。crop/resize/credit は保持する。
        """

        def pick(user_value: float, preset_value: float) -> float:
            return user_value if user_value != 0.0 else preset_value

        return settings.copy_with(
            brightness=pick(settings.brightness, self.brightness),
            contrast=pick(settings.contrast, self.contrast),
            saturation=pick(settings.saturation, self.saturation),
            sharpen=pick(settings.sharpen, self.sharpen),
            blur=pick(settings.blur, self.blur),
            denoise=pick(settings.denoise, self.denoise),
        )


#: 組み込みプリセット（代表 8 種）。表示順を保つため tuple で保持。
BUILTIN_PRESETS: tuple[PresetDefinition, ...] = (
    PresetDefinition("ナチュラル", brightness=0.05, contrast=0.05, saturation=0.05),
    PresetDefinition("ビビッド", contrast=0.15, saturation=0.35, sharpen=0.2),
    PresetDefinition("シネマティック", brightness=-0.05, contrast=0.25, saturation=-0.1),
    PresetDefinition("モノクロ", saturation=-1.0, contrast=0.1),
    PresetDefinition("セピア", saturation=-0.6, brightness=0.05, contrast=0.05),
    PresetDefinition("ソフト", blur=0.15, brightness=0.05, saturation=0.05),
    PresetDefinition("シャープネス", sharpen=0.5, contrast=0.1),
    PresetDefinition("クール", brightness=0.03, saturation=-0.15, contrast=0.1),
)

#: name -> PresetDefinition の索引
_PRESET_INDEX: dict[str, PresetDefinition] = {p.name: p for p in BUILTIN_PRESETS}


def list_presets() -> tuple[PresetDefinition, ...]:
    """組み込みプリセットの一覧（定義順）を返す。"""
    return BUILTIN_PRESETS


def preset_names() -> list[str]:
    """組み込みプリセット名の一覧を返す。"""
    return [p.name for p in BUILTIN_PRESETS]


def get_preset(name: str) -> PresetDefinition | None:
    """名前でプリセットを取得する。無ければ None。"""
    return _PRESET_INDEX.get(name)
