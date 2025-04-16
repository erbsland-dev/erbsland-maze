# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

try:
    import sphinx_rtd_theme
except ImportError:
    sphinx_rtd_theme = None

# -- Execute the _about package ----------------------------------------------

base_dir = Path(__file__).parent.parent
about = {}
sys.path.insert(0, str(base_dir / "src"))

# -- Prevent errors from a missing `cairo` package ---------------------------

MOCK_MODULES = ["cairo"]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = MagicMock()

# -- Project information -----------------------------------------------------

project = "Erbsland Maze"
if True:
    from erbsland_maze.about import get_version, get_author, get_copyright

    copyright = get_copyright()
    author = get_author()
    version = release = get_version()

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

if sphinx_rtd_theme:
    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = "default"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
