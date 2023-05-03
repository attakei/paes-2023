"""Article hooks for ``og_image`` private package."""
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from docutils import nodes
from PIL.Image import Image
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging

from og_image import image, spec

logger = logging.getLogger(__name__)

_image_base: Optional[Image] = None
_spec: Optional[spec.TextSpec] = None

ENV_KEY = f"{__name__}__image_targets"


@dataclass
class OGImageTarget:
    """Stat of og-image."""

    text: str
    path: str


def get_ext_env(env: BuildEnvironment) -> Dict[str, OGImageTarget]:
    """Find or create env property in app environment."""
    if not hasattr(env, "atsphinx"):
        logger.debug("Init env for extensions")
        env.atsphinx: Dict[str, Any] = {}
    if ENV_KEY not in env.atsphinx:
        logger.debug(f"Init env for {__name__}")
        env.atsphinx[ENV_KEY] = {}
    return env.atsphinx[ENV_KEY]


def init_shared_values(app: Sphinx):
    """Set base image and spec for wrting images.

    It works when inited builder is only html-like.
    """
    get_ext_env(app.env)
    if app.builder.format != "html":
        return
    global _image_base, _spec
    spec_ = spec.load_toml(Path(app.config.x_aoi_image_spec), work_dir=Path.cwd())
    _image_base, _ = image.init_image(spec_.base.path)
    image.paste_rounted_image(_image_base, spec_.icon)
    image.write_text(_image_base, spec_.texts[0])
    _spec = spec_.texts[1]


def catch_og_image_target(app: Sphinx, doctree: addnodes.document):
    """Append og_image directive if not exists."""
    docname = app.env.docname
    metadata = app.env.metadata[docname]
    if docname in app.config.x_aoi_excludes:
        return
    if "og:image" not in metadata:
        image_name = docname.replace("/", "~") + f".{app.config.x_aoi_format}"
        metadata["og:image"] = f"{app.config.x_aoi_basepath}/{image_name}"
        out = f"{app.srcdir}/{app.config.x_aoi_basepath}/{image_name}"
        text = list(doctree.traverse(nodes.title))[0].astext()
        get_ext_env(app.env)[docname] = OGImageTarget(text=text, path=out)
        logger.debug(f"Add image for '{docname}'")


def write_og_image(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: addnodes.document,
):
    """Write og-image included page title."""
    if not doctree:
        return
    global _image_base, _spec
    if not _image_base or not _spec:
        return
    if pagename in app.config.x_aoi_excludes:
        return
    target = get_ext_env(app.env).get(pagename)
    if target is None:
        return
    logger.debug(f"Generate image for '{pagename}'")
    img = _image_base.copy()
    text_spec = deepcopy(_spec)
    text_spec.content = target.text
    image.write_text(img, text_spec)
    img.save(target.path)


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("x_aoi_format", "png", "env", [str])
    app.add_config_value("x_aoi_basepath", "_static", "env", [str])
    app.add_config_value("x_aoi_image_spec", None, "env", [Path])
    app.add_config_value("x_aoi_excludes", [], "env", [List[str]])
    app.connect("builder-inited", init_shared_values)
    app.connect("doctree-read", catch_og_image_target)
    app.connect("html-page-context", write_og_image)
