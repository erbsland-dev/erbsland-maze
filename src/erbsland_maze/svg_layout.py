#  Copyright © 2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from colorsys import hsv_to_rgb
from pathlib import Path
from typing import Tuple

import cairo

from . import Color
from .direction import Direction
from .layout import Layout
from .line import Line
from .point import Point
from .poly_line import PolyLine
from .rectangle import Rectangle
from .room import Room
from .room_location import RoomLocation
from .room_size import RoomSize
from .size import Size
from .svg_setup import SvgSetup
from .svg_unit import SvgUnit
from .svg_zero_point import SvgZeroPoint
from .wall import Wall
from .wall_points import WallPoints


class SvgLayout(Layout):
    """
    An SVG layout for the maze.

    This instance defines how the generated maze is rendered into the SVG file. By setting the individual dimensions,
    it also defines the number of rooms in the maze.
    """

    def __init__(self, setup: SvgSetup):
        """
        Create a new SVG layout instance.

        :param setup: The setup parameters for the SVG layout.
        """
        self.setup = setup
        #
        self._room_size = Size(0, 0)
        self._maze_size = RoomSize()
        self._offset: Point = Point()
        self._x_values: list[float] = []
        self._y_values: list[float] = []
        if self.setup.svg_unit == SvgUnit.PX:
            self._svg_scale_factor = 1.0 / (25.4 / self.setup.svg_dpi)
        else:
            self._svg_scale_factor = 1.0
        self._svg_offset: Point = Point()

    def _check_count_limits(self, count, dimension):
        """
        Check if the given count is within the limits

        :param count: The count.
        :param dimension: The dimension for the error message.
        """
        if count < 5 or count > 10_000:
            raise ValueError(
                f"The number of generated rooms in the {dimension} ({count}) is outside valid limits (5-10'000)."
            )

    @staticmethod
    def _get_edge_coordinates(
        side_length: float, count: int, offset: float = 0, stretch_to_length: float = None
    ) -> list[float]:
        """
        Get a list with all the edge coordinates for one axis.

        :param side_length: The side length of the room in this axis.
        :param count: The number of rooms.
        :param offset: An optional offset to apply.
        :param stretch_to_length: If supplied, the first and last value are stretched to fill the whole length.
        :return: A list of edge coordinates.
        """
        result = list([offset + (x * side_length) for x in range(count + 1)])
        if stretch_to_length is not None:
            result[0] = 0.0
            result[-1] = stretch_to_length
        return result

    def _get_area_coordinates(
        self, room_size: Size, room_count: RoomSize, offset: Point = Point(), stretch_to_size: bool = False
    ) -> Tuple[list[float], list[float]]:
        """
        Get two lists with the edge coordinates that define the edges of the rooms in the given area.

        :param room_size: The size of the individual rooms.
        :param room_count: The number of rooms.
        :param offset: An offset to be applied to the top left corner.
        :param stretch_to_size: If the first and last edge values are stretched to completely fill the maze.
        :return: Two lists with the edge coordinates for both axes.
        """
        return (
            self._get_edge_coordinates(
                room_size.width, room_count.width, offset.x, self.setup.width if stretch_to_size else None
            ),
            self._get_edge_coordinates(
                room_size.height, room_count.height, offset.y, self.setup.height if stretch_to_size else None
            ),
        )

    def initialize(self) -> RoomSize:
        exact_size = Size(self.setup.side_length, self.setup.side_length)
        self._maze_size = self.setup.get_size().count_with_parity(
            exact_size, self.setup.width_parity, self.setup.height_parity
        )
        self._check_count_limits(self._maze_size.width, "width")
        self._check_count_limits(self._maze_size.height, "height")
        if self.setup.fill_mode.does_scale_room():
            self._room_size = self.setup.get_size() / self._maze_size
            if self.setup.fill_mode.does_proportionally_scale_room():
                self._room_size = self._room_size.min_square()
        else:
            self._room_size = exact_size
        if self.setup.fill_mode.does_center_rooms():
            offset = self.setup.get_size().get_center_offset(self._room_size * self._maze_size)
        else:
            offset = Point()
        self._x_values, self._y_values = self._get_area_coordinates(
            self._room_size, self._maze_size, offset, stretch_to_size=self.setup.fill_mode.does_stretch_edge()
        )
        if self.setup.svg_zero == SvgZeroPoint.TOP_LEFT:
            self._svg_offset = -(self.setup.get_size().get_center_point())
        return self._maze_size

    def get_dimension_info(self) -> str:
        return (
            f"{self.setup.width:0.2f} x {self.setup.height:0.2f} mm / thickness {self.setup.wall_thickness:0.2f} mm / "
            f"calculated room size: {self._room_size.width} x {self._room_size.height} mm"
        )

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
        inset = self.setup.wall_thickness / 2
        match wall.direction:
            case Direction.NORTH:
                return WallPoints(
                    adjacent1=rect.top_left.translated(x=inset),
                    inset1=rect.top_left.translated(x=inset, y=inset),
                    adjacent2=rect.top_right.translated(x=-inset),
                    inset2=rect.top_right.translated(x=-inset, y=inset),
                )
            case Direction.EAST:
                return WallPoints(
                    adjacent1=rect.top_right.translated(y=inset),
                    inset1=rect.top_right.translated(x=-inset, y=inset),
                    adjacent2=rect.bottom_right.translated(y=-inset),
                    inset2=rect.bottom_right.translated(x=-inset, y=-inset),
                )
            case Direction.SOUTH:
                return WallPoints(
                    adjacent1=rect.bottom_left.translated(x=inset),
                    inset1=rect.bottom_left.translated(x=inset, y=-inset),
                    adjacent2=rect.bottom_right.translated(x=-inset),
                    inset2=rect.bottom_right.translated(x=-inset, y=-inset),
                )
            case Direction.WEST:
                return WallPoints(
                    adjacent1=rect.top_left.translated(y=inset),
                    inset1=rect.top_left.translated(x=inset, y=inset),
                    adjacent2=rect.bottom_left.translated(y=-inset),
                    inset2=rect.bottom_left.translated(x=inset, y=-inset),
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

    def _set_color(self, ctx: cairo.Context, color: Color) -> None:
        """
        Set the source color from the given color.

        :param ctx: The cairo context.
        :param color: The color.
        """
        if color.a != 1.0:
            ctx.set_source_rgba(color.r, color.g, color.b, color.a)
        else:
            ctx.set_source_rgb(color.r, color.g, color.b)

    def _paint_room_mark(self, ctx: cairo.Context, room: Room, color: Color) -> None:
        """
        Paint a coloured rectangle into the given room to mark it visually.

        :param ctx: The cairo context.
        :param room: The room.
        :param color: The color.
        :return:
        """
        self._set_color(ctx, color)
        path_width = max(self._room_size.width, self._room_size.height) - self.setup.wall_thickness
        inset = self.setup.wall_thickness / 2
        if room.size.width > 2 and room.size.height > 2:
            inset += path_width
        elif path_width > self.setup.wall_thickness:
            inset += path_width * 0.2
        room_rect = self.get_room_rectangle(room)
        mark_rect = room_rect.equally_inset_by(inset)
        rect = self.convert_rect_to_svg(mark_rect)
        ctx.rectangle(rect.pos.x, rect.pos.y, rect.size.width, rect.size.height)
        ctx.fill()

    def render_image(self, file_path: Path, rooms: list[Room], path_end_rooms: list[Room]) -> None:
        all_room_lines = self.get_all_lines(rooms)
        polylines = PolyLine.from_merged_lines(all_room_lines)
        for polyline in polylines:
            polyline.optimize()
        with cairo.SVGSurface(
            str(file_path),
            self.convert_value_to_svg(self.setup.width),
            self.convert_value_to_svg(self.setup.height),
        ) as surface:
            if self.setup.svg_unit == SvgUnit.MM:
                surface.set_document_unit(cairo.SVG_UNIT_MM)
            else:
                surface.set_document_unit(cairo.SVG_UNIT_PX)
            ctx = cairo.Context(surface)
            if self.setup.svg_background:
                self._set_color(ctx, self.setup.background_color)
                pos = self.convert_point_to_svg(Point(0, 0))
                size = self.convert_size_to_svg(Size(self.setup.width, self.setup.height))
                ctx.rectangle(
                    pos.x,
                    pos.y,
                    size.width,
                    size.height,
                )
                ctx.fill()
            self._set_color(ctx, self.setup.room_color)
            ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
            ctx.set_line_width(self.convert_value_to_svg(0.1))
            closed_polylines = [polyline for polyline in polylines if polyline.is_closed]
            if closed_polylines:
                for polyline in closed_polylines:
                    self._paint_polyline(ctx, polyline)
                ctx.fill()
            open_polylines = [polyline for polyline in polylines if not polyline.is_closed]
            if open_polylines:
                for polyline in open_polylines:
                    self._paint_polyline(ctx, polyline)
                    ctx.stroke()
            for index, room in enumerate(path_end_rooms):
                if self.setup.endpoint_colors:
                    color = self.setup.endpoint_colors[index % len(self.setup.endpoint_colors)]
                else:
                    color = Color.for_endpoint(index, len(path_end_rooms))
                self._paint_room_mark(ctx, room, color)
