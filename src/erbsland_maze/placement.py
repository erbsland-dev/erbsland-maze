#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import enum
import math
import random
from typing import Tuple, Self

from .room_location import RoomLocation
from .room_size import RoomSize


class Placement(enum.StrEnum):
    """
    Logical placement of an element.
    """

    LEFT = "left"
    TOP_LEFT = "top_left"
    TOP = "top"
    TOP_RIGHT = "top_right"
    RIGHT = "right"
    BOTTOM_RIGHT = "bottom_right"
    BOTTOM = "bottom"
    BOTTOM_LEFT = "bottom_left"
    CENTER = "center"
    RANDOM = "random"

    def direction_normals(self) -> Tuple[int, int]:
        """
        Get normals to detect the direction of this placement.
        """
        match self:
            case Placement.LEFT:
                return -1, 0
            case Placement.TOP_LEFT:
                return -1, -1
            case Placement.TOP:
                return 0, -1
            case Placement.TOP_RIGHT:
                return 1, -1
            case Placement.RIGHT:
                return 1, 0
            case Placement.BOTTOM_RIGHT:
                return 1, 1
            case Placement.BOTTOM:
                return 0, 1
            case Placement.BOTTOM_LEFT:
                return -1, 1
            case Placement.CENTER:
                return 0, 0
            case Placement.RANDOM:
                return 0, 0
        raise NotImplementedError("Placement not implemented")

    def placement_normals(self) -> Tuple[float, float]:
        """
        Get normals to get a placement.
        """
        if self == Placement.RANDOM:
            return random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)
        nx, ny = self.direction_normals()
        return (nx + 1) / 2, (ny + 1) / 2

    def offset(self, value: int) -> RoomLocation:
        """
        Get an offset that points towards the center.

        :param value: The number of rooms toward the center.
        :return: The offset as room location.
        """
        dx, dy = self.direction_normals()
        return RoomLocation(dx * -value, dy * -value)

    def size_offset(self, size: RoomSize) -> RoomLocation:
        """
        A size offset to correct a placement according to the size of the affected locations.

        :param size: The size.
        :return: The offset as room location.
        """
        full_x = size.width - 1
        full_y = size.height - 1
        half_x = -int(math.floor(full_x // 2))
        half_y = -int(math.floor(full_y // 2))
        match self:
            case Placement.LEFT:
                return RoomLocation(0, half_y)
            case Placement.TOP_LEFT:
                return RoomLocation(0, 0)
            case Placement.TOP:
                return RoomLocation(half_x, 0)
            case Placement.TOP_RIGHT:
                return RoomLocation(-full_x, 0)
            case Placement.RIGHT:
                return RoomLocation(-full_x, half_y)
            case Placement.BOTTOM_RIGHT:
                return RoomLocation(-full_x, -full_y)
            case Placement.BOTTOM:
                return RoomLocation(half_x, -full_y)
            case Placement.BOTTOM_LEFT:
                return RoomLocation(0, -full_y)
            case Placement.CENTER:
                return RoomLocation(half_x, half_y)
            case Placement.RANDOM:
                return RoomLocation(0, 0)

    @property
    def order_value(self) -> int:
        """
        Return a value to order modifications in a sequence to case the least amount of conflicts.
        """
        match self:
            case Placement.LEFT:
                return 208
            case Placement.TOP_LEFT:
                return 201
            case Placement.TOP:
                return 202
            case Placement.TOP_RIGHT:
                return 203
            case Placement.RIGHT:
                return 204
            case Placement.BOTTOM_RIGHT:
                return 205
            case Placement.BOTTOM:
                return 206
            case Placement.BOTTOM_LEFT:
                return 207
            case Placement.CENTER:
                return 100  # Place center first.
            case Placement.RANDOM:
                return 300  # Place random last.

    @classmethod
    def alias_map(cls) -> dict[str, str]:
        return {
            "w": "left",
            "nw": "top_left",
            "n": "top",
            "ne": "top_right",
            "e": "right",
            "se": "bottom_right",
            "s": "bottom",
            "sw": "bottom_left",
            "c": "center",
            "r": "random",
        }

    @classmethod
    def from_name(cls, name: str) -> Self:
        alias_map = cls.alias_map()
        if name in alias_map:
            name = alias_map[name]
        return cls(name)

    @classmethod
    def all_names(cls) -> list[str]:
        result = list(cls.alias_map().keys())
        result.extend([str(x) for x in cls])
        result.sort()
        return result

    @classmethod
    def from_text(cls, text: str) -> Self:
        text = text.strip()
        if not text:
            raise ValueError("The placement parameter is empty.")
        try:
            return cls.from_name(text)
        except KeyError or ValueError:
            valid = ", ".join(cls.all_names())
            raise ValueError(f"The text '{text}' is not a valid placement name. Valid values are {valid}.")
