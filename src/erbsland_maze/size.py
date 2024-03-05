#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from math import floor
from typing import Self, Union

from .parity import Parity
from .point import Point
from .room_size import RoomSize


@dataclass(order=True, frozen=True)
class Size:
    """
    A graphical size.
    """

    width: float
    """The width of the size."""

    height: float
    """The height of the size."""

    def __str__(self) -> str:
        return f"({self.width}, {self.height})"

    def __repr__(self):
        return f"Size({self.width:0.2f},{self.height:0.2f})"

    def __add__(self, other: Union[Self, float]) -> Self:
        if isinstance(other, Size):
            return Size(self.width + other.width, self.height + other.height)
        if isinstance(other, float):
            return Size(self.width + other, self.height + other)
        raise NotImplemented("Can only subtract `Size` or `float`.")

    def __sub__(self, other: Union[Self, float]) -> Self:
        if isinstance(other, Size):
            return Size(self.width - other.width, self.height - other.height)
        if isinstance(other, float):
            return Size(self.width - other, self.height - other)
        raise NotImplemented("Can only subtract `Size` or `float`.")

    def __mul__(self, other: Union[Self, RoomSize, float]) -> Self:
        if isinstance(other, Size) or isinstance(other, RoomSize):
            return Size(self.width * other.width, self.height * other.height)
        if isinstance(other, float):
            return Size(self.width * other, self.height * other)
        raise NotImplemented("Can only multiply `Size`, `RoomSize` or `float`.")

    def __truediv__(self, other: Union[RoomSize, float]) -> Self:
        if isinstance(other, RoomSize):
            return Size(self.width / other.width, self.height / other.height)
        if isinstance(other, float):
            return Size(self.width / other, self.height / other)
        raise NotImplemented("Can only divide by `RoomSize`, or `float`.")

    @staticmethod
    def _count_with_parity(total_length: float, side_length: float, parity: Parity) -> int:
        """
        Get a room count for the given length, using a parity.

        Ensures `side_length * count <= total_length`.

        :param total_length: The length of the dimension to divide.
        :param side_length: The length of a section.
        :param parity: The parity.
        :return: The ideal number of sections with the given parity.
        """
        if parity == Parity.NONE:
            result = int(floor(total_length / side_length))
        else:
            result = int(floor(total_length / side_length / 2)) * 2
            if parity == Parity.ODD:
                result -= 1
        return result

    def count_with_parity(self, room_size: "Size", parity_width: Parity, parity_height: Parity) -> RoomSize:
        """
        Divide this area into rooms respecting the given parity.

        :param room_size: The size of the rooms.
        :param parity_width: The parity for the width.
        :param parity_height: The parity for the height.
        :return: The room count with the width and height.
        """
        return RoomSize(
            self._count_with_parity(self.width, room_size.width, parity_width),
            self._count_with_parity(self.height, room_size.height, parity_height),
        )

    def min_square(self) -> Self:
        """
        Get the smallest square that fits into this size.
        """
        side = min(self.width, self.height)
        return Size(side, side)

    def get_center_point(self) -> Point:
        return Point(self.width / 2.0, self.height / 2.0)

    def get_center_offset(self, other_size: Self) -> Point:
        """
        Get the relative offset to center the other size in the area defined by this size.

        :param other_size: The other size.
        :return: A relative offset as point from the top left corner of this size.
        """
        if not isinstance(other_size, Size):
            raise TypeError("Argument must be of type `Size`.")
        offset_size = (self - other_size) / 2.0
        return Point(offset_size.width, offset_size.height)
