#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import math

from .point import Point
from .types import GenericLine


class Line(GenericLine):
    """
    A straight line between two points.
    """

    def __init__(self, p1: Point, p2: Point):
        """
        Create a new line.

        :param p1: The start point.
        :param p2: The end point.
        """
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other: "Line"):
        return self

    @property
    def first(self) -> Point:
        return self.p1

    @property
    def last(self) -> Point:
        return self.p2

    @property
    def points(self) -> list[Point]:
        return [self.p1, self.p2]

    def is_collinear_with(self, other: "Line") -> bool:
        """
        Check if this line is collinear with another line.

        :param other: The other line to check collinearity with.
        :return: True if the lines are collinear, False otherwise.
        """
        # Unpack points to simplify the calculation
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = other.p1.x, other.p1.y
        x4, y4 = other.p2.x, other.p2.y

        slope_difference_a = (x1 - x2) * (y3 - y1) - (x3 - x1) * (y1 - y2)
        slope_difference_b = (x1 - x2) * (y4 - y1) - (x4 - x1) * (y1 - y2)
        return math.isclose(slope_difference_a, 0.0, rel_tol=1e-6) and math.isclose(
            slope_difference_b, 0.0, rel_tol=1e-6
        )
