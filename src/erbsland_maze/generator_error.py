#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later


class GeneratorError(Exception):
    """
    An error occurred while generating the maze.
    """

    pass


class NoValidSolutionError(GeneratorError):
    """
    There was no valid solution to generate the maze as specified.
    """

    pass
