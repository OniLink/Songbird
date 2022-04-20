from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.signal as sig
from scipy.signal import find_peaks, peak_prominences
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import sys

#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
#code referenced http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/ 

#This display orange xs where the peaks are 
def display_peaks(peaks,beat,sample_rate,segment_length):
    t = np.linspace(0., segment_length, beat.shape[0])
    plt.plot(t,beat)

    plt.plot((peaks/sample_rate), beat[peaks], "x")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

#takes in desired data, distance, prominence
def peak_count(data,distance,prominence):
    #left channel
    beat = data[:] # for clean .wav, add make it data[:, 0]

    #prominence is the steepness  
    peaks,_ = find_peaks(beat, distance=distance, prominence=prominence)
    np.diff(peaks)

    # prominences = peak_prominences(beat, peaks)[0]
    # print(prominences)

    return peaks, beat


#calculates average bpm
def bpm(samplerate,beat,peaks):
    birdbeats_list = []
    cnt = 0

    while (cnt < (len(peaks)-1)):
        birdbeats_interval = (peaks[cnt+1] - peaks[cnt]) #Calculate distance between beats in # of samples
        sec_dist = birdbeats_interval / samplerate #Convert sample distances to ms distances
        birdbeats_list.append(sec_dist) #Append to list
        cnt += 1

    bpm = 60 / np.mean(birdbeats_list) # 1 minute / average interval of signal
    return bpm

def calculate_average_bpm(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t           

    avg = sum_num / len(num)
    return avg

#this function just converts seconds to samples, but we can tack on more later to make it better if we want
def calculate_distance(sample_rate, min_xbill_period):
    return sample_rate * min_xbill_period # seconds to samples

#this function looks for the difference between the highest peaks and avg "noise"
def calculate_prominence(max_sound,avg_sound):
    return max_sound-avg_sound
    
def main():

    # Violets filter data code
    if len(sys.argv) < 3:
        print("USAGE: %s <input> <output>".format(sys.argv[0]))
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print("Grabbed arguments")

    sample_rate, data = wavfile.read(input_filename)
    filtered_data, filtered_rate = data_filter(data, sample_rate)
    wavfile.write(output_filename, filtered_rate, filtered_data)

    print("Filtered input file")

    # Megan: adding to merge our code
    sample_rate = filtered_rate
    data = filtered_data

    # Megan: commented out because above code replaced it
    # output_filename = 'Sample-Filtered_out_000.wav'
    # data_dir = pjoin(dirname(__file__), output_filename)
    # sample_rate, data = wavfile.read(data_dir)

    print("About to segment and output BPM")

    # necessary variables for segmenting
    bpm_arr = []
    total_length = len(data) / float(sample_rate)
    segment_length = 15
    start = 0
    end = sample_rate * segment_length
    print(total_length/segment_length)
    print(f"Sample rate: {sample_rate}")
    print(f"Length data: {len(data)}")
    for i in range(0, math.ceil(total_length/segment_length)):
        segment = data[start:end]
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
        prominence = calculate_prominence(max_sound,avg_sound) 
        print(prominence)

        peaks, beat = peak_count(segment,distance,prominence)
        seg_bpm = bpm(sample_rate,beat,peaks)
        print(f"bpm: {seg_bpm}")
        bpm_arr.append(seg_bpm)

        start += sample_rate
        end += sample_rate
        if(end + sample_rate > len(data)): 
            end = sample_rate

    avg_bpm = calculate_average_bpm(bpm_arr)
    print ("Average Heart Beat is: %.01f" %avg_bpm)
    display_peaks(peaks,beat,sample_rate,segment_length)

    

if __name__ == "__main__":
    main()
