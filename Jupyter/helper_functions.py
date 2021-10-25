import numpy as np
import sounddevice as sd

# Calculate

pure_signal = np.load('../Class2/wav1.npy')
pure_noise = np.load('../Class2/sine.npy')
pure_signal /= np.linalg.norm(pure_signal)
pure_noise /= np.linalg.norm(pure_noise)


def score(w):
    w = np.real(w)
    w /= np.linalg.norm(w)

    s = np.correlate(w, pure_signal, mode='full')

    print("version1")
    return np.max(s)


def play_sound(w, VOLUME, Fs):
    w = np.real(w)
    w = w / np.max(w)
    sd.play(w * VOLUME, Fs)
