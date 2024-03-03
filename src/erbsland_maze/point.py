#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Point:
    """
    A point.
    """

    x: float = 0.0
    """The x coordinate of the point."""

    y: float = 0.0
    """The y coordinate of the point."""

    def __repr__(self):
        return f"Point({self.x:0.2f},{self.y:0.2f})"

    def __add__(self, other: "Point") -> "Point":
        if not isinstance(other, Point):
            raise ValueError("Can only add points.")
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        if not isinstance(other, Point):
            raise ValueError("Can only subtract points.")
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        x1 = int(round(self.x * 1_000_000))
        y1 = int(round(self.y * 1_000_000))
        x2 = int(round(other.x * 1_000_000))
        y2 = int(round(other.y * 1_000_000))
        return x1 == x2 and y1 == y2

    def __hash__(self) -> int:
        x1 = int(round(self.x * 1_000_000))
        y1 = int(round(self.y * 1_000_000))
        return hash((x1, y1))

    def translated(self, x: float = 0.0, y: float = 0.0) -> "Point":
        """
        Return a new point that was translated by the given distance.

        :param x: The movement in the X direction.
        :param y: The movement in the Y direction.
        :return: A new point that was translated by the given distance.
        """
        return Point(self.x + x, self.y + y)
