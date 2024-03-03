#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Size:
    """
    A graphical size.
    """

    width: float
    height: float

    def __repr__(self):
        return f"Size({self.width:0.2f},{self.height:0.2f})"
