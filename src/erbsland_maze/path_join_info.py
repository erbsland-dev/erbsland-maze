#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .path_pair import PathPair


@dataclass(frozen=True)
class PathJoinInfo:
    """
    Information about a potential point where two path can be joined.
    """

    paths: PathPair
    """Which paths identifiers are connected."""

    total_length: int
    """Total length of the path at this point."""

    connection: "RoomConnection"
    """The connection between the rooms at this point."""
