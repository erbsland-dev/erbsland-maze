#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass
from typing import Self

from erbsland_maze.closing_type import ClosingType


@dataclass(frozen=True)
class Closing:
    """
    A closing specification.
    """

    closing_type: ClosingType
    invert: bool = False

    def __str__(self):
        if self.invert:
            return f"^{self.closing_type.value}"
        else:
            return f"{self.closing_type.value}"

    @classmethod
    def from_text(cls, text: str) -> Self:
        inverted = False
        text = text.strip()
        if text.startswith("^"):
            inverted = True
            text = text[1:]
        closing_type = ClosingType.from_text(text)
        return cls(closing_type, inverted)
