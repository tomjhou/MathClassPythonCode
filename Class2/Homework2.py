#
# Import libraries
#

#
# numpy, scipy, and matploblib come pre-installed with Anaconda.
#
# But "sounddevice" does not. When running for the first time, install it as follows:
#
# Step 1:
# Windows: Open "Anaconda Prompt" from Windows start menu. (can also click the "CMD.exe" button in Anaconda Navigator)
# Mac: Open the "Terminal" app.
#
# Step 2: Type the following command, and hit <Enter>:
#
# conda install -c conda-forge python-sounddevice
#
# You should see a lot of text while it installs. It may prompt you whether to proceed or not (say yes).
# This will take about 1 minute total.
#

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import sounddevice as sd

import time

#
# Load waveform from file
#

wave = np.load('../Class2/wav2.npy')

print(f'Loaded waveform with {wave.size} samples.')

# Downsample by 4x, so code will run faster.
RESAMPLE_RATIO = 0.25

wave = signal.resample(wave, int(wave.size * RESAMPLE_RATIO))

sampleRate = 44100 * RESAMPLE_RATIO
print(f'Downsampled 4x to {wave.size} samples. Duration is {wave.size / sampleRate} seconds.')


#
# Play through computer speaker
#

# Normalize amplitude to 1 because audio player clip values > 1
wave = wave / max(wave)

print(f'Playing wave.')
VOLUME = 0.25
sd.play(wave * VOLUME, sampleRate, blocking=True)

#
# Calculate and plot FFT
f = np.fft.fft(wave)  # Absolute value allows us to ignore phase

# plot FFT vs frequency
freq_list = np.linspace(0, sampleRate, num=f.size, endpoint=False)   # list of frequencies
plt.plot(freq_list, np.abs(f))

plt.title('Input spectrum, log scale')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

#
# Implement low-pass filter

# Filter order. Should be an odd number
order = 100001

# Nyquist limit is half the sample rate
nyquist = sampleRate / 2

# Generate filter "kernel"
kernel = signal.firwin(order, [1500/nyquist])

# Convolve kernel with original wave
print(f'Calculating convolution. Might take a few seconds if filter order is large ...')
t0 = time.time()
wave2 = np.convolve(wave, kernel)

print(f'Done in {time.time() - t0:.3f} seconds!')

#
# Calculate FFT of filtered waveform.
#

f2 = np.fft.fft(wave2)

# Generate list of frequency values
freq_list2 = np.linspace(0, sampleRate, num=f2.size, endpoint=False)

# plot FFT vs frequency
plt.plot(freq_list2, np.abs(f2))


#
# Play filtered result through computer speaker
#

print(f'Playing filtered wave through computer speaker.')

# Normalize amplitude to 1, again to satisfy audio player.
sd.play(wave2 / max(wave2), sampleRate, blocking=True)
