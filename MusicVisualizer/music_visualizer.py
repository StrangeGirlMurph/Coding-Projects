# multiline comments Crtl + K + C (undo + U)

import arcade
import librosa
import librosa.display
import numpy as np
from scipy.signal import savgol_filter, resample
import math

# options
RECTANGLE = "rect"
CIRCLE = "circle"
CIRCLE_OUTLINE = "circle_outline"
LINE = "line"
POINT_GRAPH = "point_graph"
LINE_GRAPH = "line_graph"
KLEIN_BOTTLE = "klein_bottle"
CHANGING_SHAPES = "changing_shapes"
TESSERACT = "tesseract"

# Constants
DEFAULT_WIDTH = 1100
DEFAULT_HEIGHT = 700
SCREEN_TITLE = "music visualizer"

# pictures
KLEIN_BOTTLE_SPRITE = arcade.Sprite("media/Klein_bottle.png", scale=1, center_x=DEFAULT_WIDTH/2, center_y=DEFAULT_HEIGHT/2)

# songs
INDUSTRY_BABY = "source/INDUSTRY_BABY_feat_Jack_Harlow.wav"  # put your song here
ALIEN_BOY = "source/Alien_Boy.wav"
ALL_IN_ALL = "source/All_in_all.wav"
BOYS = "source/Boys.wav"
SUICIDE_YEAR = "source/SUICIDE_YEAR.wav"


FPS = 60  # (refresh rate of the visualizer)

# how to add a new visualizer:
# 1. create a constant for it under options
# 2. add a key in on_key_press()
# 3. add it to one of the on_update options
# 4. create a draw function and add that function to the draw function
# 5. edit the readme


class Visualizer(arcade.Window):
    def __init__(self, default):
        super().__init__(DEFAULT_WIDTH, DEFAULT_HEIGHT, SCREEN_TITLE, update_rate=1/FPS, resizable=True)
        arcade.set_background_color(arcade.csscolor.WHITE)
        self.color = arcade.csscolor.LIME

        # window
        self.CENTER_X = DEFAULT_WIDTH//2
        self.CENTER_Y = DEFAULT_HEIGHT//2

        # sound stuff
        self.player = None

        # logic stuff
        self.frameNumber = 0
        self.numberOfLastDrawnFrame = 0
        self.cycle = 0  # for changing shapes
        self.part = 0  # part of the audio time series that the song is currently at
        self.pause = False
        self.option = default

        self.value = 0  # the value at this part
        self.points = []  # self.points for the line strip graph or the point graph

    def setup(self, song):
        # enter the song here:
        self.song = arcade.Sound(song)

        self.AUDIO_TIME_SERIES, self.SAMPLING_RATE = librosa.load(song)
        # TEMPO, BEAT_FRAMES = librosa.beat.beat_track(y=self.AUDIO_TIME_SERIES, sr=self.SAMPLING_RATE)
        # BEATS = librosa.frames_to_time(BEAT_FRAMES, sr=SAMPLING_RATE)
        self.smooth = savgol_filter(abs(self.AUDIO_TIME_SERIES), window_length=2001, polyorder=3) * 2
        self.tesseract = Tesseract()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.CENTER_X = self.SCREEN_WIDTH//2
        self.CENTER_Y = self.SCREEN_HEIGHT//2
        print(f"Window resized to: {width}, {height}")

        KLEIN_BOTTLE_SPRITE.center_x = self.CENTER_X
        KLEIN_BOTTLE_SPRITE.center_y = self.CENTER_Y

    # handle keyboard input
    def on_key_press(self, key, modifiers):
        # pause and resume
        if key == arcade.key.SPACE:
            if not self.pause:
                self.player.pause()
            else:
                self.player.play()
            self.pause = not self.pause
            return

        # close
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            # arcade.exit()

        # changing visualizer
        if key == arcade.key.R:
            self.option = RECTANGLE
        elif key == arcade.key.C:
            self.option = CIRCLE
        elif key == arcade.key.O:
            self.option = CIRCLE_OUTLINE
        elif key == arcade.key.L:
            self.option = LINE
        elif key == arcade.key.P:
            self.points.clear()
            self.option = POINT_GRAPH
        elif key == arcade.key.G:
            self.points.clear()
            self.option = LINE_GRAPH
        elif key == arcade.key.K:
            self.option = KLEIN_BOTTLE
        elif key == arcade.key.S:
            self.option = CHANGING_SHAPES
        elif key == arcade.key.T:
            self.option = TESSERACT
        else:
            return
        print(f'Choosen visualizer: {self.option}')

    # updating and drawing
    def on_update(self, delta_time):
        if not self.pause:
            self.part = int(self.song.get_stream_position(self.player) * self.SAMPLING_RATE)

            if self.option in (POINT_GRAPH, LINE_GRAPH):
                self.update_points(self.smooth)
            elif self.option in (RECTANGLE, CIRCLE, CIRCLE_OUTLINE, LINE, KLEIN_BOTTLE, CHANGING_SHAPES):
                self.update_single_value(self.smooth)
            elif self.option == TESSERACT:
                self.update_single_value(self.smooth)
                self.tesseract.angle += self.tesseract.speed * self.value * 2
                if self.value < 0.4:
                    self.tesseract.angle += 0.015
            self.frameNumber += 1

    def on_draw(self):
        if self.frameNumber > self.numberOfLastDrawnFrame:
            arcade.start_render()  # ---

            if self.option == RECTANGLE:
                self.draw_rect()
            elif self.option == CIRCLE:
                self.draw_circle()
            elif self.option == CIRCLE_OUTLINE:
                self.draw_circle_outline()
            elif self.option == LINE:
                self.draw_line()
            elif self.option == POINT_GRAPH:
                self.draw_graph_points()
            elif self.option == LINE_GRAPH:
                self.draw_graph_line_strip()
            elif self.option == KLEIN_BOTTLE:
                self.draw_klein_bottle()
            elif self.option == CHANGING_SHAPES:
                self.draw_changing_shapes()
            elif self.option == TESSERACT:
                self.draw_tesseract()

            arcade.finish_render()  # ---
            self.numberOfLastDrawnFrame = self.frameNumber

    # update functions
    def update_points(self, audio_signal):
        self.points.append([self.SCREEN_WIDTH, self.CENTER_Y - self.CENTER_Y/2 + audio_signal[self.part] * self.CENTER_Y])

        self.points = np.array(self.points)
        self.points[:, 0] = self.points[:, 0] - 2  # shift all the self.points to the left

        # delete all the self.points that are outside of the window
        self.points = np.delete(self.points, np.where(self.points[:, 0] < 0), axis=0)
        self.points = self.points.tolist()

    def update_single_value(self, audio_signal):
        self.value = abs(audio_signal[self.part])

    # draw functions
    def draw_graph_line_strip(self):
        arcade.draw_line_strip(self.points, color=self.color, line_width=2)

    def draw_graph_points(self):
        arcade.draw_points(self.points, color=self.color, size=3)

    def draw_rect(self):
        arcade.draw_rectangle_filled(self.CENTER_X, self.CENTER_Y, 800 * self.value, 200, color=self.color)

    def draw_line(self):
        arcade.draw_line(self.CENTER_X, self.CENTER_Y, self.CENTER_X + 400 * self.value, self.CENTER_Y, line_width=8, color=self.color)
        arcade.draw_line(self.CENTER_X, self.CENTER_Y, self.CENTER_X - 400 * self.value, self.CENTER_Y, line_width=8, color=self.color)

    def draw_circle_outline(self):
        arcade.draw_circle_outline(self.CENTER_X, self.CENTER_Y, 250 * self.value, color=self.color, border_width=5)

    def draw_circle(self):
        arcade.draw_circle_filled(self.CENTER_X, self.CENTER_Y, 250 * self.value, color=self.color)

    def draw_klein_bottle(self):
        KLEIN_BOTTLE_SPRITE.scale = self.value * 2
        KLEIN_BOTTLE_SPRITE.draw()
        # sound

    def draw_changing_shapes(self):
        # sensitivity = 1000
        # if self.part < BEAT_FRAMES[np.where(BEAT_FRAMES < self.part)][-1] + sensitivity:
        #     self.cycle += 1
        #     print("next shape")

        if self.frameNumber % 20 <= .5 and self.value >= 0.8:
            self.cycle += 1

        # reset if necessary
        if self.cycle == 3:
            self.cycle = 0

        # drawing
        if self.cycle == 0:
            self.draw_rect()
        elif self.cycle == 1:
            self.draw_circle()
        elif self.cycle == 2:
            self.draw_line()

    def draw_tesseract(self):
        index = 0
        projected_points = [j for j in range(len(self.tesseract.points))]

        for point in self.tesseract.points:
            rotated_3d = self.tesseract.rotation4d_xy(point)
            rotated_3d = self.tesseract.rotation4d_zw(rotated_3d)

            distance = 5
            w = 1/(distance - rotated_3d[3][0])
            projection_matrix4 = [
                [w, 0, 0, 0],
                [0, w, 0, 0],
                [0, 0, w, 0], ]

            projected_3d = self.tesseract.matrix_multiplication(projection_matrix4, rotated_3d)
            rotated_2d = self.tesseract.tesseract_rotation(projected_3d)

            z = 1/(distance - (rotated_2d[2][0] + rotated_3d[3][0]))
            projection_matrix = [[z, 0, 0],
                                 [0, z, 0]
                                 ]

            rotated_2d = self.tesseract.rotation_x(projected_3d)
            projected_2d = self.tesseract.matrix_multiplication(projection_matrix, rotated_2d)
            x = int(projected_2d[0][0] * self.tesseract.scale) + self.CENTER_X
            y = int(projected_2d[1][0] * self.tesseract.scale) + self.CENTER_Y

            projected_points[index] = [x, y]
            arcade.draw_circle_filled(x, y, color=arcade.csscolor.DARK_VIOLET, radius=4)
            index += 1

        # draw edges
        for m in range(4):
            self.connect_points(m, (m+1) % 4, projected_points, 8)
            self.connect_points(m+4, (m+1) % 4 + 4, projected_points, 8)
            self.connect_points(m, m+4, projected_points, 8)

        for m in range(4):
            self.connect_points(m, (m+1) % 4, projected_points, 0)
            self.connect_points(m+4, (m+1) % 4 + 4, projected_points, 0)
            self.connect_points(m, m+4, projected_points, 0)

        for m in range(8):
            self.connect_points(m,  m+8, projected_points, 0)

    def connect_points(self, i, j, k, offset):
        a = k[i + offset]
        b = k[j + offset]
        arcade.draw_line(start_x=a[0], start_y=a[1], end_x=b[0], end_y=b[1], line_width=3, color=arcade.csscolor.DARK_VIOLET)

    # sound stuff
    def play_song(self):
        self.player = self.song.play(loop=True)


def main():
    music_visualizer = Visualizer(default=TESSERACT)

    music_visualizer.setup(song=INDUSTRY_BABY)
    music_visualizer.play_song()
    arcade.run()


class Tesseract():
    def __init__(self):
        self.color = arcade.csscolor.LIME

        self.angle = 0
        self.default_scale = 2500
        self.scale = self.default_scale
        self.speed = 0.04
        self.points = [n for n in range(16)]

        self.points[0] = [[-1], [-1], [1], [1]]
        self.points[1] = [[1], [-1], [1], [1]]
        self.points[2] = [[1], [1], [1], [1]]
        self.points[3] = [[-1], [1], [1], [1]]
        self.points[4] = [[-1], [-1], [-1], [1]]
        self.points[5] = [[1], [-1], [-1], [1]]
        self.points[6] = [[1], [1], [-1], [1]]
        self.points[7] = [[-1], [1], [-1], [1]]
        self.points[8] = [[-1], [-1], [1], [-1]]
        self.points[9] = [[1], [-1], [1], [-1]]
        self.points[10] = [[1], [1], [1], [-1]]
        self.points[11] = [[-1], [1], [1], [-1]]
        self.points[12] = [[-1], [-1], [-1], [-1]]
        self.points[13] = [[1], [-1], [-1], [-1]]
        self.points[14] = [[1], [1], [-1], [-1]]
        self.points[15] = [[-1], [1], [-1], [-1]]

    def tesseract_rotation(self, point):
        tesseract_rotation = [[1, 0, 0],
                              [0, math.cos(-math.pi/2), -math.sin(-math.pi/2)],
                              [0, math.sin(-math.pi/2), math.cos(-math.pi/2)]]
        return self.matrix_multiplication(tesseract_rotation, point)

    # 3d matrix rotation
    def rotation_x(self, point):
        rotation_x = [[1, 0, 0],
                      [0, math.cos(self.angle), -math.sin(self.angle)],
                      [0, math.sin(self.angle), math.cos(self.angle)]]
        return self.matrix_multiplication(rotation_x, point)

    def rotation_y(self, point):
        rotation_y = [[math.cos(self.angle), 0, -math.sin(self.angle)],
                      [0, 1, 0],
                      [math.sin(self.angle), 0, math.cos(self.angle)]]
        return self.matrix_multiplication(rotation_y, point)

    def rotation_z(self, point):
        rotation_z = [[math.cos(self.angle), -math.sin(self.angle), 0],
                      [math.sin(self.angle), math.cos(self.angle), 0],
                      [0, 0, 1]]
        return self.matrix_multiplication(rotation_z, point)

    # 4d matrix rotation
    def rotation4d_xy(self, point):
        rotation4d_xy = [[math.cos(self.angle), -math.sin(self.angle), 0, 0],
                         [math.sin(self.angle), math.cos(self.angle), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]
        return self.matrix_multiplication(rotation4d_xy, point)

    def rotation4d_xz(self, point):
        rotation4d_xz = [[math.cos(self.angle), 0, -math.sin(self.angle), 0],
                         [0, 1, 0, 0],
                         [math.sin(self.angle), 0, math.cos(self.angle), 0],
                         [0, 0, 0, 1]]
        return self.matrix_multiplication(rotation4d_xz, point)

    def rotation4d_xw(self, point):
        rotation4d_xw = [[math.cos(self.angle), 0, 0, -math.sin(self.angle)],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [math.sin(self.angle), 0, 0, math.cos(self.angle)]]
        return self.matrix_multiplication(rotation4d_xw, point)

    def rotation4d_yz(self, point):
        rotation4d_yz = [[1, 0, 0, 0],
                         [0, math.cos(self.angle), -math.sin(self.angle), 0],
                         [0, math.sin(self.angle), math.cos(self.angle), 0],
                         [0, 0, 0, 1]]
        return self.matrix_multiplication(rotation4d_yz, point)

    def rotation4d_yw(self, point):
        rotation4d_yw = [[1, 0, 0, 0],
                         [0, math.cos(self.angle), 0, -math.sin(self.angle)],
                         [0, 0, 1, 0],
                         [0, math.sin(self.angle), 0, math.cos(self.angle)]]
        return self.matrix_multiplication(rotation4d_yw, point)

    def rotation4d_zw(self, point):
        rotation4d_zw = [[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, math.cos(self.angle), -math.sin(self.angle)],
                         [0, 0, math.sin(self.angle), math.cos(self.angle)]]
        return self.matrix_multiplication(rotation4d_zw, point)

    def matrix_multiplication(self, a, b):
        columns_a = len(a[0])
        rows_a = len(a)
        columns_b = len(b[0])
        rows_b = len(b)

        result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
        if columns_a == rows_b:
            for x in range(rows_a):
                for y in range(columns_b):
                    sum = 0
                    for k in range(columns_a):
                        sum += a[x][k] * b[k][y]
                    result_matrix[x][y] = sum

            return result_matrix

        else:
            print("columns of the first matrix must be equal to the rows of the second matrix")
            return None


if __name__ == "__main__":
    main()
