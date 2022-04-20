import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from matplotlib.ft2font import HORIZONTAL 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from sympy import true
import heart_filter
import beat_count
from scipy.io import wavfile


window = tk.Tk()
window.title("Heartbeat GUI")


fig, (ax1,ax2) = plt.subplots(1,2)

def toIndex(arr):
    return (3600*arr[0] + 60*arr[1] + arr[2])

def browsefunc():
    filename = filedialog.askopenfilename(filetypes=(("wav files","*.wav"),("All files","*.*")))
    search_textbox.delete(0, tk.END)
    search_textbox.insert(tk.END, filename)
    window.focus()

def write():
    global data
    global sample_rate
    global otherdata
    sample_rate_raw, data_raw = wavfile.read(search_textbox.get())
    data, sample_rate = heart_filter.data_filter(data_raw, sample_rate_raw)
    otherdata = data
    wavfile.write("deleteme.wav", sample_rate, data)
    for child in option_frame.winfo_children():
        child.configure(state='normal')
    dofilter()

def beatCount(min_xbill_period = .11, prominence_slider=1):
    bpm_arr = []
    total_length = len(otherdata) / float(sample_rate)
    segment_length = 15
    start = 0
    end = sample_rate * segment_length
    print(total_length/segment_length)
    print(f"Sample rate: {sample_rate}")
    print(f"Length data: {len(otherdata)}")
    for i in range(0, math.ceil(total_length/segment_length)):
        segment = otherdata[start:end]
        
        #smallest seconds between crossbill beats (kinda acts like a lowpass filter)
        #"magic number" for slider
        #min_xbill_period = .11

        max_sound = max(segment[:]) #looks at loudest peak in set of peaks
        avg_sound = np.median(segment[:]) #looks at median of noise

        # variable for the sliders if yall want
        distance = beat_count.calculate_distance(sample_rate, min_xbill_period) 
        prominence = beat_count.calculate_prominence(max_sound,avg_sound) 
        prominence *= prominence_slider

        peaks, beat = beat_count.peak_count(segment,distance,prominence)
        seg_bpm = beat_count.bpm(sample_rate,beat,peaks)
        print(f"bpm: {seg_bpm}")
        info_listbox.insert(tk.END, f"bpm: {seg_bpm}")
        bpm_arr.append(seg_bpm)

        start += sample_rate
        end += sample_rate
        if(end + sample_rate > len(otherdata)): 
            end = sample_rate

    avg_bpm = beat_count.calculate_average_bpm(bpm_arr)
    print ("Average Heart Beat is: %.01f" %avg_bpm)
    info_listbox.insert(tk.END, "Average Heart Beat is: %.01f" %avg_bpm)
    display_peaks(peaks,beat,sample_rate,segment_length,ax2)

def display_peaks(peaks,beat,sample_rate,segment_length, ax):
    t = np.linspace(0., segment_length, beat.shape[0])
    ax.cla()
    ax.plot(t,beat)

    ax.plot((peaks/sample_rate), beat[peaks], "x")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    #ax.show()

def dofilter():
    print("rerunning")
    minimum=option_time1.get()
    mins = list(map(int,minimum.split(':')))
    maximum=option_time2.get()
    maxs = list(map(int,maximum.split(':')))

    start = toIndex(mins) * sample_rate
    end = toIndex(maxs) * sample_rate

    #minimum = (int(minimum)) if (minimum != '') else 0
    #maximum = (int(maximum)) if (maximum != '') else 1024

    #input_data = read("deleteme.wav")[1]

    #plt.clf()
    info_listbox.delete(0,tk.END)
    beatCount(period_slider.get(),prominence_slider.get())
    #info_listbox.insert(tk.END,"Calculated X BPM")
    ax1.cla()
    ax1.plot(data[start:end])


    labels = np.arange(start/sample_rate,end/sample_rate,(end-start)/(10*sample_rate))
    labels_rounded = [round(num, 1) for num in labels]
    
    vals = [(num*sample_rate - start) for num in labels_rounded]
    ax1.set_xticks(vals)
    
    ax1.set_xticklabels(labels_rounded)
    #ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/sample_rate))
    #ax.xaxis.set_major_formatter(ticks_x)
    ax1.set_xlabel('Time (seconds)', fontsize=16)
    ax1.set_ylabel('Signal Strength', fontsize=16)
    
    canvas.draw()


window.bind('<Return>',write)

search_frame = tk.Frame(master = window)
option_frame = tk.Frame(master = window)
info_frame = tk.Frame(master = window)
display_frame = tk.Frame(master=window)
separator = ttk.Separator(master = window, orient='horizontal')


search_frame.pack(side = tk.TOP, fill = tk.BOTH)
separator.pack(fill='x')
option_frame.pack(side = tk.TOP, fill = tk.BOTH)
info_frame.pack(side = tk.TOP, fill = tk.BOTH)
display_frame.pack(side = tk.TOP, fill = tk.BOTH)

search_label = tk.Label(master = search_frame, text = "File Search: ", justify = tk.LEFT)
search_textbox = tk.Entry(master = search_frame, width = 75)
search_button = tk.Button(text = "Search", master = search_frame, command = browsefunc)
run_button = tk.Button(text = "Filter", master = search_frame, command = write)


search_label.pack(side = tk.LEFT)
search_textbox.pack(side = tk.LEFT, expand = True)
search_button.pack(side = tk.LEFT)
run_button.pack(side=tk.LEFT)

#option frame
t1_str=tk.StringVar()
t2_str=tk.StringVar()
t1_str.set("00:00:00")
t2_str.set("00:00:22")

option_label = tk.Label(master = option_frame, text = "Adjust time range: ", justify = tk.LEFT)
option_time1 = tk.Entry(master = option_frame, textvariable=t1_str)
option_time2 = tk.Entry(master = option_frame, textvariable=t2_str)
option_button = tk.Button(text = "Adjust Range", master = option_frame, command = dofilter)
period_slider = tk.Scale(master = option_frame, from_=0, to_=1, resolution=0.01, orient='horizontal')
prominence_slider = tk.Scale(master = option_frame, from_=0, to_=1, resolution=0.01, orient='horizontal')

period_slider.set(0.11)
prominence_slider.set(1)

option_label.pack(side = tk.LEFT)
option_time1.pack(side = tk.LEFT)
option_time2.pack(side = tk.LEFT)
period_slider.pack(side=tk.LEFT, expand=True)
prominence_slider.pack(side=tk.LEFT, expand=True)
option_button.pack(side = tk.LEFT)

for child in option_frame.winfo_children():
    child.configure(state='disable')

#listbox to display returned info
info_listbox = tk.Listbox(master = info_frame, width = 125, height = 10)
info_listbox.pack(side = tk.LEFT, fill = tk.Y)
info_listbox.insert(tk.END, "")
info_listbox.insert(tk.END, " Count information returned here")

#scrollbar for info listbox
scrollbar = tk.Scrollbar(master = info_frame)
scrollbar.pack(side = tk.LEFT, fill = tk.Y)

#associate scrollbar with info listbox
info_listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = info_listbox.yview)

canvas_width = 500
canvas_height = 500

#canvas = tk.Canvas(master = display_frame, width = canvas_width, height = canvas_height)
canvas = FigureCanvasTkAgg(fig, master=window)

#Scrollbars for the canvas

hscrollbar = tk.Scrollbar(master = display_frame, orient = tk.HORIZONTAL)
hscrollbar.pack(side = tk.BOTTOM, fill = tk.X)
hscrollbar.config(command = canvas.get_tk_widget().xview) 

vscrollbar = tk.Scrollbar(master = display_frame, orient = tk.VERTICAL)
vscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
vscrollbar.config(command = canvas.get_tk_widget().yview) 

#Associate the scrollbars with the canvas
canvas.get_tk_widget().config(width = canvas_width, height = canvas_height)
canvas.get_tk_widget().config(xscrollcommand = hscrollbar.set, yscrollcommand = vscrollbar.set)

#Pack canvas
canvas.get_tk_widget().pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

canvas.get_tk_widget().create_text(110, 25, text="Graph to be displayed here...")

window.mainloop()
