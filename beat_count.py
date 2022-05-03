from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.signal as sig
from scipy.signal import find_peaks, peak_prominences
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import sys
import heart_filter

#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
#code referenced http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/ 

# Display detected peaks using matplotlib
# Params:
#   peaks: The indices of the detected peaks
#   beat: The heart beat signal
#   sample_rate: The sample rate of the signal
#   segment_length: The length of the signal segment to plot
def display_peaks(peaks, beat, sample_rate, segment_length):
    t = np.linspace(0., segment_length, beat.shape[0])
    plt.plot(t,beat)

    plt.plot((peaks/sample_rate), beat[peaks], "x")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


# Detects the peaks in the heart signal
# Params:
#   data: The heart signal
#   distance: The minimum distance between peaks
#   prominence: The prominence of a peak above its surroundings
# Returns:
#   The indices of the detected peaks
def peak_count(data, distance, prominence):
    #prominence is the steepness  
    peaks,_ = find_peaks(data, distance=distance, prominence=prominence)
    np.diff(peaks)

    # prominences = peak_prominences(beat, peaks)[0]
    # print(prominences)

    return peaks


# Calculate the average bpm of a segment of the heart signal from its detected peaks
# Params:
#   sample_rate: The sample rate of the heart signal
#   segment: The segment of the heart signal
#   peaks: The indices of the detected peaks
# Returns:
#   The average bpm of the heart in the segment.
def bpm(sample_rate, segment, peaks):
    beats = len(peaks)
    duration = len(segment) / sample_rate
    return 60.0 * beats / duration


# Calculate the average bpm from several segments of the heart signal
# Params:
#   bpm_array: The array of segment bpms
# Returns:
#   The average heartrate
def calculate_average_bpm(bpm_array):
    return np.mean(bpm_array)


#this function just converts seconds to samples, but we can tack on more later to make it better if we want
# Convert seconds to sample count
# Params:
#   sample_rate: The sample rate of the signal
#   period: The time in seconds
# Returns:
#   The distance in samples of a period of time
def calculate_distance(sample_rate, period):
    return sample_rate * period


#this function looks for the difference between the highest peaks and avg "noise"
# Calculates the prominence
# Params:
#   max_sound: The maximum amplitude of the signal segment
#   avg_sound: The average amplitude of the signal segment
# Returns:
#   An estimate for the peak prominence
def calculate_prominence(max_sound, avg_sound):
    return max_sound-avg_sound


def main():
    if len(sys.argv) < 3:
        print("USAGE: %s <input> <output>".format(sys.argv[0]))
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print("Grabbed arguments")

    sample_rate, data = wavfile.read(input_filename)
    filtered_data, filtered_rate = heart_filter.data_filter(data, sample_rate)
    wavfile.write(output_filename, filtered_rate, filtered_data)

    print("Filtered input file")

    # Relabel
    sample_rate = filtered_rate
    data = filtered_data

    # necessary variables for segmenting
    bpm_arr = []
    total_length = len(data) / float(sample_rate)
    segment_length = 15
    print(total_length/segment_length)
    print(f"Sample rate: {sample_rate}")
    print(f"Length data: {len(data)}")
    for i in range(0, math.floor(total_length/segment_length)):
        segment = data[i * sample_rate * segment_length : (i+1) * sample_rate * segment_length]
        print(segment)
        
        #smallest seconds between crossbill beats (kinda acts like a lowpass filter)
        #"magic number" for slider
        min_xbill_period = .11

        max_sound = max(segment[:]) #looks at loudest peak in set of peaks
        print(max_sound)
        avg_sound = np.median(segment[:]) #looks at median of noise
        print(avg_sound)

        # variable for the sliders if yall want
        distance = calculate_distance(sample_rate, min_xbill_period) 
        print(distance)
        prominence = calculate_prominence(max_sound, avg_sound) 
        print(prominence)

        peaks = peak_count(segment, distance, prominence)
        seg_bpm = bpm(sample_rate, segment, peaks)
        print(f"bpm: {seg_bpm}")
        bpm_arr.append(seg_bpm)

    avg_bpm = calculate_average_bpm(bpm_arr)
    print ("Average Heart Beat is: %.01f" %avg_bpm)
    display_peaks(peaks, segment, sample_rate, segment_length)


if __name__ == "__main__":
    main()
