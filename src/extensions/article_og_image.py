"""Article hooks for ``og_image`` private package."""
from copy import deepcopy
from pathlib import Path

from docutils import nodes
from PIL import Image
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config

from og_image import image, spec

_image_base: Image.Image
_spec = spec.Spec


def append_og_image(app: Sphinx, doctree: addnodes.document):
    """Append og_image directive if not exists."""
    global _image_base, _spec
    docname = app.env.docname
    metadata = app.env.metadata[docname]
    if "og:image" not in metadata:
        image_name = docname.replace("/", "~") + f".{app.config.x_aog_format}"
        metadata["og:image"] = f"{app.config.x_aog_basepath}/{image_name}"
        out = f"{app.srcdir}/{app.config.x_aog_basepath}/{image_name}"
        img = _image_base.copy()

        text_spec = deepcopy(_spec.texts[1])
        text_spec.content = list(doctree.traverse(nodes.title))[0].astext()
        image.write_text(img, text_spec)
        img.save(out)


def init_shared_vals(app: Sphinx, config: Config):
    """Initialze module-wide variables."""
    global _image_base, _spec
    _spec = spec.load_toml(Path(config.x_aog_image_spec), work_dir=Path.cwd())
    _image_base, _ = image.init_image(_spec.base.path)
    image.paste_rounted_image(_image_base, _spec.icon)
    image.write_text(_image_base, _spec.texts[0])


def setup(app: Sphinx):  # noqa: D103
    global _image_base, _spec
    app.add_config_value("x_aog_format", "png", "env", [str])
    app.add_config_value("x_aog_basepath", "_static", "env", [str])
    app.add_config_value("x_aog_image_spec", None, "env", [Path])
    app.connect("config-inited", init_shared_vals)
    app.connect("doctree-read", append_og_image)
