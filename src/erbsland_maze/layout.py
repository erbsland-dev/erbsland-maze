#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from abc import ABC, abstractmethod
from pathlib import Path

from .room import Room
from .room_size import RoomSize


class Layout(ABC):
    """
    The base class for all graphical layout classes.
    """

    @abstractmethod
    def initialize(self) -> RoomSize:
        """
        Initializes the graphical layout and calculate the number of rooms required to fill the canvas.

        :return: The number of rooms in the X and Y axis.
        """
        pass

    @abstractmethod
    def render_image(self, file_path: Path, rooms: list[Room], path_end_rooms: list[Room]) -> None:
        """
        Render the maze into an image.

        :param file_path: The path for the resulting image.
        :param rooms: A list of rooms to render.
        :param path_end_rooms: The end points in the maze to be marked.
        """
        pass

    @abstractmethod
    def get_dimension_info(self) -> str:
        """
        Get dimensional information to be displayed on the console after initialization.

        :return: Text that contains the most useful dimension information.
        """
        pass
