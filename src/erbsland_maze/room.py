#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from .closing import Closing
from .connection_side import ConnectionSide
from .direction import Direction
from .location_grid import LocationGrid
from .room_connection import RoomConnection
from .room_location import RoomLocation
from .room_size import RoomSize
from .room_type import RoomType
from .wall import Wall


class Room:
    """
    A room in the maze.
    """

    def __init__(self, location: RoomLocation) -> None:
        """
        Create a new 1x2 room.

        :param location: The location of the room.
        """
        self.grid = LocationGrid(location, RoomSize(1, 1))
        self.type = RoomType.PATH  # The type of this room.
        self.connections: list[RoomConnection] = []  # The connections of this room.
        self.path_id = 0  # The ID of the path. 0 = unused, 1-99 = primary paths, 100+ decoy paths.
        self.path_length = 0  # The length of the path.

    def __hash__(self) -> int:
        """
        Room instances are unique regardless of their contents.
        """
        return id(self)

    @property
    def location(self) -> RoomLocation:
        return self.grid.location

    @location.setter
    def location(self, location: RoomLocation) -> None:
        self.grid.location = location

    @property
    def size(self) -> RoomSize:
        return self.grid.size

    @size.setter
    def size(self, size: RoomSize) -> None:
        self.grid.size = size

    @property
    def is_used(self) -> bool:
        return self.path_id != 0

    @property
    def is_primary_path(self):
        return 0 < self.path_id < 100

    @property
    def is_surrounded_by_blanks(self) -> bool:
        """
        Test if the room is surrounded by blank rooms.

        This test is used to check if a room is suitable for a start position. For example, if there is a frame around
        the maze, and the start position is in the corner, this will never work.
        """
        return all(c.remote_room(self).type == RoomType.BLANK for c in self.connections)

    def close_blocked_connections(self) -> None:
        """
        Remove all connections from this room, that are blocked because they lead to already allocated paths.
        """
        blocked_connections = list(
            [
                connection
                for connection in self.connections
                if not connection.is_used and connection.remote_room(self).is_used
            ]
        )
        for connection in blocked_connections:
            connection.is_closed = True
            connection.is_used = True

    def unused_connections(self) -> list[RoomConnection]:
        """
        Get all connections that can be potentially used to create a new path.

        :return: A list of connections.
        """
        return [connection for connection in self.connections if not connection.is_used]

    def is_connected_to_room(self, room: "Room") -> bool:
        """
        Test if this room has a connection to another room.

        :param room: The other room to test.
        :return: `True` if there is a connection between this and the other room.
        """
        for connection in self.connections:
            if not connection.is_closed and connection.remote_room(self) == room:
                return True
        return False

    def get_connection(self, wall: Wall) -> Optional[RoomConnection]:
        """
        Get a connection at the given wall.

        :param wall: The wall.
        :return: The connection at the given wall or `None` if there isn't one.
        """
        for connection in self.connections:
            side = connection.local(self)
            if side.wall == wall:
                return connection
        return None

    def get_connections_in_direction(self, direction: Direction) -> list[RoomConnection]:
        """
        Get all connections that lead to the given direction.

        :param direction: The direction.
        :return: A list of connections.
        """
        return [c for c in self.connections if c.local(self).wall.direction == direction]

    def get_connections_at_location(self, location: RoomLocation) -> list[RoomConnection]:
        """
        Get all connections from a given location inside this room.

        :param location: The location inside of this room.
        :return: A list of connections.
        """
        return [c for c in self.connections if c.local(self).wall.location == location]

    def is_open_connection(self, wall: Wall) -> bool:
        """
        Test if there is an open connection to the given wall.

        :param wall: The wall.
        :return: `True` if there is an open connection.
        """
        if connection := self.get_connection(wall):
            return not connection.is_closed
        return False

    def add_connection(self, location: RoomLocation, direction: Direction, target_room: "Room") -> None:
        """
        Add a connection to another room.

        :param location: The location inside of this room.
        :param direction: The direction for the wall in which this connection is anchored.
        :param target_room: The target room for the connection.
        """
        if not self.grid.contains(location):
            raise ValueError("location is not in this room.")
        local_wall = Wall(location, direction)
        remote_wall = Wall(target_room.location, direction.opposite())
        if self.get_connection(local_wall) is not None:
            raise ValueError("there is already a connection at this point.")
        new_connection = RoomConnection(
            ConnectionSide(self, local_wall),
            ConnectionSide(target_room, remote_wall),
        )
        self.connections.append(new_connection)
        if target_room.get_connection(remote_wall) is not None:
            raise ValueError("the remote room has already a connection back to this room.")
        target_room.connections.append(new_connection)

    def remove_connection(self, connection: RoomConnection) -> None:
        """
        Remove a connection from this room.

        :param connection: The connection to remove.
        """
        connected_room = connection.remote_room(self)
        connected_room.connections.remove(connection)
        self.connections.remove(connection)

    def _adjacent_exit_directions(self, location: RoomLocation) -> list[Direction]:
        """
        Get the adjacent exit directions at the given location.

        :param location: The location.
        :return: A list of directions.
        """
        result: list[Direction] = []
        for direction in Direction:
            if not self.grid.contains(location.advance(direction)):
                result.append(direction)
        return result

    def get_walls(self) -> list[Wall]:
        """
        Get all walls of this room.

        :return: A list of walls.
        """
        result: list[Wall] = []
        for location in self.grid.all_frame_locations():
            for direction in self._adjacent_exit_directions(location):
                result.append(Wall(location, direction))
        return result

    def remove_connections(self, closing: Closing):
        matching_walls: list[Wall] = []
        for wall in self.get_walls():
            if wall.matches_closing_type(closing.closing_type, self.grid) != closing.invert:
                matching_walls.append(wall)
        for wall in matching_walls:
            connection = self.get_connection(wall)
            if connection:
                self.remove_connection(connection)

    def remove_all_connections(self):
        """
        Remove all connections from and to this room.
        """
        for connection in self.connections.copy():
            self.remove_connection(connection)

    def reset(self):
        """
        Reset the room for another solution attempt.
        """
        self.path_id = 0
        self.path_length = 0
        for connection in self.connections:
            connection.reset()
