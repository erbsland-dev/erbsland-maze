#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .wall import Wall


@dataclass
class ConnectionSide:
    """
    Represents the end or side of a connection.
    """

    room: "Room"
    wall: Wall
