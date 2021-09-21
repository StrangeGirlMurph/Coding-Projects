# multiline comments Crtl + K + C (undo + U)

import arcade
import librosa
import librosa.display
import numpy as np

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "music visualizer"
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HEIGHT/2

SONG = "source/INDUSTRY_BABY_feat_Jack_Harlow.wav"  # put your song here
AUDIO_TIME_SERIES, SAMPLING_RATE = librosa.load(SONG)

# sampling rate for new data for industry baby is 40 fps
FPS = 30


class Visualizer(arcade.Window):
    def __init__(self):
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

        self.value = 0  # the value at this part
        self.points = []  # points for the line strip graph or the point graph

    def setup(self):
        pass

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

    def on_update(self, delta_time):
        if not self.pause:
            self.part = int(self.song.get_stream_position(self.player) * SAMPLING_RATE)

            # self.update_points()
            self.update_single_value()  # for the circle, line and rect

    def on_draw(self):
        arcade.start_render()  # ---

        # self.draw_graph_line_strip()
        # self.draw_graph_points()
        # self.draw_circle()
        # self.draw_line()
        self.draw_rect()

        arcade.finish_render()  # ---

    def update_points(self):
        self.points.append([SCREEN_WIDTH, CENTER_Y + AUDIO_TIME_SERIES[self.part] * (CENTER_Y - 100)])

        self.points = np.array(self.points)
        self.points[:, 0] = self.points[:, 0] - 3  # shift all the points to the left

        # delete all the points that are outside of the window
        self.points = np.delete(self.points, np.where(self.points[:, 0] <= 0), axis=0)
        self.points = self.points.tolist()

    def update_single_value(self):
        self.value = abs(AUDIO_TIME_SERIES[self.part])

    def draw_graph_line_strip(self):
        arcade.draw_line_strip(self.points, color=self.color, line_width=2)

    def draw_graph_points(self):
        arcade.draw_points(self.points, color=self.color, size=3)

    def draw_rect(self):
        arcade.draw_rectangle_filled(CENTER_X, CENTER_Y, 800 * self.value, 200, color=self.color)

    def draw_line(self):
        arcade.draw_line(CENTER_X, CENTER_Y, CENTER_X + 400 * self.value, CENTER_Y, line_width=8, color=self.color)
        arcade.draw_line(CENTER_X, CENTER_Y, CENTER_X - 400 * self.value, CENTER_Y, line_width=8, color=self.color)

    def draw_circle(self):
        arcade.draw_circle_outline(CENTER_X, CENTER_Y, 250 * self.value, color=self.color, border_width=5)

    def play_song(self):
        self.player = self.song.play(loop=True)


def main():
    music_visualizer = Visualizer()
    music_visualizer.setup()

    music_visualizer.play_song()
    arcade.run()


if __name__ == "__main__":
    main()
