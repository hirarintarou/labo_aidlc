"""画像変換の中核（core 層）。決定的な純粋関数群。

functional-spec.md §3.5 / Q3 に対応:
- UI 上は各加工を自由に調整できるが、最終的に画像へ焼き込む合成順序は固定の自然な順序
  （補正 -> 画質 -> フィルタ -> トリミング/リサイズ -> クレジット）とする。
- 同じ設定なら常に同じ出力になる（決定的）。恒等パラメータでは入力と一致する。

この層は GUI（PySide6）に依存しない。Pillow の Image を受け取り Image を返す。
"""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from screenshot_editor.core.edit_settings import (
    Credit,
    CreditPosition,
    Crop,
    EditSettings,
    Resize,
)
from screenshot_editor.core.presets import get_preset


def _apply_brightness(image: Image.Image, amount: float) -> Image.Image:
    """明るさ調整。amount=0 で無変化。範囲目安 -1.0〜1.0。"""
    if amount == 0.0:
        return image
    # ImageEnhance の factor は 1.0 が無変化。amount(-1..1) -> factor(0..2)。
    factor = 1.0 + amount
    return ImageEnhance.Brightness(image).enhance(factor)


def _apply_contrast(image: Image.Image, amount: float) -> Image.Image:
    if amount == 0.0:
        return image
    factor = 1.0 + amount
    return ImageEnhance.Contrast(image).enhance(factor)


def _apply_saturation(image: Image.Image, amount: float) -> Image.Image:
    if amount == 0.0:
        return image
    factor = 1.0 + amount
    return ImageEnhance.Color(image).enhance(factor)


def _apply_sharpen(image: Image.Image, amount: float) -> Image.Image:
    """シャープ化。amount=0 で無変化。UnsharpMask の強度に写像。"""
    if amount == 0.0:
        return image
    percent = int(max(0.0, amount) * 150)  # 0..1 -> 0..150%
    return image.filter(ImageFilter.UnsharpMask(radius=2, percent=percent, threshold=3))


def _apply_blur(image: Image.Image, amount: float) -> Image.Image:
    if amount == 0.0:
        return image
    radius = max(0.0, amount) * 5.0  # 0..1 -> 0..5px
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def _apply_denoise(image: Image.Image, amount: float) -> Image.Image:
    """ノイズ除去。amount=0 で無変化。MedianFilter で近似（決定的）。"""
    if amount == 0.0:
        return image
    # 強度に応じてカーネルサイズを 3,5 と離散化（奇数）。
    size = 5 if amount >= 0.5 else 3
    return image.filter(ImageFilter.MedianFilter(size=size))


def _apply_crop(image: Image.Image, crop: Crop | None) -> Image.Image:
    """トリミング。画像境界内にクランプし、1px 未満にはしない。"""
    if crop is None:
        return image
    width, height = image.size
    left = max(0, min(crop.x, width - 1))
    top = max(0, min(crop.y, height - 1))
    right = max(left + 1, min(crop.x + crop.width, width))
    bottom = max(top + 1, min(crop.y + crop.height, height))
    return image.crop((left, top, right, bottom))


def _apply_resize(image: Image.Image, resize: Resize | None) -> Image.Image:
    """リサイズ。keep_aspect=True なら target に収まる範囲でアスペクト比保持。"""
    if resize is None:
        return image
    target_w = max(1, resize.width)
    target_h = max(1, resize.height)
    if resize.keep_aspect:
        src_w, src_h = image.size
        scale = min(target_w / src_w, target_h / src_h)
        new_w = max(1, round(src_w * scale))
        new_h = max(1, round(src_h * scale))
    else:
        new_w, new_h = target_w, target_h
    return image.resize((new_w, new_h), Image.LANCZOS)


def _resolve_font(size: int) -> ImageFont.ImageFont:
    """クレジット用フォントを取得。環境非依存のため失敗時は既定ビットマップフォント。"""
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size=max(1, size))
        except OSError:
            continue
    return ImageFont.load_default()


def _credit_xy(
    position: CreditPosition,
    image_size: tuple[int, int],
    text_size: tuple[int, int],
    margin: int = 12,
) -> tuple[int, int]:
    img_w, img_h = image_size
    txt_w, txt_h = text_size
    if position is CreditPosition.TOP_LEFT:
        x, y = margin, margin
    elif position is CreditPosition.TOP_RIGHT:
        x, y = img_w - txt_w - margin, margin
    elif position is CreditPosition.BOTTOM_LEFT:
        x, y = margin, img_h - txt_h - margin
    elif position is CreditPosition.CENTER:
        x, y = (img_w - txt_w) // 2, (img_h - txt_h) // 2
    else:  # BOTTOM_RIGHT（既定）
        x, y = img_w - txt_w - margin, img_h - txt_h - margin
    # テキストが画像より大きい小さな画像でも、少なくとも一部が描画されるよう
    # 左上を画像内にクランプする（負座標だと画面外に描かれてしまうため）。
    x = max(0, min(x, max(0, img_w - 1)))
    y = max(0, min(y, max(0, img_h - 1)))
    return x, y


def _apply_credit(image: Image.Image, credit: Credit) -> Image.Image:
    """テキストクレジットを合成。text が空なら無変化。"""
    if credit.is_empty:
        return image

    base = image.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = _resolve_font(credit.size)

    try:
        bbox = draw.textbbox((0, 0), credit.text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except (AttributeError, ValueError):
        text_w, text_h = (credit.size * len(credit.text), credit.size)

    x, y = _credit_xy(credit.position, base.size, (text_w, text_h))
    alpha = max(0, min(255, round(credit.opacity * 255)))
    draw.text((x, y), credit.text, font=font, fill=(255, 255, 255, alpha))

    composited = Image.alpha_composite(base, overlay)
    # 元のモードが RGB なら RGB へ戻す（アルファを持ち込まない）。
    if image.mode == "RGB":
        return composited.convert("RGB")
    return composited


def apply(image: Image.Image, settings: EditSettings) -> Image.Image:
    """EditSettings を固定の合成順序で適用し、加工後の新しい Image を返す。

    合成順序（Q3・固定）: 補正 -> 画質 -> フィルタ(プリセット)
    -> トリミング/リサイズ -> クレジット。
    恒等設定（既定）では入力と同一内容を返す（決定的）。元 Image は変更しない。
    """
    # プリセットが指定されていれば、その効果を基準設定にマージする（明示指定を優先）。
    effective = settings
    if settings.preset_name:
        preset = get_preset(settings.preset_name)
        if preset is not None:
            effective = preset.merge_into(settings)

    result = image.copy()

    # 1) 補正（明るさ・コントラスト・彩度）
    result = _apply_brightness(result, effective.brightness)
    result = _apply_contrast(result, effective.contrast)
    result = _apply_saturation(result, effective.saturation)

    # 2) 画質（シャープ・ぼかし・ノイズ除去）
    result = _apply_sharpen(result, effective.sharpen)
    result = _apply_blur(result, effective.blur)
    result = _apply_denoise(result, effective.denoise)

    # 3) フィルタ（プリセットの色調は上の補正/彩度に含めて適用済み）
    #    ここでは追加のフィルタ効果があれば適用（mvp では補正ベースのプリセットのみ）。

    # 4) トリミング -> リサイズ
    result = _apply_crop(result, effective.crop)
    result = _apply_resize(result, effective.resize)

    # 5) クレジット（最後に載せる。リサイズ後なので文字がぼけない）
    result = _apply_credit(result, effective.credit)

    return result
