from numpy.random import rand
import pygame as pg
import numpy as np
from scipy.signal import correlate2d


class GameofLife:
    def __init__(self, background_color, line_color, cell_color, random=True, cell_size=100, rows=10, columns=10, line_thickness=1, wrap_around=True):
        # general stuff
        self.grid_size = (rows, columns)
        self.cell_size = cell_size
        self.grid_line_thickness = line_thickness
        self.rows = rows
        self.columns = columns
        self.wrap_around = wrap_around
        self.random = random

        self.iterations = 0

        # colors
        self.background_color = background_color
        self.line_color = line_color
        self.cell_color = cell_color

        # window dimension in pixels
        self.width = columns * self.cell_size + \
            (columns-1) * self.grid_line_thickness
        self.height = rows * self.cell_size + \
            (rows-1) * self.grid_line_thickness

        # init window
        self.window = pg.display.set_mode(
            (self.width, self.height), pg.RESIZABLE, pg.HWSURFACE)  # pg.FULLSCREEN pg.RESIZABLE
        self.caption = f"Conway's Game of Life ({columns}, {rows})"
        pg.display.set_caption(self.caption)

        # init grid data
        if self.random:
            # randomized grid
            self.grid = np.random.randint(2, size=self.grid_size)
        else:
            # empty grid
            self.grid = np.zeros(self.grid_size)

    def run(self):
        self.iterations += 1
        pg.display.set_caption(self.caption + " " + str(self.iterations))

        # boundary conditions
        if self.wrap_around:
            self.update_grid_wrap_around()
        else:
            self.update_grid_strict_border()

        self.draw_grid()

    def draw_grid(self):
        self.window.fill(self.background_color)

        # draw vertical lines
        x = self.cell_size
        for i in range(self.columns):
            pg.draw.line(self.window, self.line_color, (x, 0),
                         (x, self.height), self.grid_line_thickness)
            x += self.grid_line_thickness + self.cell_size

        # draw horizontal lines
        y = self.cell_size
        for i in range(self.rows):
            pg.draw.line(self.window, self.line_color, (0, y),
                         (self.width, y), self.grid_line_thickness)
            y += self.grid_line_thickness + self.cell_size

        # draw cells
        self.offset = (self.cell_size + self.grid_line_thickness)
        for index, x in np.ndenumerate(self.grid):
            if (x == 1):
                pg.draw.rect(self.window, self.cell_color,
                             (index[1]*self.offset, index[0]*self.offset, self.cell_size, self.cell_size))

        pg.display.update()

    def update_grid_strict_border(self):
        updated_grid = self.grid.copy()

        kernel = np.ones((3, 3))
        kernel[1, 1] = 0

        # array where each value is the number of neighbours
        neighbours = correlate2d(updated_grid, kernel, 'same')

        # rules
        updated_grid[(self.grid == 1) & (
            (neighbours < 2) | (neighbours > 3))] = 0
        updated_grid[(self.grid == 0) & (neighbours == 3)] = 1

        self.grid = updated_grid.copy()

    def update_grid_wrap_around(self):
        updated_grid = self.grid.copy()

        # add the top row at the bottom
        extended_grid = np.append(updated_grid, [updated_grid[0]], axis=0)
        # add the bottom row at the top
        extended_grid = np.append([updated_grid[-1]], extended_grid, axis=0)
        # add the left column at the right
        extended_grid = np.append(
            extended_grid, np.transpose([extended_grid[:, 0]]), axis=1)
        # add the right column at the left
        extended_grid = np.append(np.transpose(
            [extended_grid[:, -2]]), extended_grid, axis=1)

        kernel = np.ones((3, 3))
        kernel[1, 1] = 0

        # array where each value is the number of neighbours
        neighbours = correlate2d(extended_grid, kernel, 'same')[1:-1, 1:-1]

        # rules
        updated_grid[(self.grid == 1) & (
            (neighbours < 2) | (neighbours > 3))] = 0
        updated_grid[(self.grid == 0) & (neighbours == 3)] = 1

        self.grid = updated_grid.copy()

    def insert_at(self, pos, to_insert_arr):
        x1 = pos[0]
        y1 = pos[1]
        x2 = x1 + to_insert_arr.shape[0]
        y2 = y1 + to_insert_arr.shape[1]

        assert x2 <= to_insert_arr.shape[0], "the position will make the small matrix exceed the boundaries at x"
        assert y2 <= to_insert_arr.shape[1], "the position will make the small matrix exceed the boundaries at y"

        self.grid[x1:x2, y1:y2] = to_insert_arr

        self.draw_grid()

    def newInput(self, mouseX, mouseY, add=True):
        index_in_grid = (int(mouseY/self.offset),
                         int(mouseX/self.offset))

        if add:
            self.grid[index_in_grid] = 1
        else:
            self.grid[index_in_grid] = 0

        self.draw_grid()

    def newGrid(self):
        if self.random:
            # randomized grid
            self.grid = np.random.randint(2, size=self.grid_size)
        else:
            # empty grid
            self.grid = np.zeros(self.grid_size)

        self.iterations = 0
        pg.display.set_caption(self.caption + " " + str(self.iterations))
        self.draw_grid()
