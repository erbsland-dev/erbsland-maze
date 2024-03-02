#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later


class ModifierError(Exception):
    """
    An exception raised when the origin of the problem is based on a modifier.
    """

    def __init__(self, modifier: "Modifier", message: str):
        super().__init__(message)
        self.modifier = modifier
