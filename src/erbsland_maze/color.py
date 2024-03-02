#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass


@dataclass
class Color:

    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 1.0
