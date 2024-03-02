#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from abc import ABC, abstractmethod
from typing import Self

from .closing import Closing
from .modifier_type import ModifierType
from .placement import Placement
from .room_insets import RoomInsets
from .room_offset import RoomOffset
from .room_size import RoomSize


class Modifier(ABC):
    """
    The base class of all modifiers to style the maze in custom ways.

    Do not use this class directly. Use the derived classes instead.
    """

    def __init__(
        self,
        modifier_type: ModifierType,
        placement: Placement = None,
        size: RoomSize = None,
        insets: RoomInsets = None,
        offset: RoomOffset = None,
        closing: Closing = None,
        name: str = None,
    ):
        if not isinstance(modifier_type, ModifierType):
            raise TypeError("`modifier_type` must be an instance of `ModifierType`.")
        if placement and not isinstance(placement, Placement):
            raise TypeError("`placement` must be an instance of `Placement`.")
        if size and not isinstance(size, RoomSize):
            raise TypeError("`size` must be an instance of `RoomSize`.")
        if insets and not isinstance(insets, RoomInsets):
            raise TypeError("`insets` must be an instance of `RoomInsets`.")
        if offset and not isinstance(offset, RoomOffset):
            raise TypeError("`offset` must be an instance of `RoomOffset`.")
        if closing and not isinstance(closing, Closing):
            raise TypeError("`closing` must be an instance of `Closing`.")
        if name and not isinstance(name, str):
            raise TypeError("`name` must be a string.")
        self._modifier_type: ModifierType = modifier_type
        self._placement: Placement = placement
        self._size: RoomSize = size
        self._insets: RoomInsets = insets
        self._offset: RoomOffset = offset
        self._closing: Closing = closing
        if name:
            self._name = name
        else:
            self._name = self.__str__()

    def __str__(self) -> str:
        result = [f"{self._modifier_type.value}"]
        if self._closing:
            result.append(f"{self._closing}")
        if self._placement:
            result.append(f"{self._placement.value}")
        if self._size:
            result.append(f"{self._size}")
        elif self._insets:
            result.append(f"{self._insets}")
        if self._offset:
            result.append(f"{self._offset}")
        return ";".join(result)

    @property
    def modifier_type(self) -> ModifierType:
        return self._modifier_type

    @property
    def placement(self) -> Placement:
        return self._placement

    @property
    def size(self) -> RoomSize:
        return self._size

    @property
    def insets(self) -> RoomInsets:
        return self._insets

    @property
    def offset(self) -> RoomOffset:
        return self._offset

    @property
    def closing(self) -> Closing:
        return self._closing

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    @abstractmethod
    def from_text(cls, text: str) -> Self:
        """
        Create a modifier from a string.

        :param text: The text that will be parsed.
        :return: The modifier object.
        """
        pass
