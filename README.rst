Welcome to Erbsland Maze
========================

Erbsland Maze is a sophisticated, open-source maze generator designed for creating complex, rectangular mazes. It exports mazes as SVG files, making them perfect for graphic design applications or even for 3D modeling. This tool stands out for its customization capabilities; it supports various endpoint configurations, allowing for connected or dead-end designs.

Features
--------

- **Modular and Flexible**: Tailor your maze to fit any project requirement, from simple puzzles to complex labyrinth designs.
- **Customizable Endpoints**: Specify any number of endpoints, deciding whether they're interconnected or serve as individual dead-ends.
- **Design Freedom**: Freely position endpoints, incorporate blank areas for shaping the maze, and merge smaller rooms into larger spaces for aesthetic or functional purposes.
- **Path Customization**: Adjust room connections to guide the maze's pathways or to craft a unique template for your designs.

Requirements
------------

- Python 3.12
- The *pycairo* library.

## Requirements

To use Erbsland Maze, you'll need:

- Python 3.12 or higher.
- The `pycairo` library for rendering SVG files.

Quickstart Guide
----------------

Follow these steps to get started with Erbsland Maze:

1.  Clone the repository and navigate into it:

    .. code-block:: console
        git clone https://erbsland-dev.github.io/erbsland-maze/
        cd erbsland-maze

2.  Create and activate a new Python virtual environment:

    .. code-block:: console
        python3.12 -m venv venv
        source venv/bin/activate

3.  Install `pycairo`:

    .. code-block:: console
        pip install pycairo

4.  Generate your first maze:

    .. code-block:: console
        cd src
        python generate_maze.py -x 100 -y 100 -o maze.svg

    This command creates a `maze.svg` file in the `src` directory with your newly generated maze.

5.  For additional command-line options and configurations:

    .. code-block:: console
        python generate_maze.py --help

Documentation
-------------

You find all details about the library, it's design and file format in the `documentation`_.


License
-------

Copyright © 2003-2024 Tobias Erbsland https://erbsland.dev/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


.. _`documentation`: https://erbsland-dev.github.io/erbsland-maze/


