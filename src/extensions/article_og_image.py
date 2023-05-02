"""Article hooks for ``og_image`` private package."""
from sphinx import addnodes
from sphinx.application import Sphinx


def append_og_image(app: Sphinx, doctree: addnodes.document):
    """Append og_image directive if not exists."""
    docname = app.env.docname
    metadata = app.env.metadata[docname]
    if "og:image" not in metadata:
        image_name = docname.replace("/", "~")
        metadata[
            "og:image"
        ] = f"{app.config.x_aog_urlbase}/{image_name}.{app.config.x_aog_format}"


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("x_aog_format", "png", "env", [str])
    app.add_config_value("x_aog_urlbase", "_static", "env", [str])
    app.connect("doctree-read", append_og_image)
