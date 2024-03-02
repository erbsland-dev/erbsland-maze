#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import random

from .generator_setup import GeneratorSetup
from .room import Room


class GeneratorStack:
    """
    A single generator stack, used for the maze algorithm.
    """

    def __init__(self, path_id: int, rooms: list[Room], setup: GeneratorSetup):
        """
        Create a new generator stack.

        :param path_id: The path identifier.
        :param setup: The generator setup
        """
        self.path_id: int = path_id
        self.rooms: list[Room] = rooms
        self.setup: GeneratorSetup = setup

    def last_room(self) -> Room:
        return self.rooms[-1]

    def has_moves_left(self) -> bool:
        """
        Test if this stack has moves left.
        """
        return len(self.rooms) > 1 or self.rooms[0].unused_connections()

    def one_step(self) -> None:
        """
        Progress one step of the maze algorithm for this stack.
        """
        room = self.last_room()
        room.close_blocked_connections()
        unused_connections = room.unused_connections()
        if unused_connections:
            # TODO: Add weights.
            connection = random.choice(unused_connections)
            connection.is_used = True
            target_room = connection.remote_room(room)
            target_room.path_id = self.path_id
            self.rooms.append(target_room)
            target_room.path_length = len(self.rooms)
        elif len(self.rooms) > 1:
            self.rooms.pop()

    @classmethod
    def initialize_room(cls, room: Room, path_id: int, setup: GeneratorSetup) -> "GeneratorStack":
        """
        Initialize the room as startpoint for a new generator stack.

        :param room: The room that is the start point for a path.
        :param path_id: The path id of the new path.
        :param setup: The generator setup.
        :return: The generator stack.
        """
        room.path_id = path_id
        room.path_length = 1
        return cls(path_id=path_id, rooms=[room], setup=setup)
