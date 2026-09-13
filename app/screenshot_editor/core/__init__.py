"""core 層: 画像変換の中核ロジック（GUI 非依存の純粋モジュール）。

EditSettings（加工設定）、processor（決定的な変換）、presets（プリセット）を含む。
この層は PySide6 を一切 import しない。Pillow 型はこの層と io の内側に閉じ込める。
"""
