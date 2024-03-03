#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from typing import Union

from .blank_modifier import BlankModifier
from .closing_modifier import ClosingModifier
from .direction import Direction
from .frame_modifier import FrameModifier
from .location_grid import LocationGrid
from .merge_modifier import MergeModifier
from .modifier import Modifier
from .modifier_error import ModifierError
from .path_end import PathEnd
from .placement import Placement
from .room import Room
from .room_connection import RoomConnection
from .room_location import RoomLocation
from .room_size import RoomSize
from .room_type import RoomType


class RoomGrid:
    """
    A grid in which rooms are placed.
    """

    def __init__(self, size: RoomSize):
        """
        Create a new room grid of the given size.

        :param size: The size for the room grid.
        """
        self._location_grid = LocationGrid(RoomLocation(0, 0), size)  # The rectangle with all locations.
        self._room_map: dict[RoomLocation, Room] = {}  # A map with room locations pointing to the rooms.

    def __getitem__(self, key: RoomLocation) -> Room:
        """
        Access a room from the grid, using its location.

        :param key: The room location.
        :return: The room.
        """
        return self._room_map[key]

    def __contains__(self, key: RoomLocation) -> bool:
        """
        Test if a room location exists in the grid.

        :param key: The room location.
        :return: `True` if the room location exists.
        """
        return key in self._room_map

    @property
    def size(self) -> RoomSize:
        return self._location_grid.size

    def get_all_locations(self) -> list[RoomLocation]:
        """
        Get all room locations.
        """
        return self._location_grid.all_locations()

    def get_all_rooms(self) -> set[Room]:
        """
        Get all unique rooms in this room grid.
        """
        return {room for room in self._room_map.values()}

    def get_all_connections(self) -> set[RoomConnection]:
        """
        Get a list of all connections between the rooms.
        """
        return {connection for room in self.get_all_rooms() for connection in room.connections}

    def get_join_candidates(self) -> list[RoomConnection]:
        """
        Get a list of connections between different paths that are candidates to be joined.
        """
        return [
            connection
            for connection in self.get_all_connections()
            if connection.is_closed and connection.connects_two_paths and connection.connects_primary_paths
        ]

    def location_grid_for_modifier(self, modifier: Modifier) -> LocationGrid:
        """
        Get the location for the given modifier.

        :param modifier: The modifier.
        :return: The location.
        """
        location = self._location_grid.location_for_placement_and_size(modifier.placement, modifier.size)
        location = modifier.offset.translate_location(location, modifier.placement)
        modifier_grid = LocationGrid(location, modifier.size)
        if not self._location_grid.contains(location) or not self._location_grid.contains(modifier_grid.bottom_right):
            raise ModifierError(
                modifier,
                f"The modifier '{modifier.name}' has an offset that results in affected locations "
                "outside of the maze.",
            )
        return modifier_grid

    def get_all_locations_for_modifier(self, modifier: Modifier) -> list[RoomLocation]:
        """
        Get all locations for a modifier.

        :param modifier: The modifier.
        :return: A generator with all locations
        """
        if modifier.placement is None:
            return self._location_grid.all_frame_locations(modifier.insets)
        grid = self.location_grid_for_modifier(modifier)
        return grid.all_locations()

    def get_location_for_path_end(self, path_end: PathEnd) -> RoomLocation:
        """
        Get the location to a path end.

        :param path_end: The path end.
        :return: The room location.
        """
        location = self._location_grid.location_for_placement_and_size(path_end.placement, RoomSize(1, 1))
        location = path_end.offset.translate_location(location, path_end.placement)
        return location

    def fill_with_rooms(self) -> None:
        """
        Fill the room grid with unused, unconnected 1x1 rooms.
        """
        for location in self.get_all_locations():
            self._room_map[location] = Room(location)

    def connect_all_rooms(self) -> None:
        """
        Create logical connections between all rooms.
        """
        for location in self.get_all_locations():
            room = self._room_map[location]
            for direction in Direction:
                target_location = location.advance(direction)
                if target_location not in self._room_map:
                    continue
                target_room = self._room_map[target_location]
                if room.is_connected_to_room(target_room):
                    continue
                room.add_connection(location, direction, target_room)

    def merge_area(self, grid: LocationGrid):
        """
        Merge this area and all rooms in it into one single room.

        :param grid: The room grid that shall be merged.
        """
        if grid.size.width < 2 or grid.size.height < 2:
            raise ValueError("Merged area must be at least 2x2 units.")
        room = self._room_map[grid.location]
        merged_rooms: set[Room] = set()
        all_connections: set[RoomConnection] = set()
        all_connections.update(room.connections)
        for merged_room in [self._room_map.get(l) for l in grid.all_locations() if l != room.location]:
            if merged_room is None:
                raise ValueError("Cannot merge area, overlaps with already merged rooms, or edge of maze.")
            if not merged_room.size.is_one:
                raise ValueError("Cannot merge area, overlaps with already merged rooms, or edge of maze.")
            merged_rooms.add(merged_room)
            all_connections.update(merged_room.connections)
            if room.type == RoomType.BLANK and merged_room.type == RoomType.PATH:
                room.type = merged_room.type
            if merged_room.type == RoomType.END:
                room.type = merged_room.type
            if room.path_id == 0 and merged_room.path_id > 0:
                room.path_id = merged_room.path_id
        # Keep all connections that connect the room edges.
        connections_to_keep: set[RoomConnection] = set()
        for c in all_connections:
            ra, rb = c.a.room, c.b.room
            if ra not in merged_rooms or rb not in merged_rooms:
                connections_to_keep.add(c)
        # Now expand this room.
        room.size = grid.size
        # Move all connections into this room and make that they point to this room.
        for merged_room in merged_rooms:
            for connection in [c for c in merged_room.connections if c in connections_to_keep]:
                connection.replace_room(merged_room, room)
                room.connections.append(connection)
            self._room_map[merged_room.location] = room
        # Filter out/delete the merged connections as they make no sense anymore.
        room.connections = [c for c in room.connections if c in connections_to_keep]
        return merged_rooms

    def apply_blank_modifiers(self, modifiers: list[Union[BlankModifier, FrameModifier]]) -> None:
        """
        Apply all blank modifiers to the room grid.
        """
        for modifier in modifiers:
            for location in self.get_all_locations_for_modifier(modifier):
                self._room_map[location].type = RoomType.BLANK

    def apply_closing_modifiers(self, modifiers: list[ClosingModifier]) -> None:
        """
        Apply all closing modifiers to the room grid.
        """
        for modifier in modifiers:
            for location in self.get_all_locations_for_modifier(modifier):
                self._room_map[location].remove_connections(modifier.closing)

    def _try_apply_merge_modifier(self, modifier: Modifier) -> None:
        """
        Try to apply the given merge modifier.

        :param modifier: The modifier to apply.
        """
        grid = self.location_grid_for_modifier(modifier)
        if all(self._room_map[location].type == RoomType.BLANK for location in grid.all_locations()):
            raise ModifierError(modifier, f"The merge modifier tries to merge room in a blank space.")
        if any(not self._room_map[location].size.is_one for location in grid.all_locations()):
            raise ModifierError(modifier, f"The merge modifier overlaps with already merged rooms.")
        self.merge_area(grid)

    def apply_merge_modifiers(self, modifiers: list[MergeModifier]):
        """
        Apply all merge modifiers.
        """
        for modifier in modifiers:
            if modifier.placement == Placement.RANDOM:
                # Random placement may fail, repeat a few times to find a better spot.
                last_error = None
                for _ in range(100):
                    try:
                        self._try_apply_merge_modifier(modifier)
                        last_error = None
                        break
                    except ModifierError as error:
                        last_error = error
                if last_error:
                    raise ModifierError(
                        modifier,
                        "After testing 100 random placement, a merge problem could not get resolved: {error}",
                    ) from last_error
            else:
                self._try_apply_merge_modifier(modifier)

    def remove_blank_rooms(self) -> None:
        """
        Remove all rooms that are marked as blanks.
        """
        rooms_to_remove = list([room for room in self.get_all_rooms() if room.type == RoomType.BLANK])
        for room in rooms_to_remove:
            room.remove_all_connections()
        for room in rooms_to_remove:
            del self._room_map[room.location]

    def reset_rooms_and_connections(self) -> None:
        """
        Reset all rooms and connections to another attempt.
        """
        for room in self.get_all_rooms():
            room.reset()
