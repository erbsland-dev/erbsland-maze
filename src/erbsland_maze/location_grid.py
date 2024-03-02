#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from itertools import product

from .corner import Corner
from .direction import Direction
from .placement import Placement
from .room_insets import RoomInsets
from .room_location import RoomLocation
from .room_size import RoomSize


@dataclass(order=True)
class LocationGrid:
    """
    A rectangular grid of room locations.
    """

    location: RoomLocation
    """The top left corner of the room grid."""

    size: RoomSize
    """The size of the room grid."""

    @property
    def top_left(self) -> RoomLocation:
        return self.location

    @property
    def top_right(self) -> RoomLocation:
        return self.location.translated(self.size.width - 1, 0)

    @property
    def bottom_right(self) -> RoomLocation:
        return self.location.translated(self.size.width - 1, self.size.height - 1)

    @property
    def bottom_left(self) -> RoomLocation:
        return self.location.translated(0, self.size.height - 1)

    def get_corner(self, corner: Corner) -> RoomLocation:
        """
        Get the location a corner.

        :param corner: The corner.
        :return: The location of the corner.
        """
        match corner:
            case Corner.TOP_LEFT:
                return self.top_left
            case Corner.TOP_RIGHT:
                return self.top_right
            case Corner.BOTTOM_RIGHT:
                return self.bottom_right
            case Corner.BOTTOM_LEFT:
                return self.bottom_left

    def is_corner(self, location: RoomLocation, corner: Corner = None) -> bool:
        """
        Test if the location is a corner.

        :param location: The location to compare.
        :param corner: A specific corner, or None for any corner.
        :return: `True` if the location is a corner.
        """
        if corner is None:
            return any([location == self.get_corner(c) for c in Corner])
        return location == self.get_corner(corner)

    @property
    def middle_north(self) -> RoomLocation:
        return self.location.translated((self.size.width - 1) // 2, 0)

    @property
    def middle_east(self) -> RoomLocation:
        return self.location.translated(self.size.width - 1, (self.size.height - 1) // 2)

    @property
    def middle_south(self) -> RoomLocation:
        return self.location.translated((self.size.width - 1) // 2, self.size.height - 1)

    @property
    def middle_west(self) -> RoomLocation:
        return self.location.translated(0, (self.size.height - 1) // 2)

    def get_middle(self, direction: Direction) -> RoomLocation:
        """
        Get a middle location in the given direction.

        :param direction: The direction.
        :return: The location.
        """
        match direction:
            case Direction.NORTH:
                return self.middle_north
            case Direction.EAST:
                return self.middle_east
            case Direction.SOUTH:
                return self.middle_south
            case Direction.WEST:
                return self.middle_west

    def is_middle(self, location: RoomLocation, direction: Direction = None) -> bool:
        """
        Test is the given location is at the middle location in the given direction.

        :param location: The location.
        :param direction: The specific direction, or None for all directions.
        :return: `True` if the given location is at the middle.
        """
        if direction is None:
            return any(location == self.get_middle(d) for d in Direction)
        return location == self.get_middle(direction)

    def contains(self, location: RoomLocation) -> bool:
        """
        Test if the given location is part of this grid.

        :param location: The tested location.
        :return: `True` if it is inside of this grid.
        """
        return (
            0 <= (location.x - self.location.x) < self.size.width
            and 0 <= (location.y - self.location.y) < self.size.height
        )

    def all_locations(self):
        """
        Get all locations in this room grid.
        """
        return [
            RoomLocation(self.location.x + x, self.location.y + y)
            for x, y in product(range(self.size.width), range(self.size.height))
        ]

    def is_frame(self, location: RoomLocation, insets: RoomInsets = RoomInsets(1, 1, 1, 1)) -> bool:
        """
        Test if the given location is part of the frame of this grid.

        :param location: The tested location.
        :param insets: The size of the frame.
        :return: `True` if the room is part of the frame.
        """
        if not self.contains(location):
            return False
        location -= self.location
        return (
            location.x < insets.east
            or location.y < insets.north
            or location.x >= (self.size.width - insets.west)
            or location.y >= (self.size.height - insets.south)
        )

    def all_frame_locations(self, insets: RoomInsets = RoomInsets(1, 1, 1, 1)) -> list[RoomLocation]:
        """
        Get all locations in this grid that are part of the frame.

        :param insets: The insets of the frame.
        :return: All locations that are part of the frame.
        """
        return [location for location in self.all_locations() if self.is_frame(location, insets)]

    def location_for_placement_and_size(self, placement: Placement, size: RoomSize) -> RoomLocation:
        """
        Get the location of the given placement.

        :param placement: The placement.
        :param size: The size of the modification.
        :return: The location of the given placement.
        """
        nx, ny = placement.placement_normals()
        if placement != Placement.RANDOM:
            location = RoomLocation(int((self.size.width - 1) * nx), int((self.size.height - 1) * ny))
            location += placement.size_offset(size)
        else:
            location = RoomLocation(
                int((self.size.width - size.width) * nx), int((self.size.height - size.height) * ny)
            )
        return location + self.location
