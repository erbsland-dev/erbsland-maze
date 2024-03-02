#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .closing_type import ClosingType
from .corner import Corner
from .direction import Direction
from .location_grid import LocationGrid
from .room_location import RoomLocation


@dataclass(order=True, frozen=True)
class Wall:
    """
    A wall in a room.
    """

    location: RoomLocation
    """The location in the room where the wall is."""

    direction: Direction
    """The direction at this location where the wall is."""

    def matches_closing_type(self, closing_type: ClosingType, grid: LocationGrid) -> bool:
        """
        Test if this wall matches the closing type in relation to the given room grid.

        :param closing_type: The closing type.
        :param grid: The room grid.
        :return: `True` if the wall matches the closing type.
        """
        match closing_type:
            case ClosingType.CORNER_PATHS:
                return grid.is_corner(self.location)
            case ClosingType.CORNER_TOP_LEFT:
                return grid.is_corner(self.location, Corner.TOP_LEFT)
            case ClosingType.CORNER_TOP_RIGHT:
                return grid.is_corner(self.location, Corner.TOP_RIGHT)
            case ClosingType.CORNER_BOTTOM_RIGHT:
                return grid.is_corner(self.location, Corner.BOTTOM_RIGHT)
            case ClosingType.CORNER_BOTTOM_LEFT:
                return grid.is_corner(self.location, Corner.BOTTOM_LEFT)
            case ClosingType.DIRECTION_WEST:
                return self.direction == Direction.WEST
            case ClosingType.DIRECTION_NORTH:
                return self.direction == Direction.NORTH
            case ClosingType.DIRECTION_EAST:
                return self.direction == Direction.EAST
            case ClosingType.DIRECTION_SOUTH:
                return self.direction == Direction.SOUTH
            case ClosingType.DIRECTION_HORIZONTAL:
                return self.direction == Direction.WEST or self.direction == Direction.EAST
            case ClosingType.DIRECTION_VERTICAL:
                return self.direction == Direction.NORTH or self.direction == Direction.SOUTH
            case ClosingType.MIDDLE_PATHS:
                return grid.is_middle(self.location)
            case ClosingType.MIDDLE_WEST:
                return grid.is_middle(self.location, Direction.WEST)
            case ClosingType.MIDDLE_NORTH:
                return grid.is_middle(self.location, Direction.NORTH)
            case ClosingType.MIDDLE_EAST:
                return grid.is_middle(self.location, Direction.EAST)
            case ClosingType.MIDDLE_SOUTH:
                return grid.is_middle(self.location, Direction.SOUTH)
        return False
