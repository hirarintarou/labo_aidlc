"""メインウィンドウ（ui 層）。左メニュー＋中央プレビュー＋右調整（FR8.2）。

プレビューは表示解像度に合わせた縮小画像へ加工を適用し、原寸への適用は保存時のみ
（performance-design.md PERF-1/2/3）。core/io を呼ぶが、core は GUI を import しない。
Pillow の Image は ui へ QImage 変換の直前まで io/core 内で扱う。
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from screenshot_editor.core import processor
from screenshot_editor.core.edit_settings import Credit, EditSettings
from screenshot_editor.errors import ImageEditorError
from screenshot_editor.io import image_io
from screenshot_editor.ui.batch_dialog import BatchDialog
from screenshot_editor.ui.panels import AdjustmentPanel, PresetPanel

#: プレビュー用の最大表示寸法（PERF: 縮小版に加工を適用）
_PREVIEW_MAX = 900


def pil_to_qpixmap(image: Image.Image) -> QPixmap:
    """Pillow Image を QPixmap へ変換する（ui 層の境界でのみ行う）。"""
    rgba = image.convert("RGBA")
    data = rgba.tobytes("raw", "RGBA")
    qimage = QImage(data, rgba.width, rgba.height, QImage.Format.Format_RGBA8888)
    return QPixmap.fromImage(qimage.copy())


class MainWindow(QMainWindow):
    """アプリのメイン画面。"""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("main-window")
        self.setWindowTitle("FF14 スクリーンショット加工ツール")
        self.resize(1200, 800)

        self._src_path: Path | None = None
        self._original: Image.Image | None = None  # 原寸（保存時に使う）
        self._preview_base: Image.Image | None = None  # 縮小プレビュー元

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)

        # 左: メニュー
        self._menu = QListWidget()
        self._menu.setObjectName("category-menu")
        self._menu.addItems(["調整", "フィルタ／プリセット", "クレジット"])
        self._menu.setMaximumWidth(220)
        self._menu.setMinimumHeight(200)
        root.addWidget(self._menu)

        # 中央: プレビュー＋操作ボタン
        center = QVBoxLayout()
        self._preview = QLabel("画像を開いてください（PNG / JPEG）")
        self._preview.setObjectName("preview-label")
        self._preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview.setMinimumSize(640, 480)
        center.addWidget(self._preview, stretch=1)

        buttons = QHBoxLayout()
        self._open_btn = self._make_button("開く", "open-button", self._open_image)
        self._save_btn = self._make_button("この1枚を保存", "save-button", self._save_image)
        self._reset_btn = self._make_button("リセット", "reset-button", self._reset)
        self._batch_btn = self._make_button("バッチ適用", "batch-button", self._open_batch)
        for b in (self._open_btn, self._save_btn, self._reset_btn, self._batch_btn):
            buttons.addWidget(b)
        center.addLayout(buttons)
        root.addLayout(center, stretch=1)

        # 右: 調整パネル群
        right = QVBoxLayout()
        self._adjust = AdjustmentPanel()
        self._preset = PresetPanel()
        self._adjust.changed.connect(self._update_preview)
        self._preset.changed.connect(self._update_preview)
        right.addWidget(self._adjust)
        right.addWidget(self._preset)
        right.addStretch(1)
        right_widget = QWidget()
        right_widget.setObjectName("right-panel")
        right_widget.setLayout(right)
        right_widget.setMaximumWidth(320)
        root.addWidget(right_widget)

        self._set_editing_enabled(False)

    def _make_button(self, text: str, object_name: str, handler) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName(object_name)
        btn.setMinimumHeight(40)
        btn.clicked.connect(handler)
        return btn

    def _set_editing_enabled(self, enabled: bool) -> None:
        for w in (self._save_btn, self._reset_btn, self._batch_btn, self._adjust, self._preset):
            w.setEnabled(enabled)

    def _current_settings(self) -> EditSettings:
        v = self._adjust.values()
        return EditSettings(
            brightness=v["brightness"],
            contrast=v["contrast"],
            saturation=v["saturation"],
            sharpen=v["sharpen"],
            blur=v["blur"],
            denoise=v["denoise"],
            preset_name=self._preset.selected_preset(),
            credit=Credit(),  # mvp: クレジットは既定（未付与）。編集UIは将来拡張。
        )

    def _open_image(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "画像を開く", "", "画像 (*.png *.jpg *.jpeg)")
        if not path:
            return
        try:
            image = image_io.load_image(path)
        except ImageEditorError as exc:
            QMessageBox.warning(self, "読み込みエラー", exc.user_message)
            return

        self._src_path = Path(path)
        self._original = image
        # プレビュー用の縮小版（原寸は保存時のみ使用）
        preview = image.copy()
        preview.thumbnail((_PREVIEW_MAX, _PREVIEW_MAX), Image.LANCZOS)
        self._preview_base = preview
        self._set_editing_enabled(True)
        self._update_preview()

    def _update_preview(self) -> None:
        if self._preview_base is None:
            return
        edited = processor.apply(self._preview_base, self._current_settings())
        self._preview.setPixmap(
            pil_to_qpixmap(edited).scaled(
                self._preview.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def _save_image(self) -> None:
        if self._original is None or self._src_path is None:
            return
        try:
            fmt = image_io.detect_format(self._src_path)
            # 保存は原寸へ適用（PERF-3）
            edited = processor.apply(self._original, self._current_settings())
            out = image_io.save_nondestructive(edited, self._src_path, self._src_path.parent, fmt)
        except ImageEditorError as exc:
            QMessageBox.warning(self, "保存エラー", exc.user_message)
            return
        QMessageBox.information(self, "保存しました", f"保存先: {out}")

    def _reset(self) -> None:
        self._adjust.reset()
        self._preset.reset()

    def _open_batch(self) -> None:
        dialog = BatchDialog(self._current_settings(), self)
        dialog.exec()
