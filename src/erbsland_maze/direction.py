#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

import enum


class Direction(enum.IntEnum):
    """
    A direction in the maze.
    """

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(self):
        match self:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.WEST:
                return Direction.EAST
