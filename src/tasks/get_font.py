#!/usr/bin/env python
"""Download font file from HTTP."""
import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import click

FONT_ZIP_URL = "https://seed.line.me/src/images/fonts/LINE_Seed_JP.zip"


@click.command()
@click.argument(
    "dest", type=click.Path(file_okay=False, dir_okay=True, exists=True, path_type=Path)
)
def main(dest: Path):  # noqa: D103
    resp = urlopen(FONT_ZIP_URL)
    content = io.BytesIO(resp.read())
    with zipfile.ZipFile(content, mode="r") as zfp:
        for info in zfp.filelist:
            if not info.filename.endswith(".otf"):
                continue
            filename = info.filename.split("/")[-1]
            with (dest / filename).open("wb") as fp:
                fp.write(zfp.read(info))


if __name__ == "__main__":
    main()
