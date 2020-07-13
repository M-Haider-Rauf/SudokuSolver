"""
    Sudoku solver
    Written by Haider Rauf
    May 28, 2020
    made for Nagato Yuki
"""

import pygame
from sudoku import *

CELL_SIZE = 55  # the scale of box

# board dimension constants
BOARD_WIDTH = CELL_SIZE * 9
BOARD_HEIGHT = CELL_SIZE * 9


class Engine:
    TICK_RATE = 12

    def __init__(self):
        # init pygame stuff
        pygame.init()
        self.display: pygame.Surface = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Sudoku Solver by Haider Rauf")
        self.font = pygame.font.SysFont("consolas", CELL_SIZE)
        self.clock = pygame.time.Clock()

        self.running = True  # game running status
        self.current_selection = (0, 0)  # currently highlighted box
        self.grid = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 9]
        ]  # init the grid

    # helper method for just checking key status since the original method is a bit clunky
    @staticmethod
    def is_key_pressed(
            key: int):  # helper method for just checking key status since the original method is a bit clunky
        if pygame.key.get_pressed()[key]:
            return True
        else:
            return False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # pressing ENTER solves the sudoku
                if event.key == pygame.K_RETURN:
                    # first check if the sudoku is solvable...
                    if can_solve(self.grid):
                        self.current_selection = (9, 9)
                        solve_sudoku(self.grid)
                        print("solved!")
                    else:
                        print("can't solve")

                elif event.key == pygame.K_SPACE:
                    self.grid = [[0 for i in range(9)] for j in range(9)]

                # enter number in grid
                else:
                    (x, y) = self.current_selection
                    for key in range(pygame.K_0, pygame.K_9 + 1):  # only do something if 0-9 keys are pressed
                        if Engine.is_key_pressed(key):  # if any key number key is pressed...
                            self.grid[y][x] = key - pygame.K_0  # calculate the grid value
                            break

        if pygame.mouse.get_pressed()[0]:
            (x, y) = pygame.mouse.get_pos()
            x //= CELL_SIZE
            y //= CELL_SIZE
            self.current_selection = (x, y)

    def update(self):
        # logic so that the selection is warped
        self.current_selection = (self.current_selection[0] % 9, self.current_selection[1] % 9)

    def render(self, x=None, y=None, color=None):
        self.display.fill(pygame.color.Color(0, 0, 0, 255))
        # Begin drawing

        self.draw_grid((255, 255, 255, 255))
        self.draw_numbers(x, y, color)

        # end drawing
        pygame.display.flip()
        self.clock.tick(Engine.TICK_RATE)

    def main_loop(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
        pygame.quit()

    def draw_grid(self, color=(255, 255, 255, 255)):
        # draw vertical lines
        for i in range(1, BOARD_WIDTH // CELL_SIZE):
            if i % 3:  # for main grid
                pygame.draw.line(self.display, (127, 127, 127, 255), (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_HEIGHT))
            else:  # for the thick line for sub-grids
                pygame.draw.line(self.display, color, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_HEIGHT), 5)

        # draw horizontal lines
        for i in range(1, BOARD_HEIGHT // CELL_SIZE):
            if i % 3:  # for main grid
                pygame.draw.line(self.display, (127, 127, 127, 255), (0, i * CELL_SIZE), (BOARD_WIDTH, i * CELL_SIZE))
            else:  # for the thick line for sub-grids
                pygame.draw.line(self.display, color, (0, i * CELL_SIZE), (BOARD_WIDTH, i * CELL_SIZE), 5)

    def draw_numbers(self, x=None, y=None, color=None):
        for i in range(BOARD_HEIGHT // CELL_SIZE):
            for j in range(BOARD_WIDTH // CELL_SIZE):
                # if current cell isn't empty...
                if self.grid[i][j]:  # draw number here
                    text_surf = self.font.render(str(self.grid[i][j]), True, (255, 255, 255, 255))
                    self.display.blit(text_surf, (j * CELL_SIZE + 14, i * CELL_SIZE + 4))
                # if current cell is selected, draw red box around it...
                if (i, j) == self.current_selection:
                    self.draw_frame(i, j, (0, 0, 255, 255))
                if x is not None and y is not None and color is not None:
                    self.draw_frame(x, y, color)

    def draw_frame(self, x, y, color):
        pygame.draw.rect(self.display, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)


def main():
    # init the engine and run the main loop
    engine = Engine()
    solve_sudoku.engine = engine
    engine.main_loop()


if __name__ == '__main__':
    main()
