class Node:
    """A class representing a node in the A* algorithm."""

    def __init__(self, parent, position):
        """
        Initialize the node.

        :param parent: The parent node of this node.
        :param position: The position of this node (row, col).
        """
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        """
        Compare this node to another node.

        :param other: The other node to compare to.
        :return: True if the nodes are equal, False otherwise.
        """
        return self.position == other.position

    def __lt__(self, other):
        """
        Compare the f cost of this node to another node.

        :param other: The other node to compare to.
        :return: True if this node has a lower f cost, False otherwise.
        """
        return self.f < other.f
