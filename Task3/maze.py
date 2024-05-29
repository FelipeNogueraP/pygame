from os import path

import pygame

class Maze():

    def __init__(self, filename, zoom):
        self.__zoom = zoom
        self.__matrix = self.__load_maze(filename)
        self.__image = self.__create_maze_image()

    def __load_maze(self, filename):
        maze_img = pygame.image.load(path.join(*filename))
        maze = []
        maze_size = maze_img.get_size()

        maze_img.lock()
        for y in range(maze_size[1]):
            row = []
            for x in range(maze_size[0]):
                color = maze_img.get_at((x,y))
                if color == (255, 255, 255, 255):   #walkable
                    row.append(0)
                else:
                    row.append(1)       #wall
            maze.append(row)
        maze_img.unlock()

        return maze

    def __create_maze_image(self):
        rows, cols = self.get_size()
        maze_img = pygame.Surface((cols* self.__zoom, rows * self.__zoom))
        maze_img.lock()
        for row in range(rows):
            for col in range(cols):
                color = (255, 255, 255, 255) if self.tile_is_walkable((row, col)) else (0, 0, 0, 255)
                for x in range(self.__zoom):
                    for y in range(self.__zoom):
                        maze_img.set_at(((col* self.__zoom) + x,(row * self.__zoom) + y), color)
        maze_img.unlock()

        return maze_img

    def get_image(self):
        return self.__image

    def get_zoom(self):
        return self.__zoom

    def get_size(self):
        return len(self.__matrix), len(self.__matrix[0])

    def tile_is_walkable(self, coord):
        return self.__matrix[int(coord[0])][int(coord[1])] == 0

    def screen_point_to_maze_coord(self, point):  # returns row, col
        return int(point[1] / self.__zoom), int(point[0] / self.__zoom)

    def maze_coord_to_screen_point(self, coord):  # returns x,y
        return coord[1] * self.__zoom, coord[0] * self.__zoom
