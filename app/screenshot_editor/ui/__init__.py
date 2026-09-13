"""ui 層: PySide6 による画面。core / io をワーカースレッド経由で呼ぶ。

この層のみ PySide6 に依存する。core は GUI を import しない一方向依存 (ui -> core -> io)。
"""
