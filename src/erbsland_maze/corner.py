#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

import enum


class Corner(enum.StrEnum):
    """
    A corner of a room or maze.
    """

    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_RIGHT = "bottom_right"
    BOTTOM_LEFT = "bottom_left"

    def opposite(self):
        match self:
            case Corner.TOP_RIGHT:
                return Corner.BOTTOM_LEFT
            case Corner.BOTTOM_RIGHT:
                return Corner.TOP_LEFT
            case Corner.BOTTOM_LEFT:
                return Corner.TOP_RIGHT
            case Corner.TOP_LEFT:
                return Corner.BOTTOM_RIGHT
