"""エントリポイント。`python -m screenshot_editor` で GUI を起動する（US0.1）。

GUI 依存（PySide6）はこのモジュールと ui 層に閉じ込める。core/io はここに依存しない。
"""

from __future__ import annotations

import sys


def main() -> int:
    """アプリを起動する。GUI の初期化はここで行う。"""
    # PySide6 の import は関数内に置き、テスト収集時に GUI 依存を強制しない。
    from PySide6.QtWidgets import QApplication

    from screenshot_editor.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
