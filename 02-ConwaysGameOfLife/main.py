from numpy import add
import pygame as pg
from GameofLife import GameofLife
import random
import time

# if the imports make trouble use pip install ...

# features:
# - press the Spacebar to start, pause and resume the game
# - you can edit the grid of cells by clicking on individual cells (left click to make a cell alive, right click to kill a cell)
# - press n to clear the grid
# - press r to reset the grid with new random values

# colors
random_color = (random.randint(1, 254), random.randint(1, 254), random.randint(0, 254))
green = (67, 245, 94, 96)
light_green = (207, 255, 171)
black = (0, 0, 0)
white = (255, 255, 255)
rose = (249, 217, 245)
rose_darker = (249, 154, 245)
grey = (196, 195, 190)


# see for yourself what you can edit here
# wrap around means the opposing edges of the grid are connected
# the alternative is that the cells beyond the border are always treated as if they were dead
conway = GameofLife(
    random=True,
    cell_size=11,
    rows=80,
    columns=140,
    wrap_around=True,
    line_thickness=1,
    background_color=black,
    line_color=(40, 40, 40),
    cell_color=white,
)

tickrate = 10


def main():
    pg.init()

    run = True
    play = False
    pressed = False
    conway.draw_grid()

    while run:
        for event in pg.event.get():
            # quitting the game
            if event.type == pg.QUIT:
                run = False
            # toggle play/pause
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    t0 = time.perf_counter()
                    play = not play
                elif event.key == pg.K_n:
                    conway.random = False
                    conway.newGrid()
                elif event.key == pg.K_r:
                    conway.random = True
                    conway.newGrid()

            # mouseclick for input
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                state = pg.mouse.get_pressed()
                conway.newInput(mouseX, mouseY, add=state[0])

            elif event.type == pg.MOUSEMOTION:
                state = pg.mouse.get_pressed()
                if any(state):
                    mouseX, mouseY = pg.mouse.get_pos()
                    conway.newInput(mouseX, mouseY, add=state[0])

            # zooming with mousewheel doesn't work
            elif event.type == pg.MOUSEWHEEL:
                conway.changeZoom(event.y)

            # elif event.type == pg.KEYDOWN:
            #    if event.key == pg.K_f:
            #        pg.display.toggle_fullscreen()

        if play:
            # copied from Lentil#1133
            if time.perf_counter() > t0 + 1 / tickrate:
                t0 += 1 / tickrate
                conway.run()
    pg.quit()


if __name__ == "__main__":
    main()
