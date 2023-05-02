# noqa: D100
import logging
from pathlib import Path

import click

from . import image, spec

logger = logging.getLogger(__name__)


@click.command()
@click.option("--debug", type=bool, is_flag=True)
@click.argument(
    "src",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=Path
    ),
)
@click.argument(
    "out",
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True, path_type=Path),
)
def main(src: Path, out: Path, debug: bool = False):
    """Generate of-image by spec."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    logger.debug("Start")
    work_dir = Path.cwd()
    logger.debug(f"Working-directory is {work_dir}")
    spec_ = spec.load_toml(src, work_dir=work_dir)
    img, _ = image.init_image(spec_.base.path)

    img.save(out)
    logger.debug("End")


main()
