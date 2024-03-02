#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from collections import defaultdict

from .line import Line
from .point import Point
from .types import GenericLine


class PolyLine(GenericLine):
    """
    A line that consists of multiple points, connected by straight lines.
    """

    def __init__(self, points: list[Point] = None, is_closed: bool = False):
        """
        Create a new polyline.

        :param points: The points for the line.
        :param is_closed: If the line is closed.
        """
        self._points = points or []
        self.is_closed = is_closed

    @property
    def first(self) -> Point:
        if self.points:
            return self.points[0]

    @property
    def last(self) -> Point:
        if self.points:
            return self.points[-1]

    @property
    def points(self) -> list["Point"]:
        return self._points

    def join(self, line: GenericLine) -> bool:
        """
        Try joining a given line with this polyline.

        :param line: The line to join.
        :return: `True` if the line was joined.
        """
        if self.is_closed:
            return False
        has_merge = False
        if self.first == line.first:
            self._points = list(reversed(line.points[1:])) + self._points
            has_merge = True
        elif self.first == line.last:
            self._points = line.points[:-1] + self._points
            has_merge = True
        elif self.last == line.first:
            self._points.extend(line.points[1:])
            has_merge = True
        elif self.last == line.last:
            self._points.extend(list(reversed(line.points[:-1])))
            has_merge = True
        if has_merge and self.first == self.last:
            self._points.pop()
            self.is_closed = True
        return has_merge

    @classmethod
    def from_merged_lines(cls, lines: list[GenericLine]) -> list["PolyLine"]:
        """
        Create one or more poly-lines from a list of lines.
        The lines are joined at the ends into continuous polylines.

        :param lines: A list of lines.
        :return: One or more poly-lines
        """
        if not lines:
            return []
        # First create a quick lookup table.
        processed_lines: set[id] = set()
        line_map: dict[Point, list[GenericLine]] = defaultdict(list)
        for line in lines:
            line_map[line.first].append(line)
            line_map[line.last].append(line)
        result: list["PolyLine"] = []
        for start_line in lines:
            if id(start_line) in processed_lines:
                continue
            processed_lines.add(id(start_line))
            current_line = cls(start_line.points) if not isinstance(start_line, PolyLine) else start_line
            is_extension_possible = True
            while is_extension_possible:
                is_extension_possible = False
                for next_point in [current_line.first, current_line.last]:
                    for next_line in line_map.get(next_point, []):
                        if id(next_line) in processed_lines:
                            continue  # Skip if already processed
                        if current_line.join(next_line):
                            processed_lines.add(id(next_line))
                            is_extension_possible = True
                            break  # Break to restart extension check
                    if is_extension_possible:
                        break  # Break to restart extension check
            result.append(current_line)
        return result

    def optimize(self) -> None:
        """
        Optimize this polyline by merging straight lines that share co-linear lines.
        """
        if len(self._points) < 3:
            # If there are fewer than 3 points, no optimization is needed.
            return
        optimized_points = [self._points[0]]
        for index in range(len(self._points) - 2):
            line1 = Line(self._points[index], self._points[index + 1])
            line2 = Line(self._points[index + 1], self._points[index + 2])
            if not line1.is_collinear_with(line2):
                optimized_points.append(self._points[index + 1])
        optimized_points.append(self._points[-1])
        self._points = optimized_points
