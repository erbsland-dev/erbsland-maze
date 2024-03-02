#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import enum


class ModifierType(enum.Enum):
    """
    The type of modifier.
    """

    BLANK = "blank"
    """Create a blank space at the specified location."""

    FRAME = "frame"
    """Creates a blank space all around the maze with the specified size."""

    CLOSING = "close"
    """Permanently closes connections in portions of the maze"""

    MERGE = "merge"
    """Merge rooms into a larger room at the specified location."""
