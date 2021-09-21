import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, resample
import numpy as np


def main():
    y, sr = librosa.load(
        "source/INDUSTRY_BABY_feat_Jack_Harlow.wav")
    print(y)
    print(sr)
    print(len(y))

    downrate = resample(y, int((len(y)/sr)*100))

    abs = np.abs(y)

    #smooth = savgol_filter(abs, window_length=2001, polyorder=3)

    librosa.display.waveshow(abs, sr=sr)
    # librosa.display.waveshow(smooth[0:100000], sr=sr)  # smoother.smooth_data[0]
    librosa.display.waveshow(downrate, sr=100)
    plt.show()


if __name__ == '__main__':
    main()
