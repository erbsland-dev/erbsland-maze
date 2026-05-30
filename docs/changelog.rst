*********
Changelog
*********

Release 1.4 - 30-05-2026
========================

Release 1.4 modernizes the project infrastructure while keeping the maze generator API and generation behavior fully compatible with previous releases.

User-Facing Changes
-------------------

* Added the new ``elmaze`` command-line tool. After installation, you can generate mazes directly from the command line:

  .. code-block:: console

      elmaze -x 100 -y 100 -o maze.svg

* The package is distributed under the canonical name ``erbsland-maze``, the Python import remains unchanged:

  .. code-block:: python

      import erbsland_maze

* Updated the documentation to focus on installation with ``pip`` and usage of the ``elmaze`` command.
* Added this changelog to the documentation.

Quality Improvements
--------------------

* Added a comprehensive automated test suite covering maze generation, SVG output, parser behavior and command-line usage.
* Improved packaging, release automation, documentation builds and project maintenance tooling.
* Enhanced CI/CD workflows, security checks and release validation.
