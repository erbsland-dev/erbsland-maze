#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import enum


class SvgZeroPoint(enum.Enum):
    """
    Where the SVG zero point shall be placed, which is the center of the maze.
    """

    CENTER = "center"
    """Create a SVG file for print, where the center is at the center of the canvas."""

    TOP_LEFT = "top_left"
    """Create a technical SVG file, where the center is at the top left of the canvas."""
