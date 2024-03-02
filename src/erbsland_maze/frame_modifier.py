#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Self

from .modifier import Modifier
from .modifier_type import ModifierType
from .room_insets import RoomInsets


class FrameModifier(Modifier):
    """
    A modifier to create a frame of blank rooms around the maze.
    """

    def __init__(self, insets: RoomInsets = RoomInsets(1, 1, 1, 1), name: str = None):
        super().__init__(modifier_type=ModifierType.FRAME, insets=insets, name=name)

    @classmethod
    def from_text(cls, text: str) -> Self:
        insets = RoomInsets.from_text(text)
        return cls(insets, name=text)
