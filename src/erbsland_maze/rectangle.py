#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from .point import Point
from .size import Size


class Rectangle:
    """
    A rectangle.
    """

    def __init__(self, pos: Point, size: Size):
        """
        Create a new rectangle.

        :param pos: The position of the top-left corner.
        :param size: The size of the rectangle.
        """
        self.pos = pos
        self.size = size

    @property
    def x1(self) -> float:
        """
        Get the x coordinate of the left side.
        """
        return self.pos.x

    @property
    def y1(self) -> float:
        """
        Get the y coordinate of the top side.
        """
        return self.pos.y

    @property
    def x2(self) -> float:
        """
        Get the x coordinate of the right side.
        """
        return self.pos.x + self.size.width

    @property
    def y2(self) -> float:
        """
        Get the y coordinate of the bottom side.
        """
        return self.pos.y + self.size.height

    @property
    def top_left(self) -> Point:
        """
        Get the point in the top-left corner.
        """
        return Point(self.x1, self.y1)

    @property
    def top_right(self) -> Point:
        """
        Get the point in the top-right corner.
        """
        return Point(self.x2, self.y1)

    @property
    def bottom_left(self) -> Point:
        """
        Get the point in the bottom-left corner.
        """
        return Point(self.x1, self.y2)

    @property
    def bottom_right(self) -> Point:
        """
        Get the point in the bottom-right corner.
        """
        return Point(self.x2, self.y2)

    def equally_inset_by(self, distance: float) -> "Rectangle":
        """
        Return a new rectangle that is equally inset by the given distance.

        :param distance: The distance.
        :return: The new rectangle.
        """
        return Rectangle(
            Point(self.pos.x + distance, self.pos.y + distance),
            Size(self.size.width - 2 * distance, self.size.height - 2 * distance),
        )
