#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .point import Point


@dataclass
class WallPoints:
    """
    Points that are used to create the lines for a wall.
    """

    adjacent1: Point
    inset1: Point
    adjacent2: Point
    inset2: Point
