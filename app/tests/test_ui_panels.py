"""UI パネルのシグナル配線の回帰テスト（ui 層）。

intent `preview-changed-error` の回帰防止:
`AdjustmentPanel` / `PresetPanel` の `changed = Signal()` は引数なしで宣言されて
いる。スライダー（`QSlider.valueChanged`, int を伴う）やコンボ選択
（`QComboBox.currentIndexChanged`, int を伴う）を `self.changed.emit` へ直結すると、
PySide6 が余分な位置引数を emit へ渡してコンソールにシグネチャ不一致エラーが出る。
本テストは「`changed` が購読スロットへ位置引数 0 個で通知される」ことを検証し、
退行（余分な引数の伝播）を機械的に検知する。

GUI 依存のため、ヘッドレス（QT_QPA_PLATFORM=offscreen）で QApplication を単一生成
して実行する。実行コマンド（app/ ディレクトリ）:
    QT_QPA_PLATFORM=offscreen python -m pytest tests/test_ui_panels.py -q
"""

from __future__ import annotations

import os

import pytest

# ディスプレイのない環境でも Qt ウィジェットを生成できるようにする。
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication  # noqa: E402

from screenshot_editor.ui.panels import AdjustmentPanel, PresetPanel  # noqa: E402


@pytest.fixture(scope="session")
def qapp() -> QApplication:
    """プロセスで単一の QApplication を用意する（二重生成を避ける）。"""
    return QApplication.instance() or QApplication([])


def _zero_arg_recorder() -> tuple[list[int], object]:
    """位置引数 0 個でのみ成功するスロットと呼び出し記録を返す。

    余分な位置引数が渡ると TypeError になり、退行を検知できる。
    """
    calls: list[int] = []

    def slot() -> None:  # 引数なし: changed が余分な引数付きで発火すると TypeError
        calls.append(1)

    return calls, slot


def test_adjustment_slider_emits_changed_without_extra_args(qapp: QApplication) -> None:
    """スライダー操作で changed が引数なしで発火する（FR1.1 / FR2.1 / FR3.1）。"""
    panel = AdjustmentPanel()
    calls, slot = _zero_arg_recorder()
    panel.changed.connect(slot)

    # 少なくとも 1 つのスライダーを操作して valueChanged(int) を発火させる。
    slider = next(iter(panel._sliders.values()))
    slider.setValue(50)  # 余分な引数が伝播すれば slot 呼び出しで TypeError

    assert calls, "スライダー操作で changed が発火しなかった"


def test_preset_combo_emits_changed_without_extra_args(qapp: QApplication) -> None:
    """プリセット選択で changed が引数なしで発火する（FR1.2 / FR2.2 / FR3.1）。"""
    panel = PresetPanel()
    calls, slot = _zero_arg_recorder()
    panel.changed.connect(slot)

    # コンボの選択を変えて currentIndexChanged(int) を発火させる。
    panel._combo.setCurrentIndex(1)

    assert calls, "プリセット選択で changed が発火しなかった"


def test_adjustment_reset_emits_changed_without_extra_args(qapp: QApplication) -> None:
    """reset() 経由でも changed が引数なしで発火する（FR1.3 / FR2.3）。"""
    panel = AdjustmentPanel()
    # 一度値を変えてから reset。reset 内の setValue は blockSignals で抑制され、
    # 最後に self.changed.emit() が引数なしで 1 回呼ばれる。
    next(iter(panel._sliders.values())).setValue(30)

    calls, slot = _zero_arg_recorder()
    panel.changed.connect(slot)
    panel.reset()

    assert calls, "reset() で changed が発火しなかった"


def test_preset_reset_emits_changed_without_extra_args(qapp: QApplication) -> None:
    """PresetPanel.reset() でも changed が引数なしで発火する（FR1.3 / FR2.3）。"""
    panel = PresetPanel()
    panel._combo.setCurrentIndex(1)

    calls, slot = _zero_arg_recorder()
    panel.changed.connect(slot)
    panel.reset()

    assert calls, "PresetPanel.reset() で changed が発火しなかった"


def test_repeated_operations_do_not_raise(qapp: QApplication) -> None:
    """調整・プリセット操作を反復してもエラーなく安定して発火する（NFR3）。"""
    adjust = AdjustmentPanel()
    preset = PresetPanel()
    calls, slot = _zero_arg_recorder()
    adjust.changed.connect(slot)
    preset.changed.connect(slot)

    sliders = list(adjust._sliders.values())
    for value in (10, -10, 0, 100, -100):
        for slider in sliders:
            slider.setValue(value)
    for index in (1, 0, 1):
        preset._combo.setCurrentIndex(index)

    assert len(calls) > 0
