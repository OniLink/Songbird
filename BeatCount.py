from os.path import dirname, join as pjoin
from scipy.io import wavfile
from scipy import signal
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
#code referenced https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html

#read from directory
data_dir = pjoin(dirname(__file__), 'heartbeat-01a.wav')

#read wav
samplerate, data = wavfile.read(data_dir)

#  data stuff
#  print(f"number of channels = {data.shape[1]}")
#  length = data.shape[0] / samplerate
#  print(f"length = {length}s")

#left array 
beat = data[:, 0]
peaks,_ = find_peaks(beat, distance=2000, height=1000000000)
np.diff(peaks)

plt.plot(beat, label="Left channel")
plt.plot(peaks, beat[peaks], "x")
#right channel? just incase idk
#plt.plot(data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()


