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

To use Erbsland Maze, you'll need:

- Python 3.12 or higher.
- The `pycairo` library for rendering SVG files.

Quickstart Guide
----------------

Follow these steps to get started with Erbsland Maze:

#.  Clone the repository and navigate into it:

    .. code-block:: console

        git clone https://github.com/erbsland-dev/erbsland-maze/
        cd erbsland-maze

#.  Create and activate a new Python virtual environment:

    .. code-block:: console

        python3.12 -m venv venv
        source venv/bin/activate

#.  Install `pycairo`:

    .. code-block:: console

        pip install pycairo

#.  Generate your first maze:

    .. code-block:: console

        cd src
        python generate_maze.py -x 100 -y 100 -o maze.svg

    This command creates a `maze.svg` file in the `src` directory with your newly generated maze.

#.  For additional command-line options and configurations:

    .. code-block:: console

        python generate_maze.py --help

Reference Documentation
-----------------------

.. toctree::
    :maxdepth: 2
    :caption: Reference

    command-line
    examples
    generate-via-api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

