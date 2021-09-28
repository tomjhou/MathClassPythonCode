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

# Calculate FFT of raw waveform.
f = abs(np.fft.fft(wave))  # Take absolute value to avoid worrying about imaginary components

# plot FFT vs frequency
# plt.figure()
freq_list = np.arange(len_w) / len_w * sampleRate   # list of frequencies
plt.plot(freq_list, f)
plt.title('FFT of input waveform')

# Find noise amplitude
noiseIndex = round(2000 / sampleRate * len_w)
print(f"Amplitude of 2kHz noise is {abs(f[noiseIndex])}\n")

#  Second method of finding noise amplitude
maxIndex = np.argmin(f)
maxValue = f[maxIndex]
print(f'Amplitude of peak is {maxValue}.\n')

# Sample FFT plot as before, but with logarithmic x-axis, and with second
# half truncated, as it is just a mirror image of first half.
plt.figure()
halfLen = int(np.floor(len_w / 2))  # Need floor function to make sure this is integer, or else next line will fail
plt.plot(freq_list[0:halfLen], np.abs(f[:halfLen]))  # Show only first half
plt.xscale('log')
plt.title('FFT of input, log scale')

# Solution: bandstop filter
order = 50001
margin = 400
w = signal.firwin(order, np.array([2000 - margin, 2000 + margin])/nyquistRate)

wave_Filtered = np.convolve(wave, w)

# plot impulse response. Truncate the endpoints
plt.figure()
range1 = round(order*.49)
range2 = round(order*.51)
plt.plot(np.arange(range1, range2), w[range1:range2])
plt.title('Impulse response, bandstop filter')

# plot frequency response
plt.figure()
fft_w = np.abs(np.fft.fft(w))
len_w = len(fft_w)   # convolution increased length. Have to recalculate frequency list.
freq_list = np.arange(len_w) / len_w * sampleRate   # list of frequencies
halfLen = int(np.floor(len_w / 2))   # Need floor function to make sure this is integer
plt.plot(freq_list[:halfLen], fft_w[:halfLen])  # Show only first half
plt.xscale('log')
plt.yscale('log')
plt.title('Frequency response, bandstop filter')

# plot FFT of final output
plt.figure()
fft_filtered = abs(np.fft.fft(wave_Filtered))
len_w = len(fft_filtered)   # convolution increased length. Have to recalculate frequency list.
halfLen = round(len_w/2)
freq_list = np.arange(len_w) / len_w * sampleRate    # ; % list of frequencies
plt.plot(freq_list[:halfLen], fft_filtered[:halfLen])
plt.xscale('log')
plt.yscale('log')

noiseIndex = round(2000 / sampleRate * len_w)
print(f'After filtering, amplitude of 2kHz noise is {fft_filtered[noiseIndex]}\n')

plt.title('FFT after FIR filtering');

sd.play(wave_Filtered, blocking=True)

