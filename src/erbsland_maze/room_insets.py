#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import Self


@dataclass
class RoomInsets:
    """
    Room location insets.
    """

    north: int = 0
    east: int = 0
    south: int = 0
    west: int = 0

    def __str__(self):
        return f"{self.north},{self.east},{self.south},{self.west}"

    def __repr__(self):
        return f"RoomInsets(north={self.north},east={self.east},south={self.south},west={self.west})"

    @staticmethod
    def value_from_text(text: str) -> int:
        """
        Convert a text into an inset value.

        :param text: The text to convert.
        :return: The resulting value.
        """
        try:
            value = int(text[0], base=10)
        except ValueError:
            raise ValueError("The given text is not a valid inset.")
        if value < 1 or value >= 10_000:
            raise ValueError("The given text is not a valid inset.")
        return value

    @classmethod
    def from_text(cls, text: str) -> Self:
        """
        Create an inset definition from the given text.

        The text can be a single positive integer, or two, or four integer seperated by a comma.

        :param text: The text to parse.
        :return: A room size.
        """
        text_parts = text.lower().split(",")
        if not text_parts:
            raise ValueError("The given text is empty.")
        if len(text_parts) == 1:
            value = cls.value_from_text(text_parts[0])
            return cls(value, value, value, value)
        if len(text_parts) == 2:
            values = [cls.value_from_text(text) for text in text_parts]
            return cls(values[0], values[1], values[0], values[1])
        if len(text_parts) <= 4:
            values = [cls.value_from_text(text) for text in text_parts]
            return cls(*values)
        raise ValueError("The given text is not a valid inset. There are too many values.")
