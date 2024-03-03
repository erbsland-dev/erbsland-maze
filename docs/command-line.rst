
Command Line Options
====================

.. program:: generate-maze.py

.. option:: -h, --help

    Displays a help page with summaries of all command line options.

.. option:: -x <dimension>, --width <dimension>

    This option is required. It sets the width of the created maze in mm.

.. option:: -y <dimension>, --height <dimension>

    This option is required. It sets the height of the created maze in mm.

.. option:: -t <dimension>, --thickness <dimension>

    This option sets the thickness of the maze walls in mm. If you omit this option, the default of 1.7 mm is used.

.. option:: -l <dimension>, --length <dimension>

    This option sets the side length of a room in mm including the wall thickness. If you omit this option, the default of 4 mm is used.

    If the specified width and height of the maze do not align with the length of specify using this option, the outer rooms will be slightly stretched to completely fill the whole area.

.. option:: -o <path>, --output <path>

    Use this option to change the output filename or path of the generated SVG file. If you omit this value, the default ``output.svg`` is used. The path can be relative or absolute.

.. option:: --no-marks

    If specify this flag, the path ends will not get marked with a coloured rectangle. This is especially useful for automated workflows.

.. option:: --svg-unit {mm,px}

    Use this option to change the unit that is used in the SVG file. If you omit this value, the default unit ``mm`` is used.

    Setting the SVG unit to ``px`` does not change the units you specify with the width, height or room length. These are always specified in mm. This is just the unit of the created SVG file.

.. option:: --svg-dpi <dpi>

    Specify this option to change the DPI value that is used when converting the mm values into pixels. If you omit this option, the default of 96 DPI is used. The DPI value must be between 60 and 10'000.

.. option:: --svg-zero-point {center,top_left}

    Use this option to change the zero point of the creates SVG file. If you omit this option, the default ``center`` is used.

    - ``center``: This places the zero point, which is always the middle of the maze into the middle of the canvas. Therefore all points in the SVG file are positive values starting from the zero point in the top left corner of the document.
    - ``top_left``: This places the zero point to the top left corner of the document. While this is not displayed correctly, it is useful for further workflows that require the center of the maze at the zero point of the document.

.. option:: -e END_POINT, --end-point END_POINT

    Use this command line option to specify two or more end points in the format ``<placement>[/<offset>[/x]]``. If you set no end point option, as default an end point on the left and right side is added.

    The :ref:`param-placement` is required and controls the overall location of the end point. You can also use the ``random`` placement for end-points, even it makes not much sense.

    Optionally, seperated with a slash ``/`` character, you can specify an :ref:`param-offset`.

    And finally, separated with another slash ``/`` character, you can turn the end into a dead-end by adding an ``x`` character.

    It is also important to note, that end points overwrite blank rooms. For example if your maze has a frame of empty rooms and you place your end-point in this frame, the room of the end-point will be turned back into a regular room.

    The following example creates a maze with a frame of black rooms with a path from the top to the center.

    .. code-block:: console

        generate_maze.py -x 50 -y 50 -f 1 -e top -e center/0,1

    .. figure:: /images/example_end_point.svg
        :width: 50%

    The next example adds three dead-ends to the maze. Only one path leads from the side to the center.

    .. code-block:: console

        generate_maze.py -x 50 -y 50 -f 1 -e w -e c -e n/0/x -e e/0/x -e s/0/x -m c/3

    .. figure:: /images/example_dead_end.svg
        :width: 50%

.. option:: --width-parity {none,odd,even}

    The parity for the room count for the width of the maze.

.. option:: --height-parity {none,odd,even}

    The parity for the room count for the height of the maze.

.. option:: -m <merge definition>, --add-merge <merge definition>

    Add a merge modifier to alter the maze. The parameter has the format: ``<placement>[[/<size>]/<offset>]``

.. option:: -f <frame definition>, --add-frame <frame definition>

    Add a frame modifier to alter the maze. The parameter has the format: ``<insets>``

.. option:: -b <blank definition>, --add-blank <blank definition>

    Add a blank modifier to alter the maze. The parameter has the format: ``<placement>[[/<size>]/<offset>]``

.. option:: -c <closing definition>, --add-closing <closing definition>

    Add a closing modifier to alter the maze. The parameter has the format: ``[^]<closing>/<placement>[[/<size>]/<offset>]``

.. option:: --silent

    Do not print progress messages on the console.

.. option:: --ignore-errors

    Try to ignore all errors and produce an output anyway for debugging purposes.


.. _param-placement:

Placement Parameter
-------------------

Placements play an important role when you customize your maze. Instead of relying to absolute coordinates that you must adjust every time you resize the maze, placements let you specify one of nine points in the maze and add an offset from there.

Any :ref:`param-offset` and :ref:`param-size` automatically adjust to the placement direction, which simplifies the customization of the maze.

.. note::

    There is also ``random`` which puts the element to a random position. Be aware that random placements may lead to conflicts and overlapping, so generating a maze will require several attempts until a good arrangement for a valid maze is found.

.. list-table::
    :header-rows: 1
    :widths: 25, 75
    :width: 100%

    *   -   Parameter
        -   Meaning
    *   -   ``left``, ``w``
        -   Placed in the middle of the left edge.
    *   -   ``top_left``, ``nw``
        -   Placed in the top left corner of the maze.
    *   -   ``top``, ``n``
        -   Placed in the middle of the top edge.
    *   -   ``top_right``, ``ne``
        -   Placed in the top right corner.
    *   -   ``right``, ``e``
        -   Placed in the middle of the right edge.
    *   -   ``bottom_right``, ``se``
        -   Placed at the bottom right corner.
    *   -   ``bottom``, ``s``
        -   Placed in the middle the the bottom edge.
    *   -   ``bottom_left``, ``sw``
        -   Placed in the bottom left corner.
    *   -   ``center``, ``c``
        -   Placed in the center of the maze.
    *   -   ``random``, ``r``
        -   Placed at a random position.

.. _param-size:

Size Parameter
--------------

The size parameter can be specified either as a single positive number value, like ``3``, or as two numbers separated with an ``x`` character, like ``3x2``.

If only one value is specified, this value sets the width and height of the area.

With two values, the first specifies the width, the second the height of the area. Beside the numbers, there are also a few predefined names you can use to specify a size.

.. list-table::
    :header-rows: 1
    :widths: 25, 75
    :width: 100%

    *   -   Parameter
        -   Meaning
    *   -   ``single``
        -   An area of the size 1×1 rooms.
    *   -   ``small``
        -   An area of the size 2×2 rooms.
    *   -   ``medium``
        -   An area of the size 3×3 rooms.
    *   -   ``large``
        -   An area of the size 4×4 rooms.
    *   -   One number: ``5``
        -   An area of the size 5×5 rooms.
    *   -   Two numbers: ``2x4``
        -   An area of the size 2×4 rooms.


.. _param-offset:

Offset Parameter
----------------

The offset parameter can either be specified as a single number, like ``3``, or as two numbers separated with a comma, like ``-4,2``. Positive and negative numbers, and also zero are allowed.

If you specify a single number, the offset is diagonally towards the center of the maze. It depends on the placement of the modifier. If you place a blank in the bottom right corner, a positive single number offset moves it diagonally up and left towards the center.

Two numbers specify an offset that is independent from the placement. The first number specified the offset in the X-axis and the second number the offset in the Y-axis.

.. list-table::
    :header-rows: 1
    :widths: 25, 75
    :width: 100%

    *   -   Parameter
        -   Meaning
    *   -   One number: ``5``
        -   An offset diagonally towards the center.
    *   -   Two numbers: ``2,-4``
        -   An independent offset to the X and Y-axis.

.. _param-closing:

Closing Parameter
-----------------

The closing parameter specifies which connection between rooms shall be permanently blocked for the algorithm. By prefixing the name with a ``^`` character, the selection is inverted.

For example ``corner_paths`` blocks all paths at the corner of the specified area, but ``^corner_paths`` only allows connections at the corners and blocks every other connection.

.. list-table::
    :header-rows: 1
    :widths: 35, 65
    :width: 100%

    *   -   Parameter
        -   Meaning
    *   -   ``corner_paths``, ``c``
        -   Connections at all four corners of the area.
    *   -   ``corner_top_left``, ``cnw``
        -   The connection at this corner.
    *   -   ``corner_top_right``, ``cne``
        -   The connection at this corner.
    *   -   ``corner_bottom_right``, ``cse``
        -   The connection at this corner.
    *   -   ``corner_bottom_left``, ``csw``
        -   The connection at this corner.
    *   -   ``direction_west``, ``dw``
        -   All connections pointing to the west from the specified area.
    *   -   ``direction_north``, ``dn``
        -   All connections pointing to the north from the specified area.
    *   -   ``direction_east``, ``de``
        -   All connections pointing to the east from the specified area.
    *   -   ``direction_south``, ``ds``
        -   All connections pointing to the south from the specified area.
    *   -   ``direction_horizontal``, ``dh``
        -   All connections running horizontally in specified area.
    *   -   ``direction_vertical``, ``dv``
        -   All connections running vertically in the specified area.
    *   -   ``middle_paths``, ``m``
        -   All connections that enter or leave at the middle of the four sides of the area.
    *   -   ``middle_west``, ``mw``
        -   The connection at the middle of the specified side.
    *   -   ``middle_north``, ``mn``
        -   The connection at the middle of the specified side.
    *   -   ``middle_east``, ``me``
        -   The connection at the middle of the specified side.
    *   -   ``middle_south``, ``ms``
        -   The connection at the middle of the specified side.

.. _param-insets:

Insets Parameter
----------------

For the insets parameter, specify one to four positive numbers, seperated by a comma. One number is applied to all four sides. For two numbers, the first is applied to the top and bottom sides, and the second to the left and right side. For three or four numbers, they define the frame size in the following order:
top, right, bottom, left.

