"""Image editor functions."""
import tempfile
from pathlib import Path
from typing import Tuple

import cairosvg
from PIL import Image


def init_image(base_image_path: Path) -> Tuple[Image.Image, Path]:
    """Generate Pillow image on temporary area."""
    img_path = Path(tempfile.mktemp(suffix=".png"))
    cairosvg.svg2png(url=str(base_image_path), write_to=str(img_path))
    img = Image.open(img_path)
    return img, img_path
