import sys

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from scipy.io import wavfile


PEAK_HEARTRATE = 2000  # Expected highest heartrate in bpm
HEARTBEAT_BANDWIDTH = (PEAK_HEARTRATE / 60) * 2


def normalize_signal(data):
    return data / data[np.argmax(data)]


def demodulate_signal(data, sample_rate, carrier_rate):
    # Calculate the I and Q modulated signals
    timestamps = np.linspace(0, len(data) / sample_rate, len(data), endpoint=False)
    carrier_i = np.cos(2.0 * np.pi * carrier_rate * timestamps)
    carrier_q = np.sin(2.0 * np.pi * carrier_rate * timestamps)
    signal_i = carrier_i * data
    signal_q = carrier_q * data

    # TODO: Lowpass I and Q
    filt_order = 3
    filter_width = carrier_rate
    filter_width_nyq = filter_width / (sample_rate / 2.0)
    butter_sos = sig.butter(filt_order, filter_width_nyq, output='sos')
    signal_i = sig.sosfilt(butter_sos, signal_i)
    signal_q = sig.sosfilt(butter_sos, signal_q)

    # Combine I and Q filtered signals
    signal = np.sqrt(signal_i ** 2 + signal_q ** 2)

    return signal


def extract_am_signal(data, sample_rate):
    filt_order = 3
    filter_width = HEARTBEAT_BANDWIDTH
    freq, pwelch_spec = sig.welch(data, sample_rate, scaling='spectrum')

    # Extract peak frequency
    peak_freq = freq[np.argmax(pwelch_spec)]
    peak_nyq = peak_freq / (sample_rate / 2.0)
    width_nyq = filter_width / (sample_rate / 2.0)

    # Bandpass just that frequency
    butter_sos = sig.butter(filt_order, [peak_nyq - width_nyq, peak_nyq + width_nyq], btype='band', output='sos')

    # Plot freq spectrum
    #plt.semilogy(freq, pwelch_spec)
    #plt.xlabel('Frequency [Hz]')
    #plt.ylabel('PSD')
    #plt.grid()
    #plt.show()

    return sig.sosfilt(butter_sos, data), peak_freq


def data_filter(data, sample_rate):
    signal = data[:,0].astype(np.float32) # Take the left channel, discard the unused right
    # TODO: Replace above with sophisticated test? Sum both channels?

    signal = normalize_signal(signal)
    signal, carrier_rate = extract_am_signal(signal, sample_rate)
    signal = normalize_signal(signal)
    signal = demodulate_signal(signal, sample_rate, carrier_rate)
    signal = normalize_signal(signal)

    return signal, sample_rate


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
