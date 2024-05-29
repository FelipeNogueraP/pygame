import pygame

from maze import Maze
from pathfinder import PathFinder, Heuristic

class App:

    __zoom = 10
    __maze_filename = ["Task3", "assets", "maze.bmp"]
    __fps = 60

    def __init__(self):
        pygame.init()

        self.__maze = Maze(App.__maze_filename, App.__zoom)

        screen_size = self.__maze.get_image().get_size()
        self.__screen = pygame.display.set_mode(screen_size, 0, 32)

        self.__running = True
        self.__clock = pygame.time.Clock()

        self.__start_coord = (-1.0, -1.0)
        self.__end_coord = (-1.0, -1.0)
        self.__click_to_start = True

        self.__path_img = pygame.Surface((0,0), pygame.SRCALPHA, 32)

        self.__start_img = pygame.Surface((App.__zoom, App.__zoom))
        self.__start_img.fill((0,255,0,255))

        self.__end_img = pygame.Surface((App.__zoom, App.__zoom))
        self.__end_img.fill((255,0,0,255))

        self.__pathfinder = PathFinder(self.__maze, Heuristic.Manhattan)

    def run(self):
        while self.__running:
            delta_time = self.__clock.tick(App.__fps)

            self.__process_events()
            self.__update(delta_time)
            self.__render()

        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coord = self.__maze.screen_point_to_maze_coord(event.pos)
                    if not self.__maze.tile_is_walkable(coord):
                        continue
                    if self.__click_to_start:
                        self.__start_coord = coord
                        self.__click_to_start = False
                    else:
                        self.__end_coord = coord
                        new_path = self.__pathfinder.calc_path(self.__start_coord, self.__end_coord)
                        self.__path_img = self.__pathfinder.path_to_img(new_path)
                        self.__click_to_start = True

    def __update(self, delta_time):
        pass

    def __render(self):
        self.__screen.fill((200, 200, 200))

        self.__screen.blit(self.__maze.get_image(), (0,0))
        self.__screen.blit(self.__path_img, (0,0))

        self.__screen.blit(self.__start_img, self.__maze.maze_coord_to_screen_point(self.__start_coord))
        self.__screen.blit(self.__end_img, self.__maze.maze_coord_to_screen_point(self.__end_coord))

        pygame.display.update()

    def __quit(self):
        pygame.quit()