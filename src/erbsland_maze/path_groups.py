#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later


class PathGroups:
    """
    Implementation of the union find algorithm to test for connected paths.

    .. note::
        This implementation is written for very small sets, as the `member_of` method will scan each
        entry and find the root of it.
    """

    def __init__(self):
        """
        Create a new ConnectedPaths object.
        """
        self.parent: dict[int, int] = {}

    def are_connected(self, path_a: int, path_b: int) -> bool:
        """
        Test if two paths are connected.

        :param path_a: The first path identifier to test.
        :param path_b: The second path identifier to test.
        :return: `True` if the two paths are connected.
        """
        return self.find_root(path_a) == self.find_root(path_b)

    def find_root(self, path_id: int) -> int:
        """
        Find the group-root of a path id.

        :param path_id: The path identifier to find.
        :return: The identifier of the group.
        """
        if path_id not in self.parent:
            self.parent[path_id] = path_id
        if path_id != self.parent[path_id]:
            self.parent[path_id] = self.find_root(self.parent[path_id])
        return self.parent[path_id]

    def union(self, path_a: int, path_b: int) -> None:
        """
        Join two connected path.

        :param path_a: The identifier of the first path.
        :param path_b: The identifier of the second path.
        :return:
        """
        root_x = self.find_root(path_a)
        root_y = self.find_root(path_b)
        if root_x != root_y:
            self.parent[root_x] = root_y

    def members_of(self, path_id) -> set[int]:
        """
        Get all member of the group where the given path belongs to.

        :param path_id: The identifier of the path.
        :return: A set with all the members of the path.
        """
        root = self.find_root(path_id)
        return {node for node in self.parent if self.find_root(node) == root}

    def roots(self) -> set[int]:
        """
        Get all roots, and therefore all groups.
        """
        return {self.find_root(node) for node in self.parent}
