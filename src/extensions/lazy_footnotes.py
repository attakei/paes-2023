# noqa: D100
from sphinx.application import Sphinx
from sphinx.util.docutils import nodes


def collect_footnotes(app: Sphinx, doctree: nodes.document):
    """Collect and display later all footnotes."""
    footnotes = nodes.section()
    for footnote in doctree.traverse(nodes.footnote):
        footnote.parent.remove(footnote)
        footnotes.append(footnote)
    if len(footnotes.children):
        footnotes.insert(0, nodes.rubric(text="※脚注"))
        doctree.append(footnotes)


def setup(app: Sphinx):  # noqa: D103
    app.connect("doctree-read", collect_footnotes)
