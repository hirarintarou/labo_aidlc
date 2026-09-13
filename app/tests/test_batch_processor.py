"""バッチ処理のテスト: 部分失敗スキップ・件数一致・全件失敗の非クラッシュ・進捗通知。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from screenshot_editor.batch import batch_processor
from screenshot_editor.core.edit_settings import EditSettings


def _make_png(path: Path) -> Path:
    Image.new("RGB", (6, 4), (120, 60, 200)).save(path, format="PNG")
    return path


def test_all_success(tmp_path: Path) -> None:
    sources = [_make_png(tmp_path / f"s{i}.png") for i in range(3)]
    out_dir = tmp_path / "out"
    result = batch_processor.process_files(sources, EditSettings(brightness=0.1), out_dir)
    assert result.total == 3
    assert result.succeeded == 3
    assert result.failed == 0
    assert result.succeeded + result.failed == result.total
    for item in result.items:
        assert item.ok and item.output is not None and Path(item.output).exists()


def test_partial_failure_skips_and_continues(tmp_path: Path) -> None:
    good1 = _make_png(tmp_path / "good1.png")
    bad = tmp_path / "bad.png"
    bad.write_bytes(b"")  # 0 バイト -> 失敗
    good2 = _make_png(tmp_path / "good2.png")
    out_dir = tmp_path / "out"

    result = batch_processor.process_files([good1, bad, good2], EditSettings(), out_dir)
    assert result.total == 3
    assert result.succeeded == 2
    assert result.failed == 1
    assert result.succeeded + result.failed == result.total


def test_all_failure_does_not_crash(tmp_path: Path) -> None:
    bad1 = tmp_path / "b1.png"
    bad1.write_bytes(b"")
    bad2 = tmp_path / "b2.txt"
    bad2.write_text("not an image")
    result = batch_processor.process_files([bad1, bad2], EditSettings(), tmp_path / "out")
    assert result.total == 2
    assert result.succeeded == 0
    assert result.failed == 2
    assert "成功 0 件 / 失敗 2 件" in result.summary_ja()


def test_default_out_dir_is_source_dir(tmp_path: Path) -> None:
    src = _make_png(tmp_path / "shot.png")
    result = batch_processor.process_files([src], EditSettings(), out_dir=None)
    assert result.succeeded == 1
    output = Path(result.items[0].output)
    assert output.parent == src.parent  # 既定は元と同じフォルダ


def test_progress_callback_invoked(tmp_path: Path) -> None:
    sources = [_make_png(tmp_path / f"p{i}.png") for i in range(2)]
    calls: list[tuple[int, int, str]] = []

    def on_progress(done: int, total: int, path: str) -> None:
        calls.append((done, total, path))

    batch_processor.process_files(sources, EditSettings(), tmp_path / "out", progress=on_progress)
    assert len(calls) == 2
    assert calls[0][1] == 2  # total
    assert calls[-1][0] == 2  # 最後は 2 件目
