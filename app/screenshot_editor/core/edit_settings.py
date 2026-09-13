"""EditSettings — 加工設定の論理シェイプ（core 所有・単体編集/バッチで共有）。

functional-spec.md §3 に対応。各既定値は「恒等（無変化）」であり、既定の
EditSettings を適用しても入力画像と一致する（決定的）。
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum


class CreditPosition(str, Enum):
    """クレジットの配置位置。"""

    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    CENTER = "center"


@dataclass(frozen=True)
class Crop:
    """トリミング矩形（左上 x, y と 幅, 高さ。ピクセル単位）。"""

    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Resize:
    """リサイズ設定。既定でアスペクト比を保持する（keep_aspect=True）。"""

    width: int
    height: int
    keep_aspect: bool = True


@dataclass(frozen=True)
class Credit:
    """テキストクレジット設定。text が空文字なら未付与（恒等）。"""

    text: str = ""
    position: CreditPosition = CreditPosition.BOTTOM_RIGHT
    #: フォントサイズ（画像高さに対する相対値ではなく、実ピクセルの目安）
    size: int = 24
    #: 不透明度 0.0（透明）〜1.0（不透明）
    opacity: float = 1.0

    @property
    def is_empty(self) -> bool:
        return self.text.strip() == ""


@dataclass(frozen=True)
class EditSettings:
    """加工設定。すべての既定値は恒等（適用しても無変化）。

    - brightness / contrast / saturation: 中立値 0.0 の相対調整（-1.0〜1.0 目安、0=無変化）
    - sharpen / blur / denoise: 強度 0.0=無変化（0.0〜1.0 目安）
    - preset_name: 適用プリセット名（None=未適用）
    - crop: トリミング矩形（None=未適用）
    - resize: リサイズ（None=未適用）
    - credit: クレジット（text 空=未付与）
    """

    brightness: float = 0.0
    contrast: float = 0.0
    saturation: float = 0.0
    sharpen: float = 0.0
    blur: float = 0.0
    denoise: float = 0.0
    preset_name: str | None = None
    crop: Crop | None = None
    resize: Resize | None = None
    credit: Credit = field(default_factory=Credit)

    @property
    def is_identity(self) -> bool:
        """既定（恒等）のままで、適用しても画像が変化しないなら True。"""
        return (
            self.brightness == 0.0
            and self.contrast == 0.0
            and self.saturation == 0.0
            and self.sharpen == 0.0
            and self.blur == 0.0
            and self.denoise == 0.0
            and self.preset_name is None
            and self.crop is None
            and self.resize is None
            and self.credit.is_empty
        )

    def copy_with(self, **changes: object) -> EditSettings:
        """一部の属性だけ差し替えた新しい EditSettings を返す（不変オブジェクト）。"""
        return replace(self, **changes)
