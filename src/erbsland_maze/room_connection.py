#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .connection_side import ConnectionSide
from .path_join_info import PathJoinInfo
from .path_pair import PathPair


@dataclass
class RoomConnection:
    """
    A connection between two rooms.
    """

    a: ConnectionSide
    b: ConnectionSide
    is_used = False
    is_closed = False

    def __hash__(self):
        return id(self)  # Connections are unique regardless of its contents.

    @property
    def connects_two_paths(self) -> bool:
        """
        Test if this connection connects two paths.
        """
        return self.a.room.path_id != self.b.room.path_id

    @property
    def connects_primary_paths(self) -> bool:
        """
        Test if this connection connects primary paths and no decoy paths.
        """
        return self.a.room.path_id < 100 and self.b.room.path_id < 100

    @property
    def total_path_length(self) -> int:
        """
        Get the total path length at this connection.
        """
        return self.a.room.path_length + self.b.room.path_length

    def get_path_join_info(self) -> PathJoinInfo:
        """
        A method, to get a key for the path joining info.

        :return: A tuple containing the two path ids and the total path length.
        """
        return PathJoinInfo(PathPair(self.a.room.path_id, self.b.room.path_id), self.total_path_length, self)

    def local(self, my_room: "Room") -> ConnectionSide:
        """
        Get my local side of the connection.

        :param my_room: My room to get the side of.
        :return: The connection side.
        """
        if my_room == self.a.room:
            return self.a
        return self.b

    def remote(self, my_room: "Room") -> ConnectionSide:
        """
        Get the remote side of the connection.

        :param my_room: My room, to get the remote side from.
        :return: The connection side.
        """
        if my_room == self.a.room:
            return self.b
        return self.a

    def remote_room(self, my_room: "Room") -> "Room":
        """
        Shortcut to get the remote room.

        :param my_room: My room.
        :return: The remote room.
        """
        return self.remote(my_room).room

    def replace_room(self, old_room: "Room", new_room: "Room") -> None:
        """
        Replace a room in this connection.

        :param old_room: The old room.
        :param new_room: The new room.
        """
        if self.a.room == old_room:
            self.a.room = new_room
        if self.b.room == old_room:
            self.b.room = new_room

    def reset(self):
        """
        Reset the connection for another solution attempt.
        """
        self.is_used = False
        self.is_closed = False
