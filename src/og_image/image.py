"""Image editor functions."""
import tempfile
from pathlib import Path
from typing import Tuple

import cairosvg
from PIL import Image, ImageDraw, ImageFont

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
