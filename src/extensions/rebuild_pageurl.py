# noqa: D100
from sphinx.application import Sphinx
from sphinx.util.docutils import nodes


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
    app.connect("html-page-context", rebuild_pageurl)
