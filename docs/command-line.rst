
.. _command-line:

Command Line Options
====================

.. program:: generate_maze.py

This chapter provides a comprehensive overview of the command-line options available for the ``generate_maze.py`` tool. To utilize the tool, execute the following command:

.. code-block:: console

    python generate_maze.py -x 160 -y 160 -f 1 -o demo.svg

Adjusting the Maze Dimensions
-----------------------------

To customize the dimensions of your maze, utilize the following command-line options. These settings define the overall size and structure of the maze, influencing the generated SVG file.

.. option:: -x <dimension>, --width <dimension>

    This mandatory option specifies the width of the maze in millimeters (mm). The width impacts the final dimensions of the generated SVG file. When used alongside the :option:`--length` option, the application calculates the optimal number of rooms along the X axis.

    .. code-block:: console

        generate_maze.py -x 55 -y 35 -l 5

    .. figure:: /images/example_cmd_width.svg
        :width: 275px

.. option:: -y <dimension>, --height <dimension>

    This required option sets the height of the maze in millimeters (mm). Similar to width, height determines the dimensions of the resulting SVG file. In combination with the :option:`--length` option, it helps in determining the ideal number of rooms along the Y axis.

    .. code-block:: console

        generate_maze.py -x 20 -y 44 -l 4 -f 0,1

    .. figure:: /images/example_cmd_height.svg
        :width: 100px

.. option:: -t <dimension>, --thickness <dimension>

    Define the thickness of the maze's walls with this option, measured in millimeters (mm). If not specified, a default thickness of 1.7 mm is applied.

    .. code-block:: console

        generate_maze.py -x 55 -y 55 -l 5 -t 3

    .. figure:: /images/example_cmd_thickness_1.svg
        :width: 275px

    .. code-block:: console

        generate_maze.py -x 55 -y 55 -l 5 -t 0.4 -f 1

    .. figure:: /images/example_cmd_thickness_2.svg
        :width: 275px

.. option:: -l <dimension>, --length <dimension>

    This parameter establishes the side length of each room within the maze, including wall thickness, measured in millimeters (mm). The default value is 4 mm, applied when this option is not explicitly set.

    .. code-block:: console

        generate_maze.py -x 42 -y 42 -l 6

    .. figure:: /images/example_cmd_length_1.svg
        :width: 210px

    .. code-block:: console

        generate_maze.py -x 42 -y 42 -l 4

    .. figure:: /images/example_cmd_length_2.svg
        :width: 210px

    .. note::

        If the maze's specified width and height do not proportionately match the room length set by this option, by default, the outer rooms will be adjusted in size to ensure the entire area is filled. To change this behaviour, see :option:`--fill-mode`.

    .. code-block:: console

        generate_maze.py -x 42 -y 40 -l 5

    .. figure:: /images/example_cmd_length_3.svg
        :width: 210px

.. option:: -i <fill mode>, --fill-mode <fill mode>

    This parameters controls how the rooms are distributed in the canvas defined with :option:`--width` and :option:`--height`. There are several fill modes available, explained in the following table:

    .. list-table::
        :header-rows: 1
        :widths: 25, 55, 20
        :width: 100%

        *   -   Parameter
            -   Meaning
            -   Example
        *   -   ``stretch_edge``, ``se``
            -   Calculate the best square room size from the side lengths and parity and stretch the rooms at the edges to completely fill the specified width and height.
            -   .. image:: /images/example_cmd_fill_mode_1.svg
                    :width: 100px
        *   -   ``stretch``, ``s``
            -   Stretch the rooms into rectangles that completely fill the specified width and height.
            -   .. image:: /images/example_cmd_fill_mode_2.svg
                    :width: 100px
        *   -   ``square_top_left``, ``qt``
            -   Use a square room size that fills at least one dimension perfectly, and align the maze at the top left corner. If the room size doesn't divide the with and height evenly, there will be a gap at the bottom or right side.
            -   .. image:: /images/example_cmd_fill_mode_3.svg
                    :width: 100px
        *   -   ``square_center``, ``q``
            -   Use a square room size that fills at least one dimension perfectly, and align the maze at the top left corner. If the room size doesn't divide the with and height evenly, there will be a gap around the maze.
            -   .. image:: /images/example_cmd_fill_mode_4.svg
                    :width: 100px
        *   -   ``fixed_top_left``, ``ft``
            -   Use a square room size with the exact side length as configured and place the maze in the top left corner. If the room size doesn't divide the with and height evenly, there will be a gap at the bottom or right side.
            -   .. image:: /images/example_cmd_fill_mode_5.svg
                    :width: 100px
        *   -   ``fixed_center``, ``f``
            -   Use a square room size with the exact side length as configured and place the maze in the center. If the room size doesn't divide the with and height evenly, there will be a gap around the maze.
            -   .. image:: /images/example_cmd_fill_mode_6.svg
                    :width: 100px


.. option:: --width-parity {none,odd,even}

    This option allows you to determine the parity (odd or even) of the room count along the X axis. If not specified, the default setting is ``odd``.

    .. list-table::
        :header-rows: 1
        :widths: 25, 75
        :width: 100%

        *   -   Parameter
            -   Meaning
        *   -   ``odd``
            -   Enforce a odd number of rooms along the X axis.
        *   -   ``even``
            -   Enforce an even number of rooms along the X axis.
        *   -   ``none``
            -   Do not set any preference, the room count may be odd or even.

    .. code-block:: console

        generate_maze.py -x 30 -y 30 -l 5 -e nw -e se --width-parity=even --height-parity=even

    .. figure:: /images/example_cmd_parity_1.svg
        :width: 150px

    .. code-block:: console

        generate_maze.py -x 30 -y 30 -l 5 -e nw -e se --width-parity=odd --height-parity=even

    .. figure:: /images/example_cmd_parity_2.svg
        :width: 150px

    .. code-block:: console

        generate_maze.py -x 30 -y 30 -l 5 -e nw -e se --width-parity=none --height-parity=even

    .. figure:: /images/example_cmd_parity_3.svg
        :width: 150px

.. option:: --height-parity {none,odd,even}

    Similarly, this option lets you set the parity (odd or even) of the room count along the Y axis, with a default setting of ``odd`` if not specified.

    .. list-table::
        :header-rows: 1
        :widths: 25, 75
        :width: 100%

        *   -   Parameter
            -   Meaning
        *   -   ``odd``
            -   Enforce a odd number of rooms along the Y axis.
        *   -   ``even``
            -   Enforce an even number of rooms along the Y axis.
        *   -   ``none``
            -   Do not set any preference, the room count may be odd or even.

    .. code-block:: console

        generate_maze.py -x 30 -y 30 -l 5 -e nw -e se --width-parity=even --height-parity=odd

    .. figure:: /images/example_cmd_parity_4.svg
        :width: 150px

Configuring the End Points
--------------------------

The end points of your maze can be customized using the following command-line option. This feature allows you to define the start and finish points, or any specific points of interest within your maze.

.. option:: -e <end point definition>, --end-point <end point definition>

    Specify one or more end points using the format ``<placement>[/<offset>[/x]]``. By default, if no end points are specified, the tool automatically adds an end point on both the left and right sides of the maze.

    The :ref:`placement parameter<param-placement>` defines the location of the end point and is mandatory. For dynamic maze designs, a ``random`` placement option is available, although its practicality may vary.

    Optionally, you can specify an :ref:`offset parameter<param-offset>`, separated by a slash ``/``. This allows for more precise placement of the end points within the maze's structure.

    To designate an end point as a dead-end, append an ``x`` after another slash ``/``. This feature enables the creation of more complex maze layouts.

    It's important to note that specifying an end point will overwrite any blank (empty) rooms in the specified location. If an end point is placed within a frame of empty rooms, that room will be converted into a standard maze room.

    For example, to create a maze with a frame of blank rooms and a path leading from the top to the center, use the following command:

    .. code-block:: console

        generate_maze.py -x 50 -y 50 -f 1 -e top -e center/0,1

    .. figure:: /images/example_end_point.svg
        :width: 250px

    The example below demonstrates how to add three dead-ends to a maze, with only one path leading from the edge to the center:

    .. code-block:: console

        generate_maze.py -x 50 -y 50 -f 1 -e w -e c -e n/0/x -e e/0/x -e s/0/x -m c/3

    .. figure:: /images/example_dead_end.svg
        :width: 250px

Changing the Layout of the Maze
-------------------------------

To fine-tune the maze's layout before generating paths, you can use a series of modifier options. These modifiers are applied sequentially to achieve the desired layout effect: initially, 'blank' modifiers eliminate specific rooms; subsequently, connections are removed using 'closing' modifiers; and finally, rooms are merged to complete the layout adjustment.

The application of modifiers follows a specific sequence based on their placement within the maze. Modifiers designated for the center are applied first, followed by those at the corners, and lastly, any random modifiers are applied. This ordered approach is designed to minimize unintended consequences, particularly from random modifications.

Adding a Frame of Blank Rooms Around the Maze
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. option:: -f <frame definition>, --add-frame <frame definition>

    Use this option to add a surrounding frame of blank rooms to the maze. The thickness of the frame on each side is determined by the :ref:`insets parameter<param-insets>`.

    .. warning::

        End points completely encased in blank spaces can block all potential solutions. If the frame extends two or more rooms thick, ensure that end points either have larger merged rooms or are positioned to directly connect to an adjacent room, maintaining at least one open side.

    To add a single-room thick frame around a maze, you can use the following command:

    .. code-block:: console

        generate_maze.py -x 55 -y 55 -f 1

    .. figure:: /images/example_cmd_frame_1.svg
        :width: 275px

    In a more complex scenario, adding a two-room thick frame with even width and height parity, while merging rooms at strategic locations, can be achieved as shown below:

    .. code-block:: console

        generate_maze.py -x 80 -y 80 --width-parity=even --height-parity=even -f 2 -m nw/3 -m ne/3 -m se/3 -m sw/3 -m w/2/1 -m n/2/1 -m e/2/1 -m s/2/1 -m c/4 -e nw/0/x -e ne/0 -e sw/0/x -e se/0/x -e c

    .. figure:: /images/example_cmd_frame_2.svg
        :width: 400px

Adding Blank Space to the Maze
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Introducing blank spaces into your maze layout effectively removes rooms along with their connections in the specified areas. This feature can be particularly useful for embedding logos, text, or for sculpting the rectangular maze into more dynamic shapes.

Although there's no limit to the number of blank spaces you can add, it's crucial to maintain a viable path of rooms connecting all non-dead-end end points.

.. option:: -b <blank definition>, --add-blank <blank definition>

   This option allows you to add designated blank spaces within the maze. The syntax for this argument is: ``<placement>[/<size>[/<offset>]]``

   The :ref:`placement parameter<param-placement>` is mandatory and may be followed by an optional :ref:`size parameter<param-size>` and an :ref:`offset parameter<param-offset>`, each separated by a slash ``/``.

   .. note::

       Don't worry about overlapping blank spaces; since rooms are simply marked as blank and removed at the final stage of layout preparation, overlaps do not pose any problem.

   For example, to add a central blank space with a size of 7, use the following command:

   .. code-block:: console

       generate_maze.py -x 60 -y 60 -b c/7

   .. figure:: /images/example_cmd_blank_1.svg
       :width: 300px

   To create a layout with blank spaces at each corner of the maze, each with a size of 5, the command would be:

   .. code-block:: console

       generate_maze.py -x 60 -y 60 -b nw/5 -b ne/5 -b se/5 -b sw/5

   .. figure:: /images/example_cmd_blank_2.svg
       :width: 300px

   And to demonstrate a more randomized approach with multiple blank spaces of varying sizes placed randomly, consider this command:

   .. code-block:: console

       generate_maze.py -x 60 -y 60 -b r/3 -b r/3 -b r/3 -b r/2 -b r/2

   .. figure:: /images/example_cmd_blank_3.svg
       :width: 300px

Closing Connections between Rooms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Modifying the maze by closing connections between rooms can significantly influence the shape of the maze and the algorithm's path generation. This technique is especially useful for designing mazes with specific configurations or when you need to control exit points from merged rooms.

To illustrate the impact of closing connections, consider the following example, which closes all vertical connections in the center area, leaving only horizontal paths:

.. code-block:: console

   generate_maze.py -x 60 -y 60 -c dv/c/5x15 -t 3 --layout-only

.. figure:: /images/example_cmd_close_1.svg
    :width: 300px

Rerunning the command without the :option:`--layout-only` option showcases the final maze design:

.. code-block:: console

   generate_maze.py -x 60 -y 60 -c dv/c/5x15 -t 3

.. figure:: /images/example_cmd_close_2.svg
    :width: 300px

.. option:: -c <closing definition>, --add-closing <closing definition>

    Before running the maze generation algorithm, you can close specific connections within the maze using this option. The format for this argument is: ``[^]<closing>/<placement>[/<size>[/<offset>]]``

    The argument begins with the mandatory :ref:`closing parameter<param-closing>` and :ref:`placement parameter<param-placement>`, separated by a slash ``/``. Optionally, a :ref:`size parameter<param-size>` and an :ref:`offset parameter<param-offset>` may follow.

    For a more complex configuration, creating a unique pattern with closed connections and blank spaces can be achieved as shown:

    .. code-block:: console

       generate_maze.py -x 80 -y 80 -c dh/w/4x17 -c dv/n/17x4 -c dh/e/4x17 -c dv/s/17x4 -b c/17 -e c/-8,0 -e c/8,0 -t 0.3 -l 3

    .. figure:: /images/example_cmd_close_3.svg
        :width: 400px

    Another example demonstrates the addition of closed connections to create distinct sections within the maze, complemented by modifications and end points:

    .. code-block:: console

       generate_maze.py -x 60 -y 100 -f 0,0,2,0 -m s/3 -c ^mn/s/3/3 -m n/5/3 -c ^ms/n/5/3 -e n/3 -e s

    .. figure:: /images/example_cmd_close_4.svg
        :width: 300px

Merge Smaller Rooms into Larger Ones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Merging smaller rooms into larger spaces within your maze not only changes its visual appeal but can also be used to highlight ends or points of interest along the way. It's important to note that merging is restricted to the original 1x1 room layout and should not interfere with already merged areas or rooms of unique shapes.

For the merge to be valid, at least one of the rooms within the designated merge area must remain a standard room, maintaining connectivity with the rest of the maze.

.. option:: -m <merge definition>, --add-merge <merge definition>

    This command merges specified rooms into a single, larger room. The required format for the argument is: ``<placement>[/<size>[/<offset>]]``

    The :ref:`placement parameter<param-placement>` is essential and can be optionally followed by a :ref:`size parameter<param-size>` and an :ref:`offset parameter<param-offset>`, with each parameter divided by a slash ``/``.

    For instance, to merge rooms located at all cardinal points and midpoints around the maze, use the following command:

    .. code-block:: console

       generate_maze.py -x 60 -y 60 -m w/3 -m nw/3 -m n/3 -m ne/3 -m e/3 -m se/3 -m s/3 -m sw/3

    .. figure:: /images/example_cmd_merge_1.svg
        :width: 420px

    In cases where the area designated for merging overlaps with blank spaces, these spaces will revert to standard rooms as part of the merge process:

    .. code-block:: console

       generate_maze.py -x 84 -y 60 -e nw -e se -m w/3/1 -m nw/3 -m n/3/1 -m ne/3 -m e/3/1 -m se/3 -m s/3/1 -m sw/3 -b c/5 -f 1 -c ^m/w/3/1 -c ^m/nw/3 -c ^m/n/3/1 -c ^m/ne/3 -c ^m/e/3/1 -c ^m/se/3 -c ^m/s/3/1 -c ^m/sw/3

    .. figure:: /images/example_cmd_merge_2.svg
        :width: 420px


Options for the SVG Output
--------------------------

Customize the SVG output of your maze with the following options, allowing for adjustments in the file's location, appearance, and technical specifications.

.. option:: -o <path>, --output <path>

   Designate the filename or path for the generated SVG file. Without specification, the default file name used is ``output.svg``. Both relative and absolute paths are supported.

.. option:: --no-marks

   Activating this flag will omit the colored rectangle markers at the path ends. This option is particularly beneficial for integrating the maze generation into automated workflows, where such markers may not be needed.

.. option:: --svg-unit {mm,px}

   Select the unit of measurement for the SVG file's dimensions. By default, ``mm`` (millimeters) is used.

   Note: Switching to ``px`` (pixels) modifies the unit within the SVG file only and does not affect the input dimensions (width, height, or room length), which should always be provided in millimeters.

.. option:: --svg-dpi <dpi>

   Define the DPI (dots per inch) for converting millimeter measurements to pixels in the SVG output. The default setting is 96 DPI, and the acceptable range spans from 60 to 10,000 DPI.

.. option:: --svg-zero-point {center,top_left}

   Adjust the origin point of the SVG canvas. By default, the ``center`` option is used.

.. list-table::
    :header-rows: 1
    :widths: 25, 75
    :width: 100%

    *   -   Parameter
        -   Meaning
    *   -   ``center``
        -   Places the maze's center at the middle of the canvas, ensuring all SVG coordinates are positive from the document's top-left corner. This is the default and best choice for viewing the SVG or using it for designs, web or print.
    *   -   ``top_left``
        -   Moves the zero point to the top-left corner of the document, beneficial for workflows requiring the maze's center at the document's origin, though it may not display correctly in all viewers.

.. option:: --svg-no-background

    When this flag is set, the generated SVG will not include a background rectangle, resulting in a transparent background.

.. option:: --svg-background-color {color_value}

    Sets the background color of the SVG output. This option takes effect only if the background is enabled (i.e., :option:`--svg-no-background` is not set). The value must be specified using one of the supported color formats listed below.

.. option:: --svg-room-color {color_value}

    Sets the fill color for the maze rooms—the connected paths that form the maze itself. The color must be provided in one of the supported formats shown below.

.. option:: --svg-endpoint-color {color_value}

    Use this option one or more times to define the colors of the maze endpoints in the SVG output. The order of values determines the colors assigned to each endpoint. If fewer colors are provided than endpoints, the list will cycle as needed. Each color value must follow one of the supported formats below.

.. code-block:: console

    generate_maze.py -x 60 -y 60 -b c/2 --svg-background-color=#800 --svg-room-color=#f42 --svg-endpoint-color=#fff --svg-endpoint-color=#000

.. figure:: /images/example_cmd_color_1.svg
    :width: 300px

Supported Color Formats
^^^^^^^^^^^^^^^^^^^^^^^

The following color formats are accepted:

**Hexadecimal Notation:**

* ``#RRGGBB``
* ``#RGB``
* ``#RRGGBBAA``
* ``#RGBA``

Each component (``R``, ``G``, ``B``, ``A``) is a hexadecimal digit.

**CSS Color Functions:**

* ``rgb(R,G,B)``
* ``rgba(R,G,B,A)``
* ``hsl(H,S%,L%)``
* ``hsla(H,S%,L%,A)``

Where:

* ``R``, ``G``, ``B`` are integers between 0–255,
* ``A`` is a floating-point value between 0.0–1.0,
* ``H`` is a degree value between 0–360,
* ``S`` and ``L`` are percentages between 0–100 (with a ``%`` suffix).


Other Options
-------------

Explore additional options to enhance your command-line experience with the maze generator, ranging from accessing help resources to customizing the maze generation process.

.. option:: -h, --help

   This option displays a comprehensive help page detailing all available command-line options. It's a quick way to reference the functionality and parameters you can use.

.. option:: --silent

   Activate this mode to suppress progress messages during the maze generation process. This is particularly useful when integrating the tool into scripts or automated workflows where console output needs to be minimized.

.. option:: --ignore-errors

   When enabled, this option instructs the generator to proceed despite encountering errors, aiming to produce an output. This can be invaluable for debugging, offering insights into issues without halting the process.

.. option:: --layout-only

   This option halts the process after the layout preparation phase, saving the resulting layout where all potential connections remain open. It's designed for debugging purposes or scenarios where a template of all possible maze configurations is required.

.. _param-placement:

Placement Parameter
-------------------

The concept of placements is pivotal for tailoring your maze's design without the need to recalibrate absolute coordinates every time the maze's dimensions change. Placements allow you to specify positions within the maze relative to nine predefined points, offering an intuitive method to anchor your customizations.

The :ref:`param-offset` and :ref:`param-size` parameters are dynamically adjusted based on the specified placement, streamlining the customization process.

.. note::

    The ``random`` placement option assigns elements to unpredictable positions within the maze. While this can add an element of surprise and complexity, it also increases the likelihood of conflicts and overlaps. Consequently, generating a maze with random placements may necessitate multiple attempts to achieve a satisfactory and valid layout.

.. list-table::
    :header-rows: 1
    :widths: 25 75
    :width: 100%

    * - Parameter
      - Meaning
    * - ``left``, ``w``
      - Positioned at the midpoint of the left edge.
    * - ``top_left``, ``nw``
      - Located at the top left corner.
    * - ``top``, ``n``
      - Positioned at the midpoint of the top edge.
    * - ``top_right``, ``ne``
      - Located at the top right corner.
    * - ``right``, ``e``
      - Positioned at the midpoint of the right edge.
    * - ``bottom_right``, ``se``
      - Located at the bottom right corner.
    * - ``bottom``, ``s``
      - Positioned at the midpoint of the bottom edge.
    * - ``bottom_left``, ``sw``
      - Located at the bottom left corner.
    * - ``center``, ``c``
      - Positioned at the maze's center.
    * - ``random``, ``r``
      - Assigned to a random location within the maze.

.. _param-size:

Size Parameter
--------------

The size parameter plays a critical role in defining the scale of areas within your maze. It allows for both uniform and non-uniform area dimensions, catering to a variety of design needs.

You can specify the size in two ways:

1. As a single positive integer (e.g., ``3``), which sets both the width and height of the area to that value, resulting in a square.
2. As two positive integers separated by an ``x`` (e.g., ``3x2``), where the first number defines the width and the second defines the height of the area, enabling rectangular shapes.

Additionally, there are predefined size names for convenience, allowing quick selection of common sizes without specifying exact dimensions.

.. list-table::
    :header-rows: 1
    :widths: 25 75
    :width: 100%

    * - Parameter
      - Meaning
    * - ``single``
      - Defines an area size of 1×1 rooms.
    * - ``small``
      - Sets the area to 2×2 rooms.
    * - ``medium``
      - Establishes a size of 3×3 rooms.
    * - ``large``
      - Expands the area to 4×4 rooms.
    * - One number: ``5``
      - Creates an area of 5×5 rooms.
    * - Two numbers: ``2x4``
      - Specifies an area of 2×4 rooms, catering to specific layout requirements.


.. _param-offset:

Offset Parameter
----------------

The offset parameter enhances the precision in positioning elements within your maze. It allows for adjustments both towards the maze's center and independently along the X and Y axes. Here's how you can specify the offset:

1. As a single number (e.g., ``3``), the offset applies diagonally towards the maze's center. The direction of this diagonal movement is influenced by the specified placement. For example, an element placed in the bottom right corner with a positive single-number offset would move diagonally up and left, closer to the center.

2. As two numbers separated by a comma (e.g., ``-4,2``), the offset operates independently of the element's initial placement. The first number adjusts the position along the X-axis, and the second number along the Y-axis. Positive numbers move the element right (X-axis) or down (Y-axis), while negative numbers move it left (X-axis) or up (Y-axis).

.. list-table::
    :header-rows: 1
    :widths: 25 75
    :width: 100%

    * - Parameter
      - Meaning
    * - One number: ``5``
      - Moves the element diagonally towards the center, the direction dependent on its placement.
    * - Two numbers: ``2,-4``
      - Applies an independent offset along the X and Y-axis, allowing for precise positioning.


.. _param-closing:

Closing Parameter
-----------------

The closing parameter is a strategic tool for controlling the maze's layout by specifying which connections between rooms are to be permanently sealed off. The use of a ``^`` character as a prefix inversely selects the connections, adding versatility to your design strategy.

For instance, ``corner_paths`` would block all paths at the corners of a specified area. Conversely, ``^corner_paths`` would keep only the corner connections open, blocking all others.

This parameter can significantly influence the maze's navigational complexity and aesthetic appeal.

.. list-table::
    :header-rows: 1
    :widths: 35 65
    :width: 100%

    * - Parameter
      - Meaning
    * - ``corner_paths``, ``c``
      - Blocks connections at all four corners of the area.
    * - ``corner_top_left``, ``cnw``
      - Blocks the connection at this corner.
    * - ``corner_top_right``, ``cne``
      - Blocks the connection at this corner.
    * - ``corner_bottom_right``, ``cse``
      - Blocks the connection at this corner.
    * - ``corner_bottom_left``, ``csw``
      - Blocks the connection at this corner.
    * - ``direction_west``, ``dw``
      - Seals off all connections extending westward from the specified area.
    * - ``direction_north``, ``dn``
      - Seals off all connections extending northward from the specified area.
    * - ``direction_east``, ``de``
      - Seals off all connections extending eastward from the specified area.
    * - ``direction_south``, ``ds``
      - Seals off all connections extending southward from the specified area.
    * - ``direction_horizontal``, ``dh``
      - Blocks all horizontal connections within the specified area.
    * - ``direction_vertical``, ``dv``
      - Blocks all vertical connections within the specified area.
    * - ``middle_paths``, ``m``
      - Blocks all connections that intersect the midpoints of the area's sides.
    * - ``middle_west``, ``mw``
      - Blocks the connection at the midpoint of the western side.
    * - ``middle_north``, ``mn``
      - Blocks the connection at the midpoint of the northern side.
    * - ``middle_east``, ``me``
      - Blocks the connection at the midpoint of the eastern side.
    * - ``middle_south``, ``ms``
      - Blocks the connection at the midpoint of the southern side.


.. _param-insets:

Insets Parameter
----------------

The insets parameter allows you to define the thickness of a frame around the maze. This parameter offers a flexible way to adjust the spacing around elements or areas by specifying up to four positive numbers, each separated by a comma. The application of these numbers varies based on how many you provide:

- **One Number**: Applies uniformly to all four sides of the area (top, right, bottom, left), creating an evenly distributed frame.
- **Two Numbers**: The first number sets the thickness for the top and bottom sides, while the second number applies to the left and right sides. This allows for vertical and horizontal spacing to be defined independently.
- **Three Numbers**: The first number specifies the top side, the second number applies to both the right and left sides equally, and the third number sets the thickness for the bottom side. This configuration is less common but can be useful for specific design needs.
- **Four Numbers**: Each number corresponds directly to one side of the area in the order of top, right, bottom, and left. This offers the most precise control over the spacing, allowing each side to be individually adjusted.

