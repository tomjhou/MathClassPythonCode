import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import sounddevice as sd


wave = np.load('wav2.npy')

sampleRate = 44100

# Nyquist limit is half the sample rate, i.e. 22.05kHz instead of 44.1kHz.
nyquistRate = sampleRate / 2

# Get # of samples in waveform
len_w = len(wave)

print(f'Loaded waveform with {len_w} samples = {len_w / sampleRate} seconds.')
print(f'Now playing through computer speaker. You should hear a piercing tone.')

sd.play(wave)


# Calculate FFT of raw waveform.
f = np.abs(np.fft.fft(wave))  # Absolute value allows us to ignore phase

# plot FFT vs frequency
freq_list = np.arange(len_w) / len_w * sampleRate   # list of frequencies
plt.plot(freq_list, f)
plt.title('FFT of input waveform')

# Sample FFT plot as before, but with log axis, and with second
# half deleted, as it is mirror image of first half.
plt.figure()
halfLen = len_w // 2    # We use // instead of /, to force result to be integer
plt.plot(freq_list[0:halfLen], f[0:halfLen])  # Show only first half
plt.xscale('log')
plt.title('FFT of input, log scale')

# Solution: crappy low-pass filter with cutoff at 1500 Hz
order = 51  # Highly recommend using an odd number for filter order.
print(f'Starting to calculate convolution...')
w = signal.firwin(order, 1500/nyquistRate)
wave_Filtered = np.convolve(wave, w)
print(f'Done calculating convolution.')


# plot FFT of final output, log scales
plt.figure()
fft_filtered = abs(np.fft.fft(wave_Filtered))
len_filtered = len(fft_filtered)   # convolution increased length. Have to recalculate frequency list.
freq_list_filtered = np.arange(len_filtered) / len_filtered * sampleRate   # list of frequencies
halfLen = len_filtered // 2
plt.plot(freq_list_filtered[:halfLen], fft_filtered[:halfLen])
plt.xscale('log')
plt.yscale('log')
plt.title('FFT after filter')

print('Now playing filtered signal through computer speaker. It will still sound like a piercing tone.')
print('Your homework is to improve this crappy filter to reveal the underlying musical piece.')

plt.show()