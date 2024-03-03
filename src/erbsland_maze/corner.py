#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

import enum


class Corner(enum.StrEnum):
    """
    A corner of a room or maze.
    """

    TOP_LEFT = "top_left"
    """The top left corner."""

    TOP_RIGHT = "top_right"
    """The top right corner."""

    BOTTOM_RIGHT = "bottom_right"
    """The bottom right corner."""

    BOTTOM_LEFT = "bottom_left"
    """The bottom left corner."""

    def opposite(self):
        """
        Get the opposite corner.
        """
        match self:
            case Corner.TOP_RIGHT:
                return Corner.BOTTOM_LEFT
            case Corner.BOTTOM_RIGHT:
                return Corner.TOP_LEFT
            case Corner.BOTTOM_LEFT:
                return Corner.TOP_RIGHT
            case Corner.TOP_LEFT:
                return Corner.BOTTOM_RIGHT
