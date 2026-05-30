#  Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# -- Prevent errors from a missing `cairo` package ---------------------------
sys.modules["cairo"] = MagicMock()

# -- Project information -----------------------------------------------------
project = "Erbsland Maze"
copyright = "2003-2026, Tobias Erbsland - Erbsland DEV"
author = "Tobias Erbsland - Erbsland DEV"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
]
templates_path = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Autodoc configuration ---------------------------------------------------
autodoc_member_order = "bysource"
add_module_names = False

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_template_path = []
