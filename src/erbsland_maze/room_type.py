#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import enum


class RoomType(enum.Enum):
    """
    The type of room.
    """

    PATH = enum.auto()
    """A path through the maze."""

    BLANK = enum.auto()
    """A blank spot in the maze."""

    END = enum.auto()
    """A path end."""
