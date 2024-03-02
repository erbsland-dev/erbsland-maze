#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Self

from .modifier import Modifier
from .modifier_type import ModifierType
from .placement import Placement
from .room_offset import RoomOffset
from .room_size import RoomSize


class BlankModifier(Modifier):
    """
    A modifier to create blank areas in the maze.
    """

    def __init__(
        self, placement: Placement, size: RoomSize = RoomSize(1, 1), offset: RoomOffset = RoomOffset(), name: str = None
    ):
        super().__init__(modifier_type=ModifierType.BLANK, placement=placement, size=size, offset=offset, name=name)

    @classmethod
    def from_text(cls, text: str) -> Self:
        size = RoomSize(1, 1)
        offset = RoomOffset()
        elements = text.split("/")
        if not elements:
            raise ValueError("You must specify at least the placement parameter.")
        placement = Placement.from_text(elements.pop(0))
        if elements:
            size = RoomSize.from_text(elements.pop(0))
            if elements:
                offset = RoomOffset.from_text(elements.pop(0))
                if elements:
                    raise ValueError("There are too many parameters.")
        if placement == Placement.RANDOM and not offset.is_zero:
            raise ValueError("You must not set an offset for a random placement.")
        return cls(placement, size, offset, name=text)
