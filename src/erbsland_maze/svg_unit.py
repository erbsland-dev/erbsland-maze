#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

import enum


class SvgUnit(enum.Enum):
    """
    SVG units to use for a document.
    """

    MM = 0
    """Millimetre unit."""

    PX = 1
    """Pixel unit."""
