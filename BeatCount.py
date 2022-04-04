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

def calculate_distance(sample_rate, min_xbill_period):
    return sample_rate * min_xbill_period

def calculate_prominence(max_sound,avg_sound):
    return max_sound-avg_sound
    
def main():
    #read from directory
    file_name = 'tried_filter.wav'
    # file_name = 'Sample-Filtered_out_000.wav'
    data_dir = pjoin(dirname(__file__), file_name)
    #read wav
    #sample_rate = samples a second the wav is written in
    sample_rate, data = wavfile.read(data_dir)

    # necessary variables for segmenting
    total_length = len(data) / float(sample_rate)
    segment_length = 5
    start = 0
    end = sample_rate * segment_length
    for i in range(0, math.ceil(total_length/segment_length)):
        segment = data[start:end]
        
        #smallest seconds between crossbill beats (kinda acts like a lowpass filter)
        #"magic number" for slider (but we can do sliders for dist/prom if yall want)
        min_xbill_period = .11 

        max_sound = max(segment[:, 0])
        avg_sound = np.median(segment[:, 0])

        # try and calculate distance and prominence arguments 
        distance = calculate_distance(sample_rate, min_xbill_period) #2000
        prominence = calculate_prominence(max_sound,avg_sound) #8e+08

        #print(distance)
        #print(prominence)

        peaks, beat = peak_count(segment,distance,prominence)
        bpm(sample_rate,beat,peaks)
        display_peaks(peaks,beat,sample_rate,segment_length)

        start += sample_rate
        end += sample_rate
        if(end + sample_rate > len(data)): 
            end = sample_rate

    

if __name__ == "__main__":
    main()
