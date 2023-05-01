"""Configuration of Sphinx."""
from sphinx.application import Sphinx
from sphinx.util.docutils import nodes

# -- Project information
project = "attakei pages"
copyright = "2012-2023, Kazuya Takei"
author = "Kazuya Takei"
release = "2023.5.1"

# -- General configuration
extensions = []
templates_path = ["_templates"]
exclude_patterns = []
language = "ja"

# -- Options for HTML output
html_theme = "piccolo_theme"
html_title = "attakei pages"
html_baseurl = "https://attakei.net"  # Not need to change by environment
html_static_path = ["_static"]
html_css_files = ["css/site.css"]

# -- Options for extensions


def collect_footnotes(app: Sphinx, doctree: nodes.document):
    """Display all footnotes into tail of pages."""
    footnotes = nodes.section()
    for footnote in doctree.traverse(nodes.footnote):
        footnote.parent.remove(footnote)
        footnotes.append(footnote)
    if len(footnotes.children):
        footnotes.insert(0, nodes.rubric(text="※脚注"))
        doctree.append(footnotes)


def rebuild_pageurl(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: nodes.document,
):
    """Update canonical URL for dirhtml.

    :ref: https://github.com/sphinx-doc/sphinx/issues/9730
    """
    if not app.config.html_baseurl:
        return
    context["pageurl"] = f"{app.config.html_baseurl}/{pagename}/"


def setup(app: Sphinx):  # noqa: D103
    app.connect("doctree-read", collect_footnotes)
    app.connect("html-page-context", rebuild_pageurl)
