#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from colorsys import hsv_to_rgb
from math import floor
from pathlib import Path
from typing import Tuple

import cairo

from .direction import Direction
from .line import Line
from .parity import Parity
from .point import Point
from .poly_line import PolyLine
from .rectangle import Rectangle
from .room import Room
from .room_location import RoomLocation
from .room_size import RoomSize
from .size import Size
from .svg_unit import SvgUnit
from .svg_zero_point import SvgZeroPoint
from .wall import Wall
from .wall_points import WallPoints


class GraphicalLayout:
    """
    The graphical layout for the maze.

    This instance defines how the generated maze is rendered into the SVG file. By setting the individual sizes
    it also defines the dimensions of the maze, how many rooms it has.
    """

    def __init__(
        self,
        width: float,
        height: float,
        wall_thickness: float,
        side_length: float,
        width_parity: Parity = Parity.ODD,
        height_parity: Parity = Parity.ODD,
        start_end_mark: bool = True,
        svg_unit: SvgUnit = SvgUnit.MM,
        svg_dpi: float = 96.0,
        svg_zero: SvgZeroPoint = SvgZeroPoint.CENTER,
        svg_background: bool = True,
    ):
        """
        Create a new graphical layout instance.

        :param width: The width of the maze in mm.
        :param height: The height of the maze in mm.
        :param wall_thickness: The thickness of the walls in mm.
        :param side_length: The side length of a room, *including* the wall thickness, in mm.
        :param start_end_mark: If the start and end room shall be marked with a red and blue rectangle.
        :param svg_unit: The unit for the generated SVG file.
        :param svg_dpi: In case of PX unit, the DPI value to convert the MM values into PX.
        :param svg_zero: Select where the zero point of the maze shall be placed.
        """
        if not isinstance(width, float) or width < 40.0:
            raise ValueError("`width` must be a float, larger than 40.0.")
        if not isinstance(height, float) or height < 40.0:
            raise ValueError("`height` must be a float, larger than 40.0.")
        if not isinstance(wall_thickness, float) or wall_thickness < 0.1:
            raise ValueError("`wall_thickness` must be a float, larger than 0.1.")
        if not isinstance(side_length, float) or side_length < 2:
            raise ValueError("`side_length` must be a float, larger than 2.0.")
        if not isinstance(width_parity, Parity):
            raise ValueError("`width_parity` has the wrong type")
        if not isinstance(height_parity, Parity):
            raise ValueError("`height_parity` has the wrong type")
        if not isinstance(svg_unit, SvgUnit):
            raise ValueError("`svg_unit` has the wrong type")
        if not isinstance(svg_dpi, float) or svg_dpi < 60 or svg_dpi > 10_000:
            raise ValueError("`svg_dpi` must be a float, between 60 and 10'000.")
        if not isinstance(svg_zero, SvgZeroPoint):
            raise ValueError("`svg_zero` has the wrong type")
        if not isinstance(svg_background, bool):
            raise ValueError("`svg_background` has the wrong type.")
        self.width: float = width
        self.height: float = height
        self.wall_thickness: float = wall_thickness
        self.side_length: float = side_length
        self.width_parity: Parity = width_parity
        self.height_parity: Parity = height_parity
        self.start_end_mark: bool = start_end_mark
        self.svg_unit: SvgUnit = svg_unit
        self.svg_dpi: float = svg_dpi
        self.svg_zero: SvgZeroPoint = svg_zero
        self.svg_background: bool = svg_background
        if (side_length - wall_thickness) < 0.5:
            raise ValueError(
                "`side_length` and `wall_thickness` do not match, the resulting path width is smaller than 0.5 mm."
            )
        #
        self._size = RoomSize()
        self._offset: Point = Point()
        self._x_values: list[float] = []
        self._y_values: list[float] = []
        if svg_unit == SvgUnit.PX:
            self._svg_scale_factor = 1.0 / (25.4 / svg_dpi)
        else:
            self._svg_scale_factor = 1.0
        self._svg_offset: Point = Point()

    def _count_with_parity(self, length: float, parity: Parity) -> int:
        """
        Get a room round for the given length, using a parity.

        :param length: The length.
        :param parity: The parity.
        :return: A count.
        """
        if parity == Parity.NONE:
            result = int(floor(length / self.side_length))
        else:
            result = int(floor(length / self.side_length / 2)) * 2
            if parity == Parity.ODD:
                result += 1
        return result

    def initialize(self) -> RoomSize:
        """
        Initialize the layout and calculate the size of the maze to generate.

        :return: The size of the maze in rooms.
        """
        x_count = self._count_with_parity(self.width, self.width_parity)
        y_count = self._count_with_parity(self.height, self.height_parity)
        if x_count < 10 or x_count > 10_000:
            raise ValueError(
                f"The number of generated rooms in the width ({x_count}) is outside valid limits (10-10'000)."
            )
        if x_count < 10 or x_count > 10_000:
            raise ValueError(
                f"The number of generated rooms in the height ({y_count}) is outside valid limits (10-10'000)."
            )
        x_length = self.width / x_count
        y_length = self.height / y_count
        self.side_length = min(x_length, y_length)
        self._size = RoomSize(int(x_count), int(y_count))
        self._offset = Point(
            (self.width - (self.side_length * self._size.width)) / 2,
            (self.height - (self.side_length * self._size.height)) / 2,
        )
        self._x_values = list([self._offset.x + (x * self.side_length) for x in range(self._size.width)])
        self._y_values = list([self._offset.y + (y * self.side_length) for y in range(self._size.height)])
        self._x_values[0] = 0.0
        self._y_values[0] = 0.0
        self._x_values.append(self.width)
        self._y_values.append(self.height)
        if self.svg_zero == SvgZeroPoint.TOP_LEFT:
            self._svg_offset = Point(-self.width / 2.0, -self.height / 2.0)
        return self._size

    def get_location_rectangle(self, location: RoomLocation) -> Rectangle:
        """
        Get the graphical rectangle for the given room location.

        :param location: The location of the room.
        :return: The graphical rectangle for the given location.
        """
        return Rectangle(
            Point(self._x_values[location.x], self._y_values[location.y]),
            Size(
                self._x_values[location.x + 1] - self._x_values[location.x],
                self._y_values[location.y + 1] - self._y_values[location.y],
            ),
        )

    def get_room_rectangle(self, room: Room) -> Rectangle:
        """
        Get the graphical rectangle for the given room.

        :param room: The room.
        :return: The rectangle.
        """
        x1 = self._x_values[room.location.x]
        y1 = self._y_values[room.location.y]
        x2 = self._x_values[room.location.x + room.size.width]
        y2 = self._y_values[room.location.y + room.size.height]
        return Rectangle(Point(x1, y1), Size(x2 - x1, y2 - y1))

    def get_wall_points(self, wall: Wall) -> WallPoints:
        """
        Get a set of points for that are used to draw the lines for the situation at the given wall.

        :param wall: The wall for the points.
        :return: The points at this wall.
        """
        rect = self.get_location_rectangle(wall.location)
        inset = self.wall_thickness / 2
        match wall.direction:
            case Direction.NORTH:
                return WallPoints(
                    adjacent1=rect.top_left.moved(x=inset),
                    inset1=rect.top_left.moved(x=inset, y=inset),
                    adjacent2=rect.top_right.moved(x=-inset),
                    inset2=rect.top_right.moved(x=-inset, y=inset),
                )
            case Direction.EAST:
                return WallPoints(
                    adjacent1=rect.top_right.moved(y=inset),
                    inset1=rect.top_right.moved(x=-inset, y=inset),
                    adjacent2=rect.bottom_right.moved(y=-inset),
                    inset2=rect.bottom_right.moved(x=-inset, y=-inset),
                )
            case Direction.SOUTH:
                return WallPoints(
                    adjacent1=rect.bottom_left.moved(x=inset),
                    inset1=rect.bottom_left.moved(x=inset, y=-inset),
                    adjacent2=rect.bottom_right.moved(x=-inset),
                    inset2=rect.bottom_right.moved(x=-inset, y=-inset),
                )
            case Direction.WEST:
                return WallPoints(
                    adjacent1=rect.top_left.moved(y=inset),
                    inset1=rect.top_left.moved(x=inset, y=inset),
                    adjacent2=rect.bottom_left.moved(y=-inset),
                    inset2=rect.bottom_left.moved(x=inset, y=-inset),
                )

    @staticmethod
    def _horizontal_sort(wall: Wall) -> int:
        """
        Helper function for a horizontal sort.
        """
        return wall.location.x

    @staticmethod
    def _vertical_sort(wall: Wall) -> int:
        """
        Helper function for a vertical sort.
        """
        return wall.location.x

    def _intermediate_lines(self, all_walls: list[Wall], direction: Direction) -> list[Line]:
        """
        Get intermediate lines of a room. These are the lines between the doors or walls at the sides of the room.

        :param all_walls: All walls of the room.
        :param direction: The direction, which walls shall generate lines..
        :return: A list of lines.
        """
        if direction == Direction.NORTH or direction == Direction.SOUTH:
            key_fn = self._horizontal_sort
        else:
            key_fn = self._vertical_sort
        walls = list(sorted([wall for wall in all_walls if wall.direction == direction], key=key_fn))
        lines: list[Line] = []
        for i in range(len(walls) - 1):
            wp1 = self.get_wall_points(walls[i])
            wp2 = self.get_wall_points(walls[i + 1])
            lines.append(Line(wp1.inset2, wp2.inset1))
        return lines

    def get_lines_for_room(self, room: Room) -> list[PolyLine]:
        """
        Get all lines for a single room.

        :param room: The room to get the lines for.
        :return: A list of polylines for that room.
        """
        lines: list[Line] = []
        walls = room.get_walls()
        if room.size.width > 1:
            lines.extend(self._intermediate_lines(walls, Direction.NORTH))
            lines.extend(self._intermediate_lines(walls, Direction.SOUTH))
        if room.size.height > 1:
            lines.extend(self._intermediate_lines(walls, Direction.WEST))
            lines.extend(self._intermediate_lines(walls, Direction.EAST))
        for wall in walls:
            wall_points = self.get_wall_points(wall)
            if room.is_open_connection(wall):
                lines.append(Line(wall_points.inset1, wall_points.adjacent1))
                lines.append(Line(wall_points.inset2, wall_points.adjacent2))
            else:
                lines.append(Line(wall_points.inset1, wall_points.inset2))
        return PolyLine.from_merged_lines(lines)

    def get_all_lines(self, rooms: list[Room]) -> list[PolyLine]:
        """
        Get all lines for the given rooms.

        :param rooms: The rooms to get the lines from.
        :return: A list of polylines for the given rooms.
        """
        lines: list[PolyLine] = []
        for room in rooms:
            lines.extend(self.get_lines_for_room(room))
        return lines

    def convert_value_to_svg(self, value: float) -> float:
        """
        Convert a value into the selected target unit and coordinate system for the SVG file.

        :param value: The value to convert.
        :return: The converted value.
        """
        return value * self._svg_scale_factor

    def convert_point_to_svg(self, point: Point) -> Point:
        """
        Convert a point into the selected target unit and coordinate system for the SVG file.

        :param point: The point to convert.
        :return: The converted point.
        """
        return Point(self.convert_value_to_svg(point.x), self.convert_value_to_svg(point.y)) + self._svg_offset

    def convert_size_to_svg(self, size: Size) -> Size:
        """
        Convert a size into the selected target unit and coordinate system for the SVG file.

        :param size: The size to convert.
        :return: The converted size.
        """
        return Size(self.convert_value_to_svg(size.width), self.convert_value_to_svg(size.height))

    def convert_rect_to_svg(self, rect: Rectangle) -> Rectangle:
        """
        Convert a rectangle into the selected target unit and coordinate system for the SVG file.

        :param rect: The rectangle to convert.
        :return: The converted rectangle.
        """
        return Rectangle(self.convert_point_to_svg(rect.pos), self.convert_size_to_svg(rect.size))

    def _paint_polyline(self, ctx: cairo.Context, polyline: PolyLine) -> None:
        """
        Paint a polyline into the given cairo context.

        :param ctx: The context.
        :param polyline: The polyline to paint.
        """
        if not polyline.points:
            return
        for index, point in enumerate(polyline.points):
            point = self.convert_point_to_svg(point)
            if index == 0:
                ctx.move_to(point.x, point.y)
            else:
                ctx.line_to(point.x, point.y)
        if polyline.is_closed:
            ctx.close_path()
            ctx.fill()
        else:
            ctx.stroke()

    def _paint_room_mark(self, ctx: cairo.Context, room: Room, color: Tuple[float, float, float]) -> None:
        """
        Paint a coloured rectangle into the given room to mark it visually.

        :param ctx: The cairo context.
        :param room: The room.
        :param color: The color.
        :return:
        """
        ctx.set_source_rgb(*color)
        rect = self.get_room_rectangle(room).equally_inset_by(self.wall_thickness + self.wall_thickness * 0.5)
        rect = self.convert_rect_to_svg(rect)
        ctx.rectangle(rect.pos.x, rect.pos.y, rect.size.width, rect.size.height)
        ctx.fill()

    def save_svg(self, file_path: Path, rooms: list[Room], path_end_rooms: list[Room]) -> None:
        """
        Save the generated rooms into an SVG file.

        :param file_path: The path for the SVG file.
        :param rooms: A list of rooms.
        :param path_end_rooms: The path end rooms to be marked.
        """
        all_room_lines = self.get_all_lines(rooms)
        polylines = PolyLine.from_merged_lines(all_room_lines)
        for polyline in polylines:
            polyline.optimize()
        with cairo.SVGSurface(
            str(file_path),
            self.convert_value_to_svg(self.width),
            self.convert_value_to_svg(self.height),
        ) as surface:
            if self.svg_unit == SvgUnit.MM:
                surface.set_document_unit(cairo.SVG_UNIT_MM)
            else:
                surface.set_document_unit(cairo.SVG_UNIT_PX)
            ctx = cairo.Context(surface)
            if self.svg_background:
                ctx.set_source_rgb(0.9, 0.9, 0.9)
                pos = self.convert_point_to_svg(Point(0, 0))
                size = self.convert_size_to_svg(Size(self.width, self.height))
                ctx.rectangle(
                    pos.x,
                    pos.y,
                    size.width,
                    size.height,
                )
                ctx.fill()
            ctx.set_source_rgb(0.2, 0.2, 0.2)
            ctx.set_line_width(self.convert_value_to_svg(0.1))
            for polyline in polylines:
                self._paint_polyline(ctx, polyline)
            for index, room in enumerate(path_end_rooms):
                color = hsv_to_rgb(index / (len(path_end_rooms) + 1), 0.7, 0.7)
                self._paint_room_mark(ctx, room, color)
