#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import enum


class Parity(enum.StrEnum):
    """
    Requesting a parity of a number of elements.
    """

    NONE = "none"
    """No parity requested."""

    ODD = "odd"
    """Odd parity requested."""

    EVEN = "even"
    """Even parity requested."""
