import heapq
import math
import pygame
from node import Node
from enum import Enum

class Heuristic(Enum):
    Manhattan = 0,
    Diagonal = 1,
    Euclidean = 2

class PathFinder:
    """Class to find the shortest path using the A* algorithm."""

    def __init__(self, maze, heuristic):
        """
        Initialize the PathFinder with the given maze and heuristic.

        :param maze: The maze object representing the environment.
        :param heuristic: The heuristic function to use.
        """
        self.__maze = maze
        self.__heuristic_func = self.__solve_heuristics(heuristic)

    def calc_path(self, start, end):
        """
        Calculate the shortest path from start to end using the A* algorithm.

        :param start: The starting coordinate (row, col).
        :param end: The ending coordinate (row, col).
        :return: A list of coordinates representing the path from start to end.
        """
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0

        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = set()

        heapq.heappush(open_list, (start_node.f, start_node))

        while open_list:
            current_node = heapq.heappop(open_list)[1]
            closed_list.add(current_node.position)

            if current_node.position == end_node.position:
                return self.__return_path(current_node)

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if not self.__maze.tile_is_walkable(node_position):
                    continue

                new_node = Node(current_node, node_position)
                children.append(new_node)

            for child in children:
                if child.position in closed_list:
                    continue

                child.g = current_node.g + 1
                child.h = self.__heuristic_func(child.position, end_node.position)
                child.f = child.g + child.h

                if any(open_node.position == child.position and child.g > open_node.g for open_node in (n[1] for n in open_list)):
                    continue

                heapq.heappush(open_list, (child.f, child))

        return []

    def __solve_heuristics(self, heuristic):
        """
        Select the heuristic function based on the provided heuristic type.

        :param heuristic: The type of heuristic (Manhattan, Diagonal, Euclidean).
        :return: The corresponding heuristic function.
        """
        if heuristic == Heuristic.Manhattan:
            return self.__heuristic_manhattan_distance
        elif heuristic == Heuristic.Diagonal:
            return self.__heuristic_diagonal_distance
        elif heuristic == Heuristic.Euclidean:
            return self.__heuristic_euclidean_distance

        return self.__heuristic_manhattan_distance

    def __heuristic_euclidean_distance(self, src, dst):
        """
        Calculate the Euclidean distance between two points.

        :param src: The source coordinate (row, col).
        :param dst: The destination coordinate (row, col).
        :return: The Euclidean distance.
        """
        x_dist = abs(src[0] - dst[0])
        y_dist = abs(src[1] - dst[1])
        return 10 * (math.sqrt((x_dist * x_dist) + (y_dist * y_dist)))

    def __heuristic_manhattan_distance(self, src, dst):
        """
        Calculate the Manhattan distance between two points.

        :param src: The source coordinate (row, col).
        :param dst: The destination coordinate (row, col).
        :return: The Manhattan distance.
        """
        x_dist = abs(src[0] - dst[0])
        y_dist = abs(src[1] - dst[1])
        return 10 * (x_dist + y_dist)

    def __heuristic_diagonal_distance(self, src, dst):
        """
        Calculate the Diagonal distance between two points.

        :param src: The source coordinate (row, col).
        :param dst: The destination coordinate (row, col).
        :return: The Diagonal distance.
        """
        x_dist = abs(src[0] - dst[0])
        y_dist = abs(src[1] - dst[1])
        return (10 * (x_dist + y_dist)) + (-6 * min(x_dist, y_dist))

    def __return_path(self, current_node):
        """
        Return the path from the start to the end by backtracking from the current node.

        :param current_node: The end node to backtrack from.
        :return: A list of coordinates representing the path.
        """
        path = []
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent

        return path[::-1]

    def path_to_img(self, path):
        """
        Convert the path to an image for visualization.

        :param path: The list of coordinates representing the path.
        :return: A Pygame Surface with the path drawn on it.
        """
        rows, cols = self.__maze.get_size()
        zoom = self.__maze.get_zoom()
        maze_img = pygame.Surface((cols * zoom, rows * zoom), pygame.SRCALPHA, 32)

        if path:
            for coord in path:
                point = self.__maze.maze_coord_to_screen_point(coord)
                rect = pygame.Rect(point, (zoom, zoom))
                pygame.draw.rect(maze_img, (0, 0, 255, 255), rect)

        return maze_img
