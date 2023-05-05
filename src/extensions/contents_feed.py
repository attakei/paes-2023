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
* python-dateutil
"""

__version__ = "0.0.1"

from datetime import datetime
from typing import Optional
from xml.etree import ElementTree as ET

from dateutil.parser import parse
from dateutil.tz import tz
from docutils import nodes
from feedgen.feed import FeedGenerator
from sphinx import addnodes
from sphinx.application import Sphinx


class feed_entry(nodes.General, nodes.Element):
    """Simple node to store information of feed entry."""


def skip_node(self, node: nodes.Element):  # noqa: D103
    raise nodes.SkipNode


def calc_updated(
    published: Optional[str] = None,
    modified: Optional[str] = None,
    tzinfo: Optional[str] = None,
) -> datetime:
    """Detect 'updated' date."""
    source = None
    if published:
        source = published
    if modified:
        source = modified
    if source is None:
        raise ValueError("Time information is not exists.")
    dt = parse(source)
    if dt.tzinfo is None and tzinfo is not None:
        dt = dt.astimezone(tz.gettz(tzinfo))
    return dt


def process_entry(app: Sphinx, doctree: addnodes.document):
    """Proccess doc to create and save feed entry information."""
    # Find key metadata
    metadata = app.env.metadata[app.env.docname]
    published_time = metadata.get("article:published_time", None)
    modified_time = metadata.get("article:modified_time", None)
    # Check that doctree is target of feed
    if published_time is None and modified_time is None:
        return
    entry_node = feed_entry()
    entry_node["content"] = app.config.x_cf_default_content
    entry_node["title"] = list(doctree.findall(nodes.title))[0].astext()
    entry_node["updated"] = calc_updated(
        published_time, modified_time, app.config.x_cf_timezone
    )
    entry_node["summary"] = None
    for paragraph in doctree.findall(nodes.paragraph):
        if isinstance(paragraph.parent, nodes.section):
            entry_node["summary"] = paragraph.astext()
    if "og:description" in metadata:
        entry_node["summary"] = metadata["og:description"]
    else:
        for meta in doctree.findall(nodes.meta):
            if meta["name"] == "description":
                entry_node["summary"] = meta["content"]
    doctree.children.append(entry_node)


def append_feed_link(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: addnodes.document,
):
    """Add link tag into page metatags."""
    if "metatags" not in context:
        context["metatags"] = ""
    link = ET.Element(
        "link",
        attrib={
            "rel": "alternate",
            "type": "application/atom+xml",
            "href": f"{app.config.html_baseurl}/{app.config.x_cf_filename}",
            "title": f"Articles of {app.config.project}",
        },
    )
    context["metatags"] += ET.tostring(link).decode()


def generate_feed(app: Sphinx, exc: Exception):
    """Build and write feed file into outdir."""
    # Work only html-like builders.
    if app.builder.format != "html":
        return
    fg = FeedGenerator()
    fg.id(app.config.html_baseurl)
    fg.title(app.config.html_title)
    fg.language(app.config.language)
    for docname in app.env.all_docs:
        doctree = app.env.get_doctree(docname)
        for entry in doctree.findall(feed_entry):
            fe = fg.add_entry()
            fe.id(f"{app.config.html_baseurl}.{app.builder.get_target_uri(docname)}")
            fe.title(entry["title"])
            fe.content(entry["content"])
            fe.updated(entry["updated"])
            if entry["summary"]:
                fe.summary(entry["summary"])
    fg.atom_file(f"{app.outdir}/{app.config.x_cf_filename}")


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("x_cf_filename", "atom.xml", "env", [str])
    """Geneted filename by extension into outdir."""
    app.add_config_value("x_cf_timezone", "UTC", "env", [str])
    """TZinfo text to render 'updated' into feed file."""
    app.add_config_value("x_cf_default_content", "(Please see webpage)", "env", [str])
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
    app.connect("html-page-context", append_feed_link)
    app.connect("build-finished", generate_feed)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
