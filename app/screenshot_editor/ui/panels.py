"""右パネルの調整ウィジェット群（ui 層）。

各パネルはスライダー等で EditSettings の値を編集し、変更をシグナルで通知する。
大きめの文字・ボタンで見やすく（NFR4）。主要要素に objectName（data-testid 相当）を付与。
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from screenshot_editor.core import presets


def _make_slider(object_name: str) -> QSlider:
    """-100..100 の水平スライダー（0 が中立=恒等）を作る。"""
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setObjectName(object_name)
    slider.setMinimum(-100)
    slider.setMaximum(100)
    slider.setValue(0)
    slider.setMinimumHeight(28)
    return slider


class AdjustmentPanel(QWidget):
    """明るさ/コントラスト/彩度/シャープ/ぼかし/ノイズ除去を編集するパネル。"""

    #: いずれかの値が変わったら発火（引数は無し。呼び出し側が values() を読む）
    changed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("adjustment-panel")
        layout = QFormLayout(self)

        title = QLabel("調整")
        title.setObjectName("adjustment-title")
        font = title.font()
        font.setPointSize(font.pointSize() + 2)
        title.setFont(font)
        layout.addRow(title)

        self._sliders: dict[str, QSlider] = {}
        for key, label in (
            ("brightness", "明るさ"),
            ("contrast", "コントラスト"),
            ("saturation", "彩度"),
            ("sharpen", "シャープ"),
            ("blur", "ぼかし"),
            ("denoise", "ノイズ除去"),
        ):
            slider = _make_slider(f"slider-{key}")
            # QSlider.valueChanged は int を伴って発火する。引数なしの
            # `changed = Signal()` へ直結すると PySide6 が余分な位置引数を
            # emit へ渡してシグネチャ不一致エラーになる。引数を捨てるスロットで
            # 包み、changed を引数なしで発火させる。
            slider.valueChanged.connect(lambda *_: self.changed.emit())
            self._sliders[key] = slider
            layout.addRow(QLabel(label), slider)

    def values(self) -> dict[str, float]:
        """各調整値を -1.0..1.0 の float で返す。"""
        return {key: s.value() / 100.0 for key, s in self._sliders.items()}

    def reset(self) -> None:
        for slider in self._sliders.values():
            slider.blockSignals(True)
            slider.setValue(0)
            slider.blockSignals(False)
        self.changed.emit()


class PresetPanel(QWidget):
    """プリセット選択パネル。"""

    changed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("preset-panel")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("フィルタ／プリセット"))

        self._combo = QComboBox()
        self._combo.setObjectName("preset-combo")
        self._combo.addItem("（なし）", userData=None)
        for name in presets.preset_names():
            self._combo.addItem(name, userData=name)
        # QComboBox.currentIndexChanged は int を伴って発火する。引数なしの
        # `changed = Signal()` へ直結するとシグネチャ不一致エラーになるため、
        # 引数を捨てるスロットで包んで changed を引数なしで発火させる。
        self._combo.currentIndexChanged.connect(lambda *_: self.changed.emit())
        layout.addWidget(self._combo)
        layout.addStretch(1)

    def selected_preset(self) -> str | None:
        return self._combo.currentData()

    def reset(self) -> None:
        self._combo.blockSignals(True)
        self._combo.setCurrentIndex(0)
        self._combo.blockSignals(False)
        self.changed.emit()
