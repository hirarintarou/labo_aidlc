"""バッチ処理（batch 層）。US2.1 / FR9 に対応。

1 枚で決めた EditSettings を複数ファイルへ一括適用する。各対象は
読込 -> core 適用 -> 非破壊保存。失敗はスキップして継続し、完了時に
「成功 n 件 / 失敗 m 件（n + m = 総数）」を集計する。全件失敗でもクラッシュしない。
"""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from screenshot_editor.core import processor
from screenshot_editor.core.edit_settings import EditSettings
from screenshot_editor.errors import ImageEditorError
from screenshot_editor.io import image_io

#: 進捗コールバック: (処理済み件数, 総数, 直近の対象パス) を受け取る
ProgressCallback = Callable[[int, int, str], None]


@dataclass(frozen=True)
class BatchItemResult:
    """1 ファイルの処理結果。"""

    source: str
    ok: bool
    output: str | None = None
    error_message: str | None = None


@dataclass
class BatchResult:
    """バッチ全体の集計結果。succeeded + failed == total を常に満たす。"""

    total: int = 0
    items: list[BatchItemResult] = field(default_factory=list)

    @property
    def succeeded(self) -> int:
        return sum(1 for i in self.items if i.ok)

    @property
    def failed(self) -> int:
        return sum(1 for i in self.items if not i.ok)

    def summary_ja(self) -> str:
        """日本語の完了サマリ（AC2.1.2 準拠）。"""
        return f"成功 {self.succeeded} 件 / 失敗 {self.failed} 件（合計 {self.total} 件）"


def process_files(
    sources: Sequence[str | os.PathLike[str]],
    settings: EditSettings,
    out_dir: str | os.PathLike[str] | None = None,
    *,
    progress: ProgressCallback | None = None,
    max_pixels: int = image_io.DEFAULT_MAX_IMAGE_PIXELS,
) -> BatchResult:
    """複数ファイルへ settings を一括適用し、非破壊保存する。

    out_dir が None の場合、各画像は元画像と同じフォルダに保存する（既定）。
    1 枚の失敗では停止せず、その 1 件を失敗として記録して次へ進む。
    """
    result = BatchResult(total=len(sources))

    for index, src in enumerate(sources, start=1):
        src_path = Path(src)
        if progress is not None:
            progress(index, result.total, str(src_path))

        try:
            fmt = image_io.detect_format(src_path)
            image = image_io.load_image(src_path, max_pixels=max_pixels)
            try:
                edited = processor.apply(image, settings)
            finally:
                image.close()
            target_dir = Path(out_dir) if out_dir is not None else src_path.parent
            output = image_io.save_nondestructive(edited, src_path, target_dir, fmt)
            result.items.append(BatchItemResult(source=str(src_path), ok=True, output=str(output)))
        except ImageEditorError as exc:
            # 想定内のドメインエラー: スキップして継続。
            result.items.append(
                BatchItemResult(source=str(src_path), ok=False, error_message=exc.user_message)
            )
        except OSError as exc:
            # ディスク/権限などの想定外 I/O エラーもクラッシュさせずスキップ。
            result.items.append(
                BatchItemResult(
                    source=str(src_path),
                    ok=False,
                    error_message=f"処理できませんでした: {exc}",
                )
            )

    return result
