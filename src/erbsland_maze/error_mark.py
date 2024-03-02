#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass

from .room_location import RoomLocation
from .room_size import RoomSize


@dataclass(frozen=True)
class ErrorMark:
    """
    An error marked in the maze.
    """

    location: RoomLocation
    size: RoomSize = None
    message: str = None
