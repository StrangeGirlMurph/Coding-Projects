import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np


def main():
    y, sr = librosa.load(
        "media/INDUSTRY_BABY_feat_Jack_Harlow.wav")
    print(y)
    print(sr)
    print(len(y))

    abs = np.abs(y)
    smooth = savgol_filter(abs, window_length=99, polyorder=8)

    librosa.display.waveshow(abs, sr=sr)
    librosa.display.waveshow(smooth, sr=sr)
    plt.show()


if __name__ == '__main__':
    main()
