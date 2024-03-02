#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class RoomSize:
    """
    The size of a room in room units.
    """

    width: int = 0
    height: int = 0

    def __str__(self):
        return f"{self.width}x{self.height}"

    @property
    def is_one(self) -> bool:
        return self.width == 1 and self.height == 1

    @classmethod
    def from_text(cls, text: str) -> Self:
        """
        Create a room size from the given text.

        The text can be a name like "single", "small", "medium" or "large", or
        a single positive integer, or two integer seperated by a comma.

        :param text: The text to parse.
        :return: A room size.
        """
        text = text.lower()
        if text == "single":
            return cls(1, 1)
        if text == "small":
            return cls(2, 2)
        if text == "medium":
            return cls(3, 3)
        if text == "large":
            return cls(4, 4)
        if "x" not in text:
            try:
                value = int(text, base=10)
            except ValueError:
                raise ValueError("The given text is not a valid room size.")
            if value < 1 or value >= 10_000:
                raise ValueError("The given text is not a valid room size.")
            return cls(value, value)
        text_parts = text.split("x")
        if len(text_parts) != 2:
            raise ValueError("The given text is not a valid room size.")
        text_x, text_y = text_parts
        try:
            value_x = int(text_x.strip(), base=10)
            value_y = int(text_y.strip(), base=10)
        except ValueError:
            raise ValueError("The given text is not a valid room size.")
        if value_x < 1 or value_x >= 10_000 or value_y < 1 or value_y >= 10_000:
            raise ValueError("The given text is not a valid room size.")
        return cls(value_x, value_y)
