"""Spec definition of generated image."""
from pathlib import Path
from typing import List, Tuple, Union

import tomli
from pydantic import BaseModel

Number = Union[int, float]


class PositionD2(BaseModel):  # noqa: D101
    x: Number
    y: Number

    def to_tuple(self) -> Tuple[Number, Number]:  # noqa: D102
        return (self.x, self.y)


class SizeD2(BaseModel):  # noqa: D101
    width: Number
    height: Number

    def to_tuple(self) -> Tuple[Number, Number]:  # noqa: D102
        return (self.width, self.height)


class BaseImageSpec(BaseModel):
    """Base image spec."""

    path: Path
    size: SizeD2


class ImageSpec(BaseModel):
    """Image drawing spec."""

    path: Path
    size: SizeD2
    pos: PositionD2


class TextSpec(BaseModel):
    """Text drawing spec."""

    font_path: Path
    font_size: int
    pos: PositionD2
    content: str


class Spec(BaseModel):
    """Spec of generated image.

    It is used as base image and edit attributes.
    """

    base: BaseImageSpec
    icon: ImageSpec
    texts: List[TextSpec]


def load_toml(src: Path, *, work_dir: Path) -> Spec:
    """Load spec object from TOML file."""
    data = tomli.loads(src.read_text())
    data["base"]["path"] = data["base"]["path"].format(work_dir=str(work_dir))
    data["icon"]["path"] = data["icon"]["path"].format(work_dir=str(work_dir))
    for attr in data["texts"]:
        attr["font_path"] = attr["font_path"].format(work_dir=str(work_dir))
    return Spec(**data)
