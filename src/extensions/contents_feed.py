"""Content feed extension.

Overview
--------

This extension generates RSS feed from documents categorized as "content".
"content" has ``article:published_time`` or ``article:modified_time``
on metadata fields.
(This is based OpenGraph)

Works
-----

* Feed entry is created by docname, doctree and metadata.
* Feed file is created on last phase of build and only html-like builder.

Dependencies
------------

* feedgen
"""

__version__ = "0.0.1"

from docutils import nodes
from feedgen.feed import FeedGenerator
from sphinx.addnodes import document
from sphinx.application import Sphinx


class feed_entry(nodes.Element):
    """Simple node to store information of feed entry."""


def process_entry(app: Sphinx, doctree: document):
    """Proccess doc to create and save feed entry information."""
    # Find key metadata
    metadata = app.env.metadata[app.env.docname]
    published_time = metadata.get("article:published_time", None)
    modified_time = metadata.get("article:modified_time", None)
    # Check that doctree is target of feed
    if published_time is None and modified_time is None:
        return
    # TODO: Implement to pick elements of enetry
    entry_node = feed_entry()
    doctree.children.append(entry_node)


def generate_feed(app: Sphinx, exc: Exception):
    """Build and write feed file into outdir."""
    # Work only html-like builders.
    if app.builder.format != "html":
        return
    fg = FeedGenerator()
    fg.id(app.config.html_baseurl)
    fg.title(app.config.html_title)
    fg.language(app.config.language)
    fg.atom_file(f"{app.outdir}/{app.config.x_cf_filename}")


def skip_node(self, node: nodes.Element):  # noqa: D103
    raise nodes.SkipNode


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("x_cf_filename", "atom.xml", "env", [str])
    """Geneted filename by extension into outdir."""
    app.add_config_value("x_cf_timezone", "UTC", "env", [str])
    """TZinfo text to render 'updated' into feed file."""
    app.add_node(
        feed_entry,
        html=(skip_node, None),
        latex=(skip_node, None),
        text=(skip_node, None),
        man=(skip_node, None),
        texinfo=(skip_node, None),
    )
    app.connect("doctree-read", process_entry)
    app.connect("build-finished", generate_feed)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
