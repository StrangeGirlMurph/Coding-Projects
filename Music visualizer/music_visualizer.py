# multiline comments Crtl + K + C (undo + U)

import arcade
import librosa
import librosa.display
import numpy as np
from scipy.signal import savgol_filter, resample


# options
RECTANGLE = "rect"
CIRCLE = "circle"
CIRCLE_OUTLINE = "circle_outline"
LINE = "line"
POINT_GRAPH = "point_graph"
LINE_GRAPH = "line_graph"
KLEIN_BOTTLE = "klein_bottle"
CHANGING_SHAPES = "changing_shapes"

# Constants
DEFAULT_WIDTH = 1100
DEFAULT_HEIGHT = 700
SCREEN_TITLE = "music visualizer"

# pictures
KLEIN_BOTTLE_SPRITE = arcade.Sprite("media/Klein_bottle.png", scale=1, center_x=DEFAULT_WIDTH/2, center_y=DEFAULT_HEIGHT/2)

# sound
SONG = "source/INDUSTRY_BABY_feat_Jack_Harlow.wav"  # put your song here
AUDIO_TIME_SERIES, SAMPLING_RATE = librosa.load(SONG)
TEMPO, BEAT_FRAMES = librosa.beat.beat_track(y=AUDIO_TIME_SERIES, sr=SAMPLING_RATE)
# BEATS = librosa.frames_to_time(BEAT_FRAMES, sr=SAMPLING_RATE)

FPS = 75  # (refresh rate of the visualizer)

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
        self.CENTER_X = DEFAULT_WIDTH/2
        self.CENTER_Y = DEFAULT_HEIGHT/2

        # sound stuff
        self.song = arcade.Sound(SONG)
        self.player = None

        # logic stuff
        self.frameNumber = 0
        self.cycle = 0  # for changing shapes
        self.part = 0  # part of the audio time series that the song is currently at
        self.pause = False
        self.option = default

        self.value = 0  # the value at this part
        self.points = []  # points for the line strip graph or the point graph

    def setup(self):
        self.smooth = savgol_filter(abs(AUDIO_TIME_SERIES), window_length=2001, polyorder=3) * 2

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.CENTER_X = self.SCREEN_WIDTH/2
        self.CENTER_Y = self.SCREEN_HEIGHT/2
        print(f"Window resized to: {width}, {height}")

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
        else:
            return
        print(f'Choosen visualizer: {self.option}')

    def on_update(self, delta_time):
        if not self.pause:
            self.part = int(self.song.get_stream_position(self.player) * SAMPLING_RATE)

            if self.option in (POINT_GRAPH, LINE_GRAPH):
                self.update_points(self.smooth)
            elif self.option in (RECTANGLE, CIRCLE, CIRCLE_OUTLINE, LINE, KLEIN_BOTTLE, CHANGING_SHAPES):
                self.update_single_value(self.smooth)

            self.frameNumber += 1

    def on_draw(self):
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

        arcade.finish_render()  # ---

    # update functions
    def update_points(self, audio_signal):
        self.points.append([self.SCREEN_WIDTH, self.CENTER_Y - self.CENTER_Y/2 + audio_signal[self.part] * self.CENTER_Y])

        self.points = np.array(self.points)
        self.points[:, 0] = self.points[:, 0] - 2  # shift all the points to the left

        # delete all the points that are outside of the window
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

    # sound stuff
    def play_song(self):
        self.player = self.song.play(loop=True)


def main():
    music_visualizer = Visualizer(default=RECTANGLE)

    music_visualizer.setup()
    music_visualizer.play_song()
    arcade.run()


if __name__ == "__main__":
    main()
