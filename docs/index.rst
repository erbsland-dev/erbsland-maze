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

#.  Install the package from the PyPI:

    .. code-block:: console

        pip install erbsland-maze

#.  Generate your first maze:

    .. code-block:: console

        elmaze -x 100 -y 100 -o maze.svg

    This command creates a `maze.svg` file in the current directory with your newly generated maze.

#.  For additional command-line options and configurations:

    .. code-block:: console

        elmaze --help

Reference Documentation
-----------------------

.. toctree::
    :maxdepth: 2
    :caption: Reference

    command-line
    examples
    generate-via-api
    changelog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
