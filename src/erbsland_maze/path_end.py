#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field

from .placement import Placement
from .room_offset import RoomOffset


@dataclass(frozen=True)
class PathEnd:
    """
    Represents the end of a connected path.
    This can also be an intermediate point of the path, that must be connected.
    """

    placement: Placement
    """The placement of the path end."""

    offset: RoomOffset = field(default_factory=RoomOffset)
    """The offset from this placement."""

    is_dead_end: bool = False
    """
    If this path end is a dead-end and does not connect any other path ends.
    A such path can be cut short to allow connecting the real paths.
    """

    name: str = ""
    """
    The name that was used to configure this path. Used in error messages.
    """

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"PathEnd({self.placement}, {self.offset}, is_dead_end={self.is_dead_end})"

    @classmethod
    def from_text(cls, text: str):
        """
        Create a path end by parsing the given text.

        :param text: The text to parse.
        :return: A new path end.
        """
        offset = RoomOffset()
        elements = text.split("/")
        is_dead_end = False
        if not elements:
            raise ValueError("You must specify at least the placement.")
        placement = Placement.from_text(elements.pop(0))
        if elements:
            offset = RoomOffset.from_text(elements.pop(0))
            if elements:
                flags_text = elements.pop(0).lower()
                if flags_text == "x":
                    is_dead_end = True
                else:
                    raise ValueError("The third parameter must be 'x' for a dead-end or omitted.")
                if elements:
                    raise ValueError("There are too many parameters.")
            if placement == Placement.RANDOM and not offset.is_zero:
                raise ValueError("You must not set an offset for a random placement.")
        return cls(placement, offset, is_dead_end, text)
