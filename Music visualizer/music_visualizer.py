import arcade
import librosa
import librosa.display
import math
import numpy as np

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Music visualizer"
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HEIGHT/2
INDUSTRY_BABY = arcade.Sound("media/INDUSTRY_BABY_feat_Jack_Harlow.wav")
AUDIO_TIME_SERIES, SAMPLING_RATE = librosa.load(
    "media/INDUSTRY_BABY_feat_Jack_Harlow.wav")
FPS = 10


class visualizer(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,
                         SCREEN_TITLE, update_rate=1/FPS)

        arcade.set_background_color(arcade.csscolor.WHITE)
        self.numFrames = 0
        self.player = None
        self.color = arcade.csscolor.LIME

    def setup(self):
        # AUDIO_TIME_SERIES_ABS = np.abs(AUDIO_TIME_SERIES)
        self.points = []
        pass

    def on_draw(self):
        part = int(INDUSTRY_BABY.get_stream_position(
            self.player) * SAMPLING_RATE)

        arcade.start_render()  # ---

        self.graph(abs(AUDIO_TIME_SERIES[part]))

        arcade.finish_render()  # ---

    def graph_points(self, value):
        self.points.append([SCREEN_WIDTH, CENTER_Y + value * (CENTER_Y - 100)])
        arcade.draw_points(self.points, color=self.color, size=4)

        self.points = np.array(self.points)
        self.points[:, 0] = self.points[:, 0] - 4

        self.points = np.delete(self.points, np.where(
            self.points[:, 0] <= 0), axis=0)

        self.points = self.points.tolist()

    def rect(self, value):
        arcade.draw_rectangle_filled(
            CENTER_X, CENTER_Y, 800 * value, 100, color=self.color)

    def line(self, value):
        arcade.draw_line(CENTER_X, CENTER_Y, CENTER_X + 400 * value,
                         CENTER_Y, line_width=8, color=self.color)
        arcade.draw_line(CENTER_X, CENTER_Y, CENTER_X - 400 * value,
                         CENTER_Y, line_width=8, color=self.color)

    def circle(self, value):
        arcade.draw_circle_outline(
            CENTER_X, CENTER_Y, 250 * value, color=self.color, border_width=5)


def main():
    window = visualizer()
    window.setup()

    window.player = INDUSTRY_BABY.play()
    arcade.run()


if __name__ == "__main__":
    main()
