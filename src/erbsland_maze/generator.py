#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import sys
from itertools import product, combinations
from pathlib import Path
from typing import Optional

from .about import VERSION
from .error_mark import ErrorMark
from .generator_error import GeneratorError, NoValidSolutionError
from .generator_setup import GeneratorSetup
from .generator_stack import GeneratorStack
from .layout import Layout
from .path_groups import PathGroups
from .path_join_info import PathJoinInfo
from .path_pair import PathPair
from .placement import Placement
from .room import Room
from .room_grid import RoomGrid
from .room_location import RoomLocation
from .room_size import RoomSize
from .room_type import RoomType


class Generator:
    """
    The maze generator.
    """

    def __init__(self, layout: Layout, setup: GeneratorSetup = GeneratorSetup()):
        """
        Create a new instance of the maze generator.

        :param layout: The graphical layout for the maze to generate.
        :param setup: The setup for the generator.
        """
        if not isinstance(layout, Layout):
            raise TypeError("graphical_layout must be a GraphicalLayout instance.")
        if not isinstance(setup, GeneratorSetup):
            raise TypeError("generator_setup must be a GeneratorSetup instance.")
        self.layout: Optional[Layout] = layout
        self.setup: GeneratorSetup = setup
        #
        size = self.layout.initialize()
        self.room_grid = RoomGrid(size)  # Create the room grid with the calculated size.
        self.path_end_rooms: list[Room] = []  # The rooms associated with the path ends.
        self.error_marks: list[ErrorMark] = []  # Error marks for the output.

    def print_info(self):
        """
        Print the welcome message and basic infos about the generated maze.
        """
        if not self.setup.verbose:
            return
        print(f"Erbsland Maze - V{VERSION}")
        print(f"  Layout: {self.layout.get_dimension_info()}")
        print(f"  Room count: {self.room_grid.size.width} x {self.room_grid.size.height}")

    def raise_generator_error(self, message: str, location: RoomLocation, size: RoomSize = RoomSize(1, 1)):
        if self.setup.ignore_errors:
            self.error_marks.append(ErrorMark(location, size=size, message=message))
            print(message, file=sys.stderr)
        else:
            raise GeneratorError(message)

    def raise_not_valid_solution_error(self, message: str):
        if self.setup.ignore_errors:
            print(message, file=sys.stderr)
        else:
            raise NoValidSolutionError(message)

    def _prepare_path_ends(self) -> None:
        """
        Prepare the locations of the start and end rooms.
        """
        for path_end in sorted(self.setup.path_ends, key=lambda path_end: path_end.placement.order_value):
            location = self.room_grid.get_location_for_path_end(path_end)
            room = self.room_grid[location]
            if path_end.placement == Placement.RANDOM and room.type != RoomType.PATH:
                # For random placements, do a few attempts to find a better spot.
                for _ in range(100):
                    if room.type == RoomType.PATH and not room.is_surrounded_by_blanks:
                        break
                    location = self.room_grid.get_location_for_path_end(path_end)
                    room = self.room_grid[location]
            if room.is_surrounded_by_blanks:
                self.raise_generator_error(
                    f"The configured path end '{path_end}' seems to end up in a spot at location ({location}) with "
                    "no connections to other paths. Check your configuration. If the placement is random, 100 "
                    "attempts to find a better spot were unsuccessful.",
                    room.location,
                    room.size,
                )
            if room.type == RoomType.END:
                self.raise_generator_error(
                    f"The configured path end '{path_end}' collides with another path end and would end up in the "
                    f"same room at location ({location}). Check your configuration. If the placement is random, "
                    "100 attempts to find a better spot were unsuccessful.",
                    room.location,
                    room.size,
                )
            room.type = RoomType.END
            self.path_end_rooms.append(room)

    def _verify_preparations(self):
        """
        Make sure the prepared room structure can be filled with a maze.
        """
        # First check that each end point starts in a different room.
        room_indices = {}
        for index, room in enumerate(self.path_end_rooms):
            if room in room_indices:
                self.raise_generator_error(
                    f"The end-points {index + 1} and {room_indices[room] + 1} ending up in the same room. Make sure "
                    "they are placed at different locations and room merging does not merge two end-points into one.",
                    room.location,
                    room.size,
                )
            room_indices[room] = index

    def prepare_rooms(self) -> None:
        """
        Prepare the rooms and connections between them.
        """
        if self.setup.verbose:
            print("Preparing rooms...")
        self.room_grid.fill_with_rooms()
        self.room_grid.apply_blank_modifiers(self.setup.modifiers.get_frame_modifiers())
        self.room_grid.apply_blank_modifiers(self.setup.modifiers.get_blank_modifiers())
        self.room_grid.connect_all_rooms()
        self.room_grid.apply_merge_modifiers(self.setup.modifiers.get_merge_modifiers())
        self.room_grid.apply_closing_modifiers(self.setup.modifiers.get_closing_modifiers())
        self._prepare_path_ends()
        self.room_grid.remove_blank_rooms()
        self._verify_preparations()

    def generate_maze(self) -> None:
        """
        Generate the paths for the main maze that connects the start and end point.
        """
        if self.setup.verbose:
            print("Generating the paths for the maze...")
        generator_stacks = [
            GeneratorStack.initialize_room(room, index + 1, self.setup)
            for index, room in enumerate(self.path_end_rooms)
        ]
        while any(generator_stack.has_moves_left() for generator_stack in generator_stacks):
            for generator_stack in generator_stacks:
                generator_stack.one_step()

    def get_unused_room(self) -> Optional[Room]:
        """
        Search for a room that is not in use.
        """
        for room in self.room_grid.get_all_rooms():
            if not room.is_used:
                return room

    def fill_islands(self) -> None:
        """
        If there are isolated areas that have no paths, fill them with decoy paths.
        """
        if self.setup.verbose:
            print("Filling islands...")
        path_id = 101
        while unused_room := self.get_unused_room():
            generator_stack = GeneratorStack.initialize_room(unused_room, path_id, self.setup)
            while generator_stack.has_moves_left():
                generator_stack.one_step()

    def verify_maze(self) -> None:
        """
        Do basic verifications of the generated maze, to make sure there are no issues in the algorithm.
        """
        if self.setup.verbose:
            print("Verifying generated paths...")
        for room in self.room_grid.get_all_rooms():
            if not room.is_used:
                self.raise_generator_error(
                    f"Found a room that is not in use. Location: {room.location}", room.location, room.size
                )
            if not room.connections:
                self.raise_generator_error(
                    f"Found a room without exits. Location: {room.location}", room.location, room.size
                )

    def connect_longest_path(self) -> None:
        """
        Connect the longest path to join the two individually generated mazes.

        To make the maze as difficult as possible, the algorithm searches the best spot to create the longest path
        between all ends. It first tries to connect the ends in the defined sequence (1-2, 2-3. 3-4). This ideal
        solution may not be possible. So if e.g. path 1 cannot be connected to path 2, the algorithm tries to connect
        it with path 3, as this path will eventually be connected to path 2 and therefore connect its endpoint.

        In a next step, if there are dead-ends, the algorithm tries to cut off a portion of a such dead-end, if
        this will allow to make a connection between the two paths.

        Yet, if for some reason a path cannot be connected to any other primary paths, the process stops with an
        error.
        """
        if self.setup.verbose:
            print("Connect all paths...")
        best_joins: dict[PathPair, PathJoinInfo] = {}
        for connection in self.room_grid.get_join_candidates():
            join_info = connection.get_path_join_info()
            old_join_info = best_joins.get(join_info.paths)
            if old_join_info is None or join_info.total_length > old_join_info.total_length:
                best_joins[join_info.paths] = join_info

        # Stage 1
        paths_to_connect = list(
            [index + 1 for index, path_end in enumerate(self.setup.path_ends) if not path_end.is_dead_end]
        )
        path_groups = PathGroups()
        for path_a, path_b in combinations(paths_to_connect, r=2):
            if path_groups.are_connected(path_a, path_b):
                continue  # Skip already connected paths.
            group_a, group_b = path_groups.members_of(path_a), path_groups.members_of(path_b)
            joins = [PathPair(path_a, path_b) for path_a, path_b in product(group_a, group_b)]
            longest_join_info = max(
                (best_joins.get(paths) for paths in joins if best_joins.get(paths) is not None),
                key=lambda join_info: join_info.total_length,
                default=None,
            )
            if longest_join_info:
                longest_join_info.connection.is_closed = False
                if self.setup.verbose:
                    print(f"  - successfully joined paths {longest_join_info.paths}")
                path_groups.union(longest_join_info.paths.a, longest_join_info.paths.b)

        # TODO: Stage 2
        # if len(roots := path_groups.roots()) > 1:
        #     print(f"  There are {len(roots)} unconnected path groups to be joined.")

        # Final check
        if len(roots := path_groups.roots()) > 1:
            unconnected_groups = []
            for root in roots:
                unconnected_groups.append(", ".join([str(x) for x in path_groups.members_of(root)]))
            unconnected_paths_str = "(" + "), (".join(unconnected_groups) + ")"
            self.raise_not_valid_solution_error(
                "Could not join all paths with any other end points that are not marked "
                "as dead-ends. Make sure there is a path between all end points. The unconnected path "
                f"groups are: {unconnected_paths_str}"
            )

    def generate_output(self, path: Path):
        """
        Render the output from the generated maze.

        :param path: The output path file.
        """
        if self.setup.verbose:
            print("Rendering image...")
        self.layout.render_image(path, list(self.room_grid.get_all_rooms()), self.path_end_rooms)

    def generate_and_save(self, path: Path):
        """
        Generate and save the maze in the specified format.

        :param path: The output path for the image.
        """
        self.print_info()
        self.prepare_rooms()
        if self.setup.layout_only:
            self.generate_output(path)
            return
        for attempt in range(self.setup.maximum_attempts):
            if self.setup.verbose:
                print(f"{attempt + 1}. attempt to find a solution.")
            try:
                self.generate_maze()
                if self.setup.allow_islands:
                    self.fill_islands()
                self.verify_maze()
                self.connect_longest_path()
                break
            except NoValidSolutionError:
                if attempt == self.setup.maximum_attempts - 1:
                    raise
                self.room_grid.reset_rooms_and_connections()
        self.generate_output(path)
