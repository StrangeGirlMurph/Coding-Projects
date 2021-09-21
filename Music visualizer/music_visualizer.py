# multiline comments Crtl + K + C (undo + U)

import arcade
import librosa
import librosa.display
import numpy as np
from scipy.signal import savgol_filter, resample

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "music visualizer"
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HEIGHT/2

# options
RECTANGLE = "rect"
CIRCLE = "circle"
CIRCLE_OUTLINE = "circle_outline"
LINE = "line"
POINT_GRAPH = "point_graph"
LINE_GRAPH = "line_graph"

SONG = "source/INDUSTRY_BABY_feat_Jack_Harlow.wav"  # put your song here
AUDIO_TIME_SERIES, SAMPLING_RATE = librosa.load(SONG)

FPS = 75  # (refresh rate of the visualizer)


class Visualizer(arcade.Window):
    def __init__(self, default):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, update_rate=1/FPS)
        arcade.set_background_color(arcade.csscolor.WHITE)
        self.color = arcade.csscolor.LIME

        # sound stuff
        self.song = arcade.Sound(SONG)
        self.player = None

        # logic stuff
        self.frameNumber = 0
        self.part = 0  # part of the audio time series that the song is currently at
        self.pause = False
        self.option = default

        self.value = 0  # the value at this part
        self.points = []  # points for the line strip graph or the point graph

    def setup(self):
        self.smooth = savgol_filter(abs(AUDIO_TIME_SERIES), window_length=2001, polyorder=3)

    def on_key_press(self, key, modifiers):
        # pause and resume
        if key == arcade.key.SPACE:
            if not self.pause:
                self.player.pause()
            else:
                self.player.play()
            self.pause = not self.pause

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
            self.option = POINT_GRAPH
        elif key == arcade.key.G:
            self.option = LINE_GRAPH

    #
    def on_update(self, delta_time):
        if not self.pause:
            self.part = int(self.song.get_stream_position(self.player) * SAMPLING_RATE)

            if self.option in (POINT_GRAPH, LINE_GRAPH):
                self.update_points(self.smooth * 2)
            elif self.option in (RECTANGLE, CIRCLE, CIRCLE_OUTLINE, LINE):
                self.update_single_value(self.smooth * 2)

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

        arcade.finish_render()  # ---

    # update functions
    def update_points(self, audio_signal):
        self.points.append([SCREEN_WIDTH, CENTER_Y - CENTER_Y/2 + audio_signal[self.part] * CENTER_Y])

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
        arcade.draw_rectangle_filled(CENTER_X, CENTER_Y, 800 * self.value, 200, color=self.color)

    def draw_line(self):
        arcade.draw_line(CENTER_X, CENTER_Y, CENTER_X + 400 * self.value, CENTER_Y, line_width=8, color=self.color)
        arcade.draw_line(CENTER_X, CENTER_Y, CENTER_X - 400 * self.value, CENTER_Y, line_width=8, color=self.color)

    def draw_circle_outline(self):
        arcade.draw_circle_outline(CENTER_X, CENTER_Y, 250 * self.value, color=self.color, border_width=5)

    def draw_circle(self):
        arcade.draw_circle_filled(CENTER_X, CENTER_Y, 250 * self.value, color=self.color)

    # sound
    def play_song(self):
        self.player = self.song.play(loop=True)


def main():
    music_visualizer = Visualizer(default=RECTANGLE)

    music_visualizer.setup()
    music_visualizer.play_song()
    arcade.run()


if __name__ == "__main__":
    main()
