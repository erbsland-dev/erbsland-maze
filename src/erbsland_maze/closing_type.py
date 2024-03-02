#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import enum
from typing import Self


class ClosingType(enum.Enum):

    CORNER_PATHS = "corner_paths"
    CORNER_TOP_LEFT = "corner_top_left"
    CORNER_TOP_RIGHT = "corner_top_right"
    CORNER_BOTTOM_RIGHT = "corner_bottom_right"
    CORNER_BOTTOM_LEFT = "corner_bottom_left"
    DIRECTION_WEST = "direction_west"
    DIRECTION_NORTH = "direction_north"
    DIRECTION_EAST = "direction_east"
    DIRECTION_SOUTH = "direction_south"
    DIRECTION_HORIZONTAL = "direction_horizontal"
    DIRECTION_VERTICAL = "direction_vertical"
    MIDDLE_PATHS = "middle_paths"
    MIDDLE_WEST = "middle_west"
    MIDDLE_NORTH = "middle_north"
    MIDDLE_EAST = "middle_east"
    MIDDLE_SOUTH = "middle_south"

    @classmethod
    def alias_map(cls) -> dict[str, str]:
        return {
            "c": "CORNER_PATHS",
            "cnw": "CORNER_TOP_LEFT",
            "cne": "CORNER_TOP_RIGHT",
            "cse": "CORNER_BOTTOM_RIGHT",
            "csw": "CORNER_BOTTOM_LEFT",
            "dw": "DIRECTION_WEST",
            "dn": "DIRECTION_NORTH",
            "de": "DIRECTION_EAST",
            "ds": "DIRECTION_SOUTH",
            "dh": "DIRECTION_HORIZONTAL",
            "dv": "DIRECTION_VERTICAL",
            "m": "MIDDLE_PATHS",
            "mw": "MIDDLE_WEST",
            "mn": "MIDDLE_NORTH",
            "me": "MIDDLE_EAST",
            "ms": "MIDDLE_SOUTH",
        }

    @classmethod
    def from_name(cls, name: str) -> Self:
        alias_map = cls.alias_map()
        if name in alias_map:
            name = alias_map[name]
        return cls[name]

    @classmethod
    def all_names(cls) -> list[str]:
        result = list(cls.alias_map().keys())
        result.extend([x.value for x in cls])
        result.sort()
        return result

    @classmethod
    def from_text(cls, text: str) -> Self:
        text = text.strip()
        if not text:
            raise ValueError("The closing type parameter is empty.")
        try:
            return cls.from_name(text)
        except KeyError:
            valid = ", ".join(cls.all_names())
            raise ValueError(f"The text '{text}' is not a valid closing type. Valid values are {valid}.")
