#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later


class PathPair:
    """
    A pair of path identifiers that can be used as a key.
    """

    def __init__(self, a: int, b: int):
        if a < 1 or b < 1 or a == b:
            raise ValueError("Invalid paths.")
        self._a = min(a, b)
        self._b = max(a, b)

    def __hash__(self) -> int:
        return hash((self._a, self._b))

    def __eq__(self, other: "PathPair") -> bool:
        return self._a == other._a and self._b == other._b

    def __str__(self) -> str:
        return f"{self.a}-{self.b}"

    def __repr__(self) -> str:
        return f"PathPair({self.a}, {self.b})"

    @property
    def a(self) -> int:
        return self._a

    @property
    def b(self) -> int:
        return self._b
