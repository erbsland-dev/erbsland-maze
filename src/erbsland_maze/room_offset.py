#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass
from typing import Self

from .placement import Placement
from .room_location import RoomLocation


@dataclass(frozen=True)
class RoomOffset:

    x: int = 0
    """The offset in x direction, or the length for a relative offset."""

    y: int = 0
    """The offset in y direction. Ignored for relative offsets."""

    is_relative: bool = False
    """A relative positive offset moves the room from the placement towards the center."""

    def __str__(self):
        if self.is_relative:
            return f"{self.x}"
        return f"{self.x},{self.y}"

    def __repr__(self):
        return f"RoomLocation({self.x}, {self.y}, is_relative={self.is_relative})"

    @property
    def is_zero(self) -> bool:
        """
        Test if this offset does nothing.
        """
        return self.x == 0 and self.y == 0

    def translate_location(self, location: RoomLocation, placement: Placement) -> RoomLocation:
        """
        Return a new location with this offset and placement.

        :param location: The start location.
        :param placement: The placement.
        :return: The new location with this offset applied.
        """
        if self.is_zero or placement == Placement.RANDOM:
            return location
        if self.is_relative:
            dx, dy = placement.direction_normals()
            return RoomLocation(location.x + -dx * self.x, location.y + -dy * self.x)
        return RoomLocation(location.x + self.x, location.y + self.y)

    @classmethod
    def from_text(cls, text: str) -> Self:
        text = text.strip()
        if not text:
            raise ValueError("The offset parameter is empty.")
        try:
            if "," not in text:
                return cls(x=int(text, base=10), y=0, is_relative=True)
            text_parts = text.split(",")
            if len(text_parts) != 2:
                raise ValueError()
            text_x, text_y = text_parts
            return cls(x=int(text_x, base=10), y=int(text_y, base=10), is_relative=False)
        except ValueError:
            raise ValueError(
                f"The text '{text}' is not a valid offset. Either specify a single positive or negative integer "
                "value for a directional offset, or two integers seperated by a comma for a custom offset."
            )
