"""型付きドメインエラー（core/io が送出し、ui が日本語メッセージへ変換する）。

security-design.md のエラー階層に対応する。利用者に届くメッセージは技術例外そのもの
ではなく、UI 層で日本語の分かりやすい文言に変換する。
"""

from __future__ import annotations


class ImageEditorError(Exception):
    """本ツールのドメインエラーの基底。

    ``user_message`` に利用者向けの日本語メッセージを持つ。UI 層はこれを表示する。
    """

    #: 既定の利用者向けメッセージ（サブクラスで上書きする）
    default_user_message = "画像処理でエラーが発生しました。"

    def __init__(self, message: str | None = None, *, user_message: str | None = None) -> None:
        super().__init__(message or self.default_user_message)
        self.user_message = user_message or self.default_user_message


class UnsupportedImageError(ImageEditorError):
    """非対応フォーマットの画像を開こうとした。"""

    default_user_message = "このファイルは開けませんでした（対応形式は PNG / JPEG です）。"


class CorruptImageError(ImageEditorError):
    """破損・デコード失敗（0 バイトを含む）。"""

    default_user_message = "このファイルは壊れているか、画像として読み込めませんでした。"


class ImageTooLargeError(ImageEditorError):
    """デコード爆弾防止の上限（MAX_IMAGE_PIXELS）を超過した。"""

    default_user_message = "この画像はサイズが大きすぎるため読み込めませんでした。"


class SaveError(ImageEditorError):
    """書き込み失敗（ディスク・権限・パス不正など）。"""

    default_user_message = (
        "画像を保存できませんでした（保存先の空き容量や書き込み権限をご確認ください）。"
    )
