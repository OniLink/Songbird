import sys

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from scipy.io import wavfile


def data_filter(data, sample_rate):
    data = data[:,0] # Take the left channel, discard the unused right
    # TODO: Replace above with sophisticated test? Sum both channels?
    freq, pwelch_spec = sig.welch(data, sample_rate, scaling='spectrum')

    # Select peak frequency and then bandpass filter the signal
    filt_order = 3
    filter_width = 0.001

    peak_freq = freq[np.argmax(pwelch_spec)]
    peak_nyq = peak_freq / (sample_rate / 2.0)
    butter_sos = sig.butter(filt_order, [(1 - filter_width) * peak_nyq, (1 + filter_width) * peak_nyq], btype='band', output='sos')
    filtered_signal = sig.sosfilt(butter_sos, data)

    # Plot freq spectrum
    plt.semilogy(freq, pwelch_spec)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD')
    plt.grid()
    plt.show()

    return filtered_signal, sample_rate


def main():
    if len(sys.argv) < 3:
        print("USAGE: %s <input> <output>".format(sys.argv[0]))
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    sample_rate, data = wavfile.read(input_filename)
    filtered_data, filtered_rate = data_filter(data, sample_rate)
    wavfile.write(output_filename, filtered_rate, filtered_data)


if __name__ == "__main__":
    main()
