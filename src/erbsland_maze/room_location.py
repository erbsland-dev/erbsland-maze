#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .direction import Direction


@dataclass(order=True, frozen=True)
class RoomLocation:
    """
    The location of a room in room units.
    """

    x: int = 0
    """The x coordinate of the room."""

    y: int = 0
    """The y coordinate of the room."""

    def advance(self, direction: Direction) -> "RoomLocation":
        """
        Get a new room location that is in the given direction.

        :param direction: The direction.
        :return: The new room location.
        """
        match direction:
            case Direction.NORTH:
                return RoomLocation(self.x, self.y - 1)
            case Direction.EAST:
                return RoomLocation(self.x + 1, self.y)
            case Direction.SOUTH:
                return RoomLocation(self.x, self.y + 1)
            case Direction.WEST:
                return RoomLocation(self.x - 1, self.y)

    def __sub__(self, other: "RoomLocation") -> "RoomLocation":
        if not isinstance(other, RoomLocation):
            raise TypeError("Can only subtract other room location.")
        return RoomLocation(self.x - other.x, self.y - other.y)

    def __add__(self, other: "RoomLocation") -> "RoomLocation":
        if not isinstance(other, RoomLocation):
            raise TypeError("Can only add other room location.")
        return RoomLocation(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return f"RoomLocation({self.x}, {self.y})"

    def translated(self, delta_x: int, delta_y: int) -> "RoomLocation":
        """
        Get a translated room location, with the given delta.

        :param delta_x: The delta in the X direction.
        :param delta_y: The delta in the Y direction.
        :return: The new room location.
        """
        return RoomLocation(self.x + delta_x, self.y + delta_y)

    @classmethod
    def from_text(cls, text: str) -> "RoomLocation":
        """
        Create a room location from a given text.

        :param text: The text to parse.
        :return: The room location.
        """
        if "," not in text:
            raise ValueError(f"The given text is not a valid room location.")
        text_parts = text.split(",")
        if len(text_parts) != 2:
            raise ValueError(f"The given text is not a valid room location.")
        text_x, text_y = text_parts
        try:
            value_x = int(text_x, base=10)
            value_y = int(text_y, base=10)
        except ValueError:
            raise ValueError("The given text is not a valid room location.")
        return cls(value_x, value_y)
