# code partly copyed from Keith Galli
# https://github.com/KeithGalli/Connect4-Python

from arcade.color import SKY_BLUE, WHITE
import numpy as np
import arcade
import math

BLUE = arcade.csscolor.SKY_BLUE
BLACK = arcade.csscolor.BLACK
WHITE = arcade.csscolor.WHITE
RED = arcade.csscolor.RED
YELLOW = arcade.csscolor.YELLOW
AMAZON = arcade.color.AMAZON
GREEN = arcade.csscolor.LIME_GREEN
# font myfont = pygame.font.SysFont("monospace", 75)

ROW_COUNT = 6
COLUMN_COUNT = 9

SQUARESIZE = 140
RADIUS = int(SQUARESIZE/2 - 15)

SCREEN_WIDTH = COLUMN_COUNT * SQUARESIZE
SCREEN_HEIGHT = ROW_COUNT * SQUARESIZE
SCREEN_TITLE = "connect four"


class Connect4(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.colorPlayer1 = SKY_BLUE
        self.colorPlayer2 = GREEN
        self.colorBackground = WHITE
        self.colorGrid = AMAZON
        arcade.set_background_color(self.colorGrid)

        self.game_over = False
        self.turn = 0

        self.mousePositionX = 0
        self.mousePositionY = 0

    def setup(self):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT))

    def on_draw(self):
        arcade.start_render()
        self.draw_board()
        if not self.game_over:
            self.draw_circle()
        arcade.finish_render()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        # close
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.game_over:
            col = int(math.floor(x/SQUARESIZE))
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)

                if self.turn == 0:
                    self.drop_piece(row, col, 1)

                    if self.winning_move(1):
                        self.game_over = True
                        #arcade.draw_text("Player\n 1 wins!!", 0, SCREEN_HEIGHT-SQUARESIZE/2, self.colorPlayer1,font_size=12, width=600, align="left")
                        print("Player 1 wins !!!")
                else:
                    self.drop_piece(row, col, 2)

                    if self.winning_move(2):
                        self.game_over = True
                        #arcade.draw_text("Player\n 2 wins!!", 0, SCREEN_HEIGHT-SQUARESIZE/2, self.colorPlayer2,font_size=12, width=600, align="left")
                        print("Player 2 wins !!!")

                self.print_board()

                self.turn += 1
                self.turn = self.turn % 2

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mousePositionX = x
        self.mousePositionY = y

    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                arcade.draw_circle_filled(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2), RADIUS, self.colorBackground)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == 1:
                    arcade.draw_circle_filled(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2), RADIUS, self.colorPlayer1)
                elif self.board[r][c] == 2:
                    arcade.draw_circle_filled(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2), RADIUS, self.colorPlayer2)

    def draw_circle(self):
        col = int(math.floor(self.mousePositionX/SQUARESIZE))
        r = self.get_next_open_row(col)
        if r != None:
            if self.turn == 0:
                arcade.draw_circle_filled(int(col*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2), RADIUS, self.colorPlayer1)
            else:
                arcade.draw_circle_filled(int(col*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2), RADIUS, self.colorPlayer2)

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        board = self.board

        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def is_valid_location(self, col):
        return self.board[ROW_COUNT-1][col] == 0


def main():
    game = Connect4(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
