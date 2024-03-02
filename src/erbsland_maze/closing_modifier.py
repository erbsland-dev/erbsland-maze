#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Self

from .closing import Closing
from .modifier import Modifier
from .modifier_type import ModifierType
from .placement import Placement
from .room_offset import RoomOffset
from .room_size import RoomSize


class ClosingModifier(Modifier):
    """
    A modifier to close paths in the maze.
    """

    def __init__(
        self,
        closing: Closing,
        placement: Placement,
        size: RoomSize = RoomSize(1, 1),
        offset: RoomOffset = RoomOffset(),
        name: str = None,
    ):
        super().__init__(
            modifier_type=ModifierType.CLOSING,
            closing=closing,
            placement=placement,
            size=size,
            offset=offset,
            name=name,
        )

    @classmethod
    def from_text(cls, text: str) -> Self:
        size = RoomSize(1, 1)
        offset = RoomOffset()
        elements = text.split("/")
        if len(elements) < 2:
            raise ValueError("You must specify at least the closing type and placement parameter.")
        closing = Closing.from_text(elements.pop(0))
        placement = Placement.from_text(elements.pop(0))
        if placement == Placement.RANDOM:
            raise ValueError("Closings must not be randomly placed.")
        if elements:
            size = RoomSize.from_text(elements.pop(0))
            if elements:
                offset = RoomOffset.from_text(elements.pop(0))
                if elements:
                    raise ValueError("There are too many parameters.")
        return cls(closing, placement, size, offset, name=text)
