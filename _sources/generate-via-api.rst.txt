
Generate Mazes via API
======================

.. currentmodule:: erbsland_maze

Creating labyrinths programmatically via the API offers the same level of customization and control as the command-line tool, but with the flexibility and integration capabilities of a Python script. Below is a concise guide to generating mazes using the Erbsland Maze API.

Start by importing the necessary classes from the :mod:`erbsland_maze` module. This includes setup for the SVG output, layout configurations, modifiers to customize the maze, and the generator itself. The :mod:`pathlib` module is used for file path operations, ensuring compatibility across different operating systems.

.. code-block:: pycon

    >>> from erbsland_maze import SvgSetup, SvgLayout, BlankModifier, Placement, RoomSize, GeneratorSetup, Generator
    >>> from pathlib import Path
    >>> svg_setup = SvgSetup(width=100.0, height=100.0, side_length=5.0)
    >>> svg_layout = SvgLayout(svg_setup)
    >>> modifiers = [BlankModifier(Placement.CENTER, RoomSize(5, 5))]
    >>> generator_setup = GeneratorSetup(modifiers=modifiers)
    >>> generator = Generator(svg_layout)
    >>> svg_file = Path('maze.svg')
    >>> generator.generate_and_save(svg_file)
    Erbsland Maze - V1.1
      Layout: 100.00 x 100.00 mm / thickness 1.70 mm / calculated side length: 4.76 mm
      Room count: 21 x 21
    Preparing rooms...
    1. attempt to find a solution.
    Generating the paths for the maze...
    Filling islands...
    Verifying generated paths...
    Connect all paths...
      - successfully joined paths 1-2
    Rendering image...

In this example, a maze with a dimension of 100x100 mm is created, with a specified side length of 5.0 mm for each room. A :class:`BlankModifier` is used to create a blank area in the center of the maze, demonstrating how to apply customizations. The maze generation process is initiated, and the resulting SVG is saved to a file named "maze.svg".

.. figure:: /images/example_api_initial.svg
    :width: 300px

This approach provides a powerful way to integrate maze generation into applications, allowing for dynamic creation and manipulation of mazes based on user input or other runtime conditions.

Step by Step
------------

Generating a maze programmatically involves a series of steps that allow you to customize every aspect of the maze, from its layout and dimensions to specific features like end points and blank spaces. Here's a step-by-step guide to creating a maze using the Erbsland Maze API:

1. **Initialize the Layout**: Start by creating an instance of the :class:`Layout` class for the :class:`Generator`. The API provides an :class:`SvgLayout` class, which is designed to work with SVG output. This class requires an instance of :class:`SvgSetup` that contains the initial setup parameters, including dimensions and side length.

2. **Configure the Generator**: If you wish to customize your maze, prepare a :class:`GeneratorSetup` instance next. This setup allows you to add modifications such as end points, blank spaces, or any other modifiers to the maze's layout.

3. **Instantiate the Generator**: With your :class:`SvgLayout` and :class:`GeneratorSetup` ready, create a new :class:`Generator` instance. Pass the previously prepared :class:`SvgLayout` and :class:`GeneratorSetup` to the constructor of the :class:`Generator`.

4. **Generate and Save the Maze**: To kick off the maze generation process and save the output, call the :meth:`Generator.generate_and_save` method on the :class:`Generator` instance, providing a :class:`pathlib.Path` object that specifies the filename and location for the generated SVG file.

For subsequent mazes with the same layout but different configurations or to introduce randomness, you can call the :meth:`Generator.generate_and_save` method multiple times. Each call generates a new maze according to the current :class:`GeneratorSetup` configuration.

Feel free to adjust the settings in your :class:`GeneratorSetup` between generations to explore different maze layouts and features. However, should you need to modify the maze's dimensions or fundamental layout, you will need to instantiate a new :class:`Layout` and :class:`Generator`.

The Generator
-------------

At the heart of the maze generation process lies the :class:`Generator`, which leverages an abstract algorithm to construct the maze. This component works hand-in-hand with a :class:`Layout` class, tasked with transforming the conceptual room layout into a tangible image.

.. class:: Generator(layout: Layout, setup: GeneratorSetup)

    Essential to the maze generation, the :class:`Generator` orchestrates the creation process, guided by a :class:`Layout` instance for graphical representation and a :class:`GeneratorSetup` for procedural directives.

    :param layout: Specifies the graphical framework for maze generation.
    :type layout: Layout
    :param setup: Dictates the generation strategy and maze configuration.
    :type setup: GeneratorSetup

    .. method:: generate_and_save(path)

        Executes the maze generation and commits the final image to file.

        :param path: Designates the file path for the saved maze image.
        :type path: pathlib.Path

The :class:`GeneratorSetup` class is instrumental in fine-tuning the generation process, offering a wide array of parameters to customize the maze's layout, appearance, and complexity.

.. class:: GeneratorSetup(path_ends=None, modifiers=None, allow_islands=True, maximum_attempts=20, verbose=True, ignore_errors=False, layout_only=False)

    Configures the operational parameters for the :class:`Generator`, influencing everything from path dynamics to visual modifiers.

    :param list[PathEnd] path_ends: A list of path-ends in the maze..
    :param list[Modifier] modifiers: A list of modifiers to customize the maze layout..
    :param bool allow_islands: Allows isolated sections in the maze. They will filled with random paths as decorations. If set to ``False``, isolated sections raise an exception.
    :param int maximum_attempts: Caps the attempts to resolve the maze.
    :param bool verbose: Enables or disables console updates throughout the generation process.
    :param bool ignore_errors: Allows the process to continue past errors, useful for debugging.
    :param bool layout_only: If enabled, there is no maze generated and just the room layout saved into the image.

The SVG Layout
--------------

This project currently provides only built-in support to generate SVG files using the PyCairo library. In order to render the mazes in SVG files, you have to create an instance of the :class:`SvgLayout` class and pass it to the constructor of :class:`Generator`.

.. py:class:: SvgLayout(setup: SvgSetup)

    The SVG layout class renders the generated maze into a SVG file using PyCairo. It takes one parameter `setup` that contains all dimensions and settings defining the rendered maze.

    :param setup: The setup values for the SVG layout.
    :type setup: SvgSetup

.. py:class:: SvgSetup

    This class provides all attributes for the SVG layout.

    .. attribute:: width
        :type: float

        This mandatory attribute specifies the width of the maze in millimeters (mm). The width impacts the final dimensions of the generated SVG file. When used alongside the :attr:`side_length`, the layout calculates the optimal number of rooms along the X axis.

    .. attribute:: height
        :type: float

        This required attribute sets the height of the maze in millimeters (mm). Similar to width, height determines the dimensions of the resulting SVG file. In combination with the :attr:`side_length` attribute, it helps in determining the ideal number of rooms along the Y axis.

    .. attribute:: wall_thickness
        :type: float
        :value: 1.7

        Defines the thickness of the maze's walls with this option, measured in millimeters (mm). If not specified, a default thickness of 1.7 mm is applied.

    .. attribute:: side_length
        :type: float
        :value: 4.0

        This parameter establishes the side length of each room within the maze, including wall thickness, measured in millimeters (mm). The default value is 4 mm.

        .. note::

            If the maze's specified width and height do not proportionately match the room length set by this option, the outer rooms will be adjusted in size to ensure the entire area is filled.

    .. attribute:: width_parity
        :type: Parity
        :value: Parity.ODD

        This option allows you to determine the parity (odd or even) of the room count along the X axis.

    .. attribute:: height_parity
        :type: Parity
        :value: Parity.ODD

        Similarly, this option lets you set the parity (odd or even) of the room count along the Y axis.

    .. attribute:: start_end_mark
        :type: bool
        :value: True

        this flag controls if the colored rectangle markers at the path ends will be painted or not. Setting this attribute to ``False`` is particularly beneficial for integrating the maze generation into automated workflows, where such markers may not be needed.

    .. attribute:: svg_unit
        :type: SvgUnit
        :value: SvgUnit.MM

        Select the unit of measurement for the SVG file's dimensions.

        .. note::

            Switching to :attr:`SvgUnit.PX` (pixels) modifies the unit within the SVG file only and does not affect the input dimensions (:attr:`width`, :attr:`height`, or :attr:`side_length`), which should always be provided in millimeters.

    .. attribute:: svg_dpi
        :type: float
        :value: 96.0

        Define the DPI (dots per inch) for converting millimeter measurements to pixels in the SVG output. The default setting is 96 DPI, and the acceptable range spans from 60 to 10,000 DPI.

    .. attribute:: svg_zero
        :type: SvgZeroPoint
        :value: SvgZeroPoint.CENTER

        Adjust the origin point of the SVG canvas.

        .. list-table::
            :header-rows: 1
            :widths: 25, 75
            :width: 100%

            *   -   Parameter
                -   Meaning
            *   -   :attr:`SvgZeroPoint.CENTER`
                -   Places the maze's center at the middle of the canvas, ensuring all SVG coordinates are positive from the document's top-left corner. This is the default and best choice for viewing the SVG or using it for designs, web or print.
            *   -   :attr:`SvgZeroPoint.TOP_LEFT`
                -   Moves the zero point to the top-left corner of the document, beneficial for workflows requiring the maze's center at the document's origin, though it may not display correctly in all viewers.

    .. attribute:: svg_background
        :type: bool
        :value: True

        This flag controls if the SVG background shall be drawn opaque.

.. autoclass:: Parity
    :members:

.. autoclass:: SvgFillMode
    :members:

.. autoclass:: SvgUnit
    :members:

.. autoclass:: SvgZeroPoint
    :members:


Path Ends
---------

.. autoclass:: PathEnd
    :members:


Modifier Classes
----------------

.. autoclass:: Modifier
    :members:

.. autoclass:: BlankModifier
    :members:

.. autoclass:: FrameModifier
    :members:

.. autoclass:: ClosingModifier
    :members:

.. autoclass:: Closing
    :members:

.. autoclass:: MergeModifier
    :members:


Modifier Enumerations
---------------------

.. autoclass:: ModifierType
    :members:

.. autoclass:: Placement
    :members:

.. autoclass:: ClosingType
    :members:


Room Layout Classes
-------------------

.. autoclass:: Room
    :members:

.. autoclass:: RoomConnection
    :members:

.. autoclass:: ConnectionSide
    :members:

.. autoclass:: RoomLocation
    :members:

.. autoclass:: RoomSize
    :members:

.. autoclass:: Wall
    :members:

.. autoclass:: RoomInsets
    :members:

.. autoclass:: RoomOffset
    :members:

.. autoclass:: LocationGrid
    :members:


Room Layout Enumerations
------------------------

.. autoclass:: RoomType
    :members:

.. autoclass:: Direction
    :members:

.. autoclass:: Corner
    :members:


The Graphical Layout Classes
----------------------------

.. autoclass:: Layout
    :members:


Exception Classes
-----------------

.. autoexception:: GeneratorError
    :members:

.. autoexception:: ModifierError
    :members:

