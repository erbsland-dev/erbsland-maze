#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol


class GenericLine(Protocol):

    @property
    def first(self) -> "Point":
        """
        The first point of the line.
        """
        ...

    @property
    def last(self) -> "Point":
        """
        The last point of the line.
        """
        ...

    @property
    def points(self) -> list["Point"]:
        """
        All points of the line.
        """
        ...
