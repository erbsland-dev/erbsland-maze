#  Copyright © 2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

import enum
from typing import Self


ALIAS_MAP: dict[str, str] = {
    "se": "stretch_edge",
    "s": "stretch",
    "qt": "square_top_left",
    "q": "square_center",
    "ft": "fixed_top_left",
    "f": "fixed_center",
}


class SvgFillMode(enum.StrEnum):
    """
    The mode how the actual side length is calculated.
    """

    STRETCH_EDGE = "stretch_edge"
    """
    Calculate the best square room size from the side lengths and parity and stretch the rooms at the edges to
    completely fill the specified width and height.
    """

    STRETCH = "stretch"
    """
    Stretch the rooms into rectangles that completely fill the specified width and height.
    """

    SQUARE_TOP_LEFT = "square_top_left"
    """
    Use a square room size that fills at least one dimension perfectly, and align the maze at the top left corner.
    If the room size doesn't divide the with and height evenly, there will be a gap at the bottom or right side.
    """

    SQUARE_CENTER = "square_center"
    """
    Use a square room size that fills at least one dimension perfectly, and align the maze at the top left corner.
    If the room size doesn't divide the with and height evenly, there will be a gap around the maze.
    """

    FIXED_TOP_LEFT = "fixed_top_left"
    """
    Use a square room size with the exact side length as configured and place the maze in the top left corner.
    If the room size doesn't divide the with and height evenly, there will be a gap at the bottom or right side.
    """

    FIXED_CENTER = "fixed_center"
    """
    Use a square room size with the exact side length as configured and place the maze in the center.
    If the room size doesn't divide the with and height evenly, there will be a gap around the maze.
    """

    def does_stretch_edge(self) -> bool:
        """
        Tests if this value stretches the maze edge.
        """
        return self == self.STRETCH_EDGE

    def does_scale_room(self) -> bool:
        """
        Tests if this value scales the room, proportionally or not.
        """
        return self not in [self.FIXED_CENTER, self.FIXED_TOP_LEFT]

    def does_proportionally_scale_room(self) -> bool:
        """
        Tests if this value scales the room size to fill the area.
        """
        return self in [self.STRETCH_EDGE, self.SQUARE_TOP_LEFT, self.SQUARE_CENTER]

    def does_center_rooms(self) -> bool:
        """
        Tests if this value centers the room.
        """
        return self in [self.STRETCH_EDGE, self.SQUARE_CENTER, self.FIXED_CENTER]

    @classmethod
    def get_all_names(cls) -> list[str]:
        """
        Get all possible names for the fill modes.
        """
        result = [str(x) for x in cls]
        result.extend(ALIAS_MAP.keys())
        return sorted(result)

    @classmethod
    def from_name(cls, name: str) -> Self:
        """
        Get an instance from the given name.

        :param name: The name.
        :return: The enum value.
        """
        name = name.lower()
        if name in ALIAS_MAP:
            name = ALIAS_MAP[name]
        return cls(name)

    @classmethod
    def from_text(cls, text: str) -> Self:
        """
        Parse a text and convert it to a fill mode.

        :param text: The text to parse.
        :return: The enum value.
        """
        text = text.strip()
        if not text:
            raise ValueError("The fill mode parameter is empty.")
        try:
            return cls.from_name(text)
        except KeyError or ValueError:
            valid = ", ".join(cls.get_all_names())
            raise ValueError(f"The text '{text}' is not a valid fill mode. Valid values are {valid}.")
