import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, resample, resample_poly
import numpy as np


def main():
    y, sr = librosa.load(
        "source/INDUSTRY_BABY_feat_Jack_Harlow.wav")

    print(f'Number of samples default: {len(y)}')
    print(f'samples per second default: {sr}')

    SAMPLE_RATE = 100

    # plotting
    fig, ax = plt.subplots()
    ax.set(xlim=[0, 10])

    # compare downsampling functions
    downrate = resample(y, int((len(y)/sr)*SAMPLE_RATE))
    downsample = resample_poly(y, 2, int(sr/SAMPLE_RATE)*2)

    librosa.display.waveshow(np.abs(y), sr=sr, label="default")
    librosa.display.waveshow(downrate, sr=SAMPLE_RATE, label="downrate")
    librosa.display.waveshow(downsample, sr=SAMPLE_RATE, label="downsample")

    # compare smoothing
    downrate = resample(y, int((len(y)/sr)*SAMPLE_RATE))
    smooth = savgol_filter(np.abs(downrate), window_length=int(SAMPLE_RATE/10)+1, polyorder=3)
    smoothy = savgol_filter(np.abs(y), window_length=2001, polyorder=3)

    librosa.display.waveshow(np.abs(y), sr=sr, label="default")
    librosa.display.waveshow(smoothy, sr=sr, label="default smooth")
    librosa.display.waveshow(smooth, sr=SAMPLE_RATE, label="downrate smooth")

    # plotting
    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
