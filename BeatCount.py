from os.path import dirname, join as pjoin
from scipy.io import wavfile
from scipy import signal
from scipy.signal import find_peaks, peak_prominences
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
#code referenced http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/ 

#This display orange xs where the peaks are 
def display_peaks(peaks,beat):
    plt.plot(beat, label="Left channel")

    #orange xs
    plt.plot(peaks, beat[peaks], "x")
    #right channel? just incase idk
    #plt.plot(data[:, 1], label="Right channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

#takes in desired data, distance, prominence
def peak_count(data,distance,prominence):
    #left channel
    beat = data[:, 0] # for clean .wav, add make it data[:, 0]

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
        ms_dist = ((birdbeats_interval / samplerate) * 1000.0) #Convert sample distances to ms distances
        birdbeats_list.append(ms_dist) #Append to list
        cnt += 1

    bpm = 60000 / np.mean(birdbeats_list) #60000 ms (1 minute) / average interval of signal
    print ("Average Heart Beat is: %.01f" %bpm)  #Round off to 1 decimal and print

    
def main():
    #read from directory
    file_name = 'heartbeat-01a.wav'
    # file_name = 'Sample-Filtered_out_000.wav'
    data_dir = pjoin(dirname(__file__), file_name)
    #read wav
    sample_rate, data = wavfile.read(data_dir)

    # necessary variables for segmenting
    total_length = len(data) / float(sample_rate)
    segment_length = 60
    start = 0
    end = sample_rate * segment_length
    for i in range(0, math.ceil(total_length/segment_length)):
        segment = data[start:end]
        
        # try and calculate distance and prominence arguments 
        distance = 2000 # calculate_distance(segment)
        prominence = 8e+08 # calculate_prominence(segment)
        peaks, beat = peak_count(segment,distance,prominence)
        bpm(sample_rate,beat,peaks)
        # display_peaks(peaks,beat)

        start += sample_rate
        end += sample_rate
        if(end + sample_rate > len(data)): 
            end = sample_rate

    

if __name__ == "__main__":
    main()