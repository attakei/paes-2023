"""Image editor functions."""
import tempfile
from pathlib import Path
from typing import Tuple

import cairosvg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import spec


def init_image(base_image_path: Path) -> Tuple[Image.Image, Path]:
    """Generate Pillow image on temporary area."""
    img_path = Path(tempfile.mktemp(suffix=".png"))
    cairosvg.svg2png(url=str(base_image_path), write_to=str(img_path))
    img = Image.open(img_path)
    return img, img_path


def write_text(img: Image.Image, spec: spec.TextSpec) -> Image.Image:
    """Write text content for spec into target image."""
    font = ImageFont.truetype(str(spec.font_path), spec.font_size)
    draw = ImageDraw.Draw(img)
    draw.text(spec.pos.to_tuple(), spec.content, (0, 0, 0), font)
    return img


def paste_rounted_image(target: Image.Image, spec: spec.ImageSpec) -> Image.Image:
    """Paste image into target. source image is rounded."""
    source = Image.open(spec.path).copy()
    # Rounding
    mask = Image.new("L", source.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, source.size[0], source.size[1]), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    source.putalpha(mask)

    paste_img = Image.new("RGB", source.size, (255, 255, 255))
    paste_img.paste(source, mask=source.convert("RGBA").split()[-1])
    target.paste(
        paste_img.resize(spec.size.to_tuple(), resample=Image.Resampling.LANCZOS),
        spec.pos.to_tuple(),
    )
    return target
