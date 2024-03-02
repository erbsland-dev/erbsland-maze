#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from .modifier import Modifier
from .modifiers import Modifiers
from .path_end import PathEnd
from .placement import Placement


class GeneratorSetup:
    def __init__(
        self,
        path_ends: list[PathEnd] = None,
        modifiers: list[Modifier] = None,
        allow_islands: bool = True,
        maximum_attempts: int = 20,
        verbose: bool = True,
        ignore_errors: bool = False,
    ):
        """
        Create the setup for the maze generator.

        :param path_ends: A list of path ends.
        :param modifiers: A list of modifiers to apply to the maze.
        :param allow_islands: If islands (isolated areas) are allowed. If this is the case, these areas are filled
            with decoy paths to create a consistent look for the maze.
        :param maximum_attempts: The maximum number of attempts to find a solution for the maze before giving up.
        :param verbose: Display status information on the console.
        :param ignore_errors: Ignore errors, and produce invalid/incomplete solutions for debugging.
        """
        if path_ends:
            if not isinstance(path_ends, list):
                raise TypeError("path_ends must be a list of PathEnd objects.")
            for path_end in path_ends:
                if not isinstance(path_end, PathEnd):
                    raise TypeError("path_ends must be a list of PathEnd objects.")
        if modifiers:
            if not isinstance(modifiers, list):
                raise TypeError("modifiers must be a list of Modifiers objects.")
            for modifier in modifiers:
                if not isinstance(modifier, Modifier):
                    raise TypeError("modifiers must be a list of Modifiers objects.")
        if not isinstance(allow_islands, bool):
            raise TypeError("allow_islands must be a bool")
        if not isinstance(maximum_attempts, int):
            raise TypeError("maximum_attempts must be an integer.")
        if maximum_attempts < 1 or maximum_attempts > 10_000:
            raise TypeError("maximum_attempts must is outside of a valid range of 1 to 10'000.")
        if path_ends:
            if len(path_ends) < 2:
                raise ValueError("You must provide at least two path ends.")
            self.path_ends = path_ends
        else:
            self.path_ends = [PathEnd(Placement.LEFT), PathEnd(Placement.RIGHT)]
        self.modifiers: Modifiers = Modifiers(modifiers)
        self.allow_islands: bool = allow_islands
        self.maximum_attempts: int = maximum_attempts
        self.verbose: bool = verbose
        self.ignore_errors: bool = ignore_errors
