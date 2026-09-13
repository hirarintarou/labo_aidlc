"""バッチ適用ダイアログ（ui 層）。

複数ファイル/フォルダに同じ EditSettings を一括適用する。処理はワーカースレッドで
実行し UI をブロックしない（performance-design.md）。進捗・件数を表示し、Esc で閉じる。
"""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from screenshot_editor.batch import batch_processor
from screenshot_editor.core.edit_settings import EditSettings


class _BatchWorker(QObject):
    """バッチ処理をワーカースレッドで実行する。UI へは Qt シグナルで通知する。"""

    progress = Signal(int, int, str)
    finished = Signal(object)  # BatchResult

    def __init__(self, sources: Sequence[str], settings: EditSettings) -> None:
        super().__init__()
        self._sources = list(sources)
        self._settings = settings

    def run(self) -> None:
        def on_progress(done: int, total: int, path: str) -> None:
            self.progress.emit(done, total, path)

        result = batch_processor.process_files(
            self._sources, self._settings, out_dir=None, progress=on_progress
        )
        self.finished.emit(result)


class BatchDialog(QDialog):
    """バッチ適用ダイアログ。settings を渡して開く。"""

    def __init__(self, settings: EditSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("batch-dialog")
        self.setWindowTitle("バッチ適用")
        self._settings = settings
        self._thread: QThread | None = None
        self._worker: _BatchWorker | None = None

        layout = QVBoxLayout(self)
        self._info = QLabel("処理する画像ファイルを選択してください（PNG / JPEG）。")
        self._info.setObjectName("batch-info")
        layout.addWidget(self._info)

        self._select_btn = QPushButton("ファイルを選択して開始")
        self._select_btn.setObjectName("batch-select-button")
        self._select_btn.setMinimumHeight(36)
        self._select_btn.clicked.connect(self._choose_and_run)
        layout.addWidget(self._select_btn)

        self._progress = QProgressBar()
        self._progress.setObjectName("batch-progress")
        self._progress.setValue(0)
        layout.addWidget(self._progress)

        self._status = QLabel("")
        self._status.setObjectName("batch-status")
        layout.addWidget(self._status)

    def keyPressEvent(self, event) -> None:  # noqa: N802 (Qt シグネチャ)
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)

    def _choose_and_run(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, "画像を選択", "", "画像 (*.png *.jpg *.jpeg)")
        if not files:
            return
        self._select_btn.setEnabled(False)
        self._progress.setMaximum(len(files))
        self._progress.setValue(0)

        self._thread = QThread(self)
        self._worker = _BatchWorker(files, self._settings)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._thread.start()

    def _on_progress(self, done: int, total: int, path: str) -> None:
        self._progress.setValue(done)
        self._status.setText(f"{total} 枚中 {done} 枚処理中…")

    def _on_finished(self, result: batch_processor.BatchResult) -> None:
        self._status.setText(result.summary_ja())
        self._select_btn.setEnabled(True)
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
            self._thread = None
        self._worker = None
