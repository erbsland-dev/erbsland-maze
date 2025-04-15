#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

import argparse
from pathlib import Path
from typing import Optional

from erbsland_maze import (
    BlankModifier,
    ClosingModifier,
    Color,
    FrameModifier,
    Generator,
    GeneratorError,
    GeneratorSetup,
    MergeModifier,
    Modifier,
    ModifierError,
    Parity,
    PathEnd,
    SvgFillMode,
    SvgLayout,
    SvgSetup,
    SvgUnit,
    SvgZeroPoint,
)


class UserError(Exception):
    pass


class CommandLineTool:
    def __init__(self):
        self.generator: Optional[Generator] = None
        self.output_path = Path()

    def run(self) -> None:
        self.read_command_line()
        try:
            self.generator.generate_and_save(self.output_path)
        except ModifierError as error:
            raise UserError(f"Your modifier '{error.modifier}' caused the following problem: {error}") from error
        except GeneratorError as error:
            raise UserError(f"The generator could not produce a valid maze for your input: {error}") from error

    def read_command_line(self) -> None:
        """
        Parse the command line arguments.
        """
        parser = argparse.ArgumentParser()
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.description = """\
            This command generates a random maze and stores it in a SVG file.
        """
        parser.add_argument(
            "-x",
            "--width",
            type=float,
            metavar="<dimension>",
            required=True,
            help="Width of the maze in mm.",
        )
        parser.add_argument(
            "-y",
            "--height",
            metavar="<dimension>",
            type=float,
            required=True,
            help="Height of the maze in mm.",
        )
        parser.add_argument(
            "-t",
            "--thickness",
            metavar="<dimension>",
            type=float,
            default=1.7,
            help="Thickness of the maze walls in mm.",
        )
        parser.add_argument(
            "-l",
            "--length",
            type=float,
            metavar="<dimension>",
            default=4.0,
            help="The side length of a room in mm including the wall thickness.",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=Path,
            metavar="<path>",
            default="output.svg",
            help="The path and name for the SVG file.",
        )
        parser.add_argument(
            "--no-marks", action="store_true", help="If specified, start and end positions are not marked."
        )
        parser.add_argument(
            "--svg-unit", choices=["mm", "px"], default="mm", help="The unit used for for the generated SVG file."
        )
        parser.add_argument(
            "--svg-dpi",
            type=float,
            default=96.0,
            metavar="<dpi>",
            help="The DPI value for the SVG file if 'px' units are used.",
        )
        parser.add_argument(
            "--svg-zero-point",
            choices=["center", "top_left"],
            default="center",
            help="Where the center point in the SVG file is placed.",
        )
        parser.add_argument(
            "--svg-no-background",
            action="store_true",
            help="If specified, no background is added to the SVG file.",
        )
        parser.add_argument(
            "--svg-background-color",
            type=str,
            metavar="<color>",
            help="The background color for the SVG file. See the documentation for supported color formats.",
        )
        parser.add_argument(
            "--svg-room-color",
            type=str,
            metavar="<color>",
            help="The color for the rooms in the SVG file.",
        )
        parser.add_argument(
            "--svg-endpoint-color",
            type=str,
            dest="svg_endpoint_colors",
            action="append",
            metavar="<color>",
            help="The color(s) for the end points in the SVG file.",
        )
        parser.add_argument(
            "-e",
            "--end-point",
            action="append",
            help="Specify two or more end points in the format '<placement>[/<offset>]'.",
        )
        parity_choices = list(str(x) for x in Parity)
        parser.add_argument(
            "--width-parity",
            choices=parity_choices,
            default="odd",
            help="The parity for the room count for the width of the maze.",
        )
        parser.add_argument(
            "--height-parity",
            choices=parity_choices,
            default="odd",
            help="The parity for the room count for the height of the maze.",
        )
        parser.add_argument(
            "-m",
            "--add-merge",
            action="append",
            type=str,
            metavar="<merge definition>",
            help="Add a merge modifier to alter the maze. The parameter has the format: "
            "<placement>[[/<size>]/<offset>]",
        )
        parser.add_argument(
            "-f",
            "--add-frame",
            type=str,
            metavar="<frame definition>",
            help="Add a frame modifier to alter the maze. The parameter has the format: <insets>",
        )
        parser.add_argument(
            "-b",
            "--add-blank",
            action="append",
            type=str,
            metavar="<blank definition>",
            help="Add a blank modifier to alter the maze. The parameter has the format: "
            "<placement>[[/<size>]/<offset>]",
        )
        parser.add_argument(
            "-c",
            "--add-closing",
            action="append",
            type=str,
            metavar="<closing definition>",
            help="Add a closing modifier to alter the maze. The parameter has the format: "
            "[^]<closing>/<placement>[[/<size>]/<offset>]",
        )
        parser.add_argument("--silent", action="store_true", help="Do not print progress messages on the console.")
        parser.add_argument(
            "--ignore-errors",
            action="store_true",
            help="Try to ignore all errors and produce an output anyway for debugging purposes.",
        )
        parser.add_argument(
            "--layout-only",
            action="store_true",
            help="Only prepare the rooms and save the layout of the maze for debugging purposes.",
        )
        parser.add_argument(
            "-i",
            "--fill-mode",
            choices=SvgFillMode.get_all_names(),
            default="stretch_edge",
            help="This option controls how the rooms are distributed in the specified canvas size.",
        )
        parser.epilog = """\
            About Modifiers Definitions:
            
            Separate multiple parameters with a '/' character and do not add spaces before
            or after each parameter.
             
            For <placement> use values like 'left', 'top_left', 'bottom_right' or
            alternatively directions like 'e', 'ne', 'n', 'sw'. Also there is 'center' or
            'c' and 'random' or 'r'.
            
            For <size> specify two positive integer values separated by the 'x' character
            like this '2x3'. If you omit it, the default `1x1` is used.
            
            For <insets> specify one to four positive integers, seperated by comma. One
            integer is applied to all four sides. For two integers, the first is applied
            to the top and bottom sides, and the second to the left and right side. For
            three or four integers, they define the frame size in the following order:
            top, right, bottom, left.
            
            For <offset> specify either a single integer, like '2', to offset the element
            towards the center of the maze, or use two integers seperated by a comma,
            like '-4,3' to define a custom offset.
            
            For <closing> specify which walls in the specified area shall get permanently
            closed. Valid values are 'corner_paths', 'direction_west', or 'middle_paths'.
            See the documentation for details. If you put a '^' character in front of the
            name (without spaces), all walls except the specified get closed. It inverts
            you chosen selection.
        """
        args = parser.parse_args()
        if args.svg_unit == "px":
            svg_unit = SvgUnit.PX
        else:
            svg_unit = SvgUnit.MM
        if args.svg_zero_point == "top_left":
            svg_zero_point = SvgZeroPoint.TOP_LEFT
        else:
            svg_zero_point = SvgZeroPoint.CENTER
        path_ends: Optional[list[PathEnd]] = None
        if args.end_point:
            path_ends = []
            if len(args.end_point) < 2:
                raise UserError("You must specify at least two end points.")
            if len(args.end_point) > 16:
                raise UserError("You must specify not more than 16 end points.")
            connected_end_points = 0
            for index, end_point in enumerate(args.end_point):
                try:
                    path_end = PathEnd.from_text(end_point)
                    if not path_end.is_dead_end:
                        connected_end_points += 1
                    path_ends.append(path_end)
                except ValueError as error:
                    raise UserError(f"There was a problem with the {index+1}. end point you specified: {error}")
            if connected_end_points < 2:
                raise UserError("You must specify at least two connected end points that are no dead-ends.")
        svg_setup_args = {
            "width": float(args.width),
            "width_parity": Parity(args.width_parity),
            "height": float(args.height),
            "height_parity": Parity(args.height_parity),
            "wall_thickness": float(args.thickness),
            "side_length": float(args.length),
            "fill_mode": SvgFillMode.from_text(args.fill_mode),
            "start_end_mark": (not args.no_marks),
            "svg_unit": svg_unit,
            "svg_dpi": float(args.svg_dpi),
            "svg_zero": svg_zero_point,
            "svg_background": not args.svg_no_background,
        }
        if args.svg_background_color:
            try:
                svg_setup_args["background_color"] = Color.from_text(args.svg_background_color)
            except ValueError as error:
                raise UserError(f"There was a problem with your SVG background color: {error}") from error
        if args.svg_room_color:
            try:
                svg_setup_args["room_color"] = Color.from_text(args.svg_room_color)
            except ValueError as error:
                raise UserError(f"There was a problem with your SVG room color: {error}") from error
        if args.svg_endpoint_colors:
            endpoint_colors = []
            for index, color in enumerate(args.svg_endpoint_colors):
                try:
                    endpoint_colors.append(Color.from_text(color))
                    if len(endpoint_colors) > 16:
                        raise UserError("You can only specify up to 16 endpoint colors.")
                except ValueError as error:
                    raise UserError(f"There was a problem with your {index+1}. SVG endpoint color: {error}") from error
            svg_setup_args["endpoint_colors"] = endpoint_colors
        svg_setup = SvgSetup(**svg_setup_args)
        svg_layout = SvgLayout(svg_setup)
        self.output_path = Path(args.output)
        modifiers: list[Modifier] = []
        if args.add_merge:
            for index, parameter in enumerate(args.add_merge):
                try:
                    modifiers.append(MergeModifier.from_text(parameter))
                except ValueError as error:
                    raise UserError(f"There was a problem with your {index + 1}. merge modifier: {error}") from error
        if args.add_frame:
            try:
                modifiers.append(FrameModifier.from_text(args.add_frame))
            except ValueError as error:
                raise UserError(f"There was a problem with your frame modifier: {error}") from error
        if args.add_blank:
            for index, parameter in enumerate(args.add_blank):
                try:
                    modifiers.append(BlankModifier.from_text(parameter))
                except ValueError as error:
                    raise UserError(f"There was a problem with your {index + 1}. blank modifier: {error}") from error
        if args.add_closing:
            for index, parameter in enumerate(args.add_closing):
                try:
                    modifiers.append(ClosingModifier.from_text(parameter))
                except ValueError as error:
                    raise UserError(f"There was a problem with your {index + 1}. closing modifier: {error}") from error
        setup = GeneratorSetup(
            path_ends=path_ends,
            modifiers=modifiers,
            verbose=not args.silent,
            ignore_errors=args.ignore_errors,
            layout_only=args.layout_only,
        )
        self.generator = Generator(svg_layout, setup)


def main():
    working_set = CommandLineTool()
    try:
        working_set.run()
    except UserError as error:
        exit(error)


if __name__ == "__main__":
    main()
