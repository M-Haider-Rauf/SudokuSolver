import pygame
import math
from sudoku import *

# board dimension constants
BOARD_WIDTH: int = 405
BOARD_HEIGHT: int = 405
SCALE = 45  # the scale of box


class Engine:
    def __init__(self):
        # init pygame stuff
        pygame.init()
        self.display: pygame.Surface = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        pygame.display.set_caption("Sudoku Solver by haider_rauf")
        self.clock: pygame.time = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", SCALE)

        self.running = True  # game running status
        self.current_selection = (0, 0)  # currently highlighted box
        self.grid = [[0 for i in range(9)] for j in range(9)]  # init the grid

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # pressing ENTER solves the sudoku
                if event.key == pygame.K_RETURN:
                    # first check if the sudoku is solvable...
                    if can_solve(self.grid):
                        solve_sudoku(self.grid)
                        print("solved!")
                    else:
                        print("can't solve")

                # move the target box via arrow keys
                # update which row / col of sudoku boards is selected
                # up / down means y-=1 / y+=1 and left / right means x-=1 /x+=1
                elif event.key == pygame.K_UP:
                    self.current_selection = (self.current_selection[0], self.current_selection[1] - 1)
                elif event.key == pygame.K_DOWN:
                    self.current_selection = (self.current_selection[0], self.current_selection[1] + 1)
                elif event.key == pygame.K_LEFT:
                    self.current_selection = (self.current_selection[0] - 1, self.current_selection[1])
                elif event.key == pygame.K_RIGHT:
                    self.current_selection = (self.current_selection[0] + 1, self.current_selection[1])

                # SPACE key resets board (fill list with zeros i.e. empty)
                elif event.key == pygame.K_SPACE:
                    self.grid = [[0 for i in range(9)] for j in range(9)]

                # enter number in grid
                else:
                    keys_pressed = pygame.key.get_pressed()  # get keyboard status
                    (y, x) = self.current_selection
                    for key in range(pygame.K_0, pygame.K_9 + 1):  # only do something if 0-9 keys are pressed
                        if keys_pressed[key]:  # if any key number key is pressed...
                            self.grid[y][x] = key - pygame.K_0   # calculate the grid value
                            break

    def update(self):
        # logic so that the selection is warped
        self.current_selection = (self.current_selection[0] % 10, self.current_selection[1] % 10)
        self.clock.tick(30)

    def render(self):
        self.display.fill(pygame.color.Color(0, 0, 0, 255))
        self.draw_grid((255, 255, 0, 255))

        # draw numbers on grid
        for i in range(BOARD_HEIGHT // SCALE):
            for j in range(BOARD_WIDTH // SCALE):
                # if current cell isn't empty...
                if self.grid[i][j]:  # draw number here
                    text_surf = self.font.render(str(self.grid[i][j]), True, (0, 0, 255, 255))
                    self.display.blit(text_surf, (i * SCALE + 7, j * SCALE + 0))
                # if current cell is selected, draw red box around it...
                if (i, j) == self.current_selection:
                    pygame.draw.rect(self.display, (255, 0, 0, 255), (i * SCALE, j * SCALE, SCALE, SCALE), 3)

        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
        pygame.quit()

    def draw_grid(self, color=(255, 255, 255, 255)):
        # draw vertical lines
        for i in range(1, BOARD_WIDTH // SCALE):
            if i % 3:
                pygame.draw.line(self.display, color, (i * SCALE, 0), (i * SCALE, BOARD_HEIGHT))
            else:  # for the thick line for sub-grids
                pygame.draw.line(self.display, color, (i * SCALE, 0), (i * SCALE, BOARD_HEIGHT), 5)

        # draw horizontal lines
        for i in range(1, BOARD_HEIGHT // SCALE):
            if i % 3:
                pygame.draw.line(self.display, color, (0, i * SCALE), (BOARD_WIDTH, i * SCALE))
            else:  # for the thick line for sub-grids
                pygame.draw.line(self.display, color, (0, i * SCALE), (BOARD_WIDTH, i * SCALE), 5)


def main():
    # init the engine and run the main loop
    engine = Engine()
    engine.main_loop()


if __name__ == '__main__':
    main()
