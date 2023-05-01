"""Configuration of Sphinx."""

# -- Project information
project = "attakei pages"
copyright = "2012-2023, Kazuya Takei"
author = "Kazuya Takei"
release = "2023.5.1"

# -- General configuration
extensions = [
    "extensions.lazy_footnotes",
    "extensions.rebuild_pageurl",
    "sphinxext.opengraph",
]
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
# sphinxext-opengraph
ogp_site_url = html_baseurl
ogp_description_length = 100
ogp_type = "article"
