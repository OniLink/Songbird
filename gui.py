import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from matplotlib.ft2font import HORIZONTAL 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from sympy import true
import heart_filter
import beat_count
from scipy.io import wavfile
import time
import math


window = tk.Tk()
window.title("Heartbeat GUI")


#fig, (ax1,ax2) = plt.subplots(1,2)
fig, ax1 = plt.subplots()

def isHHMMSS(time_string):
    try:
        time.strptime(time_string, "%H:%M:%S")
    except ValueError:
        return False
    return True

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
    sample_rate, data_raw = wavfile.read(search_textbox.get())

    data = heart_filter.data_filter(data_raw, sample_rate)
    wavfile.write("filtered_file.wav", sample_rate, data)
    option_button.configure(state='normal')
    dofilter()

def peak_count_data(initial_index, sample_rate, data, segment_length, min_xbill_period, prominence_scale=1):
    bpm_arr = []
    peaklist = []
    total_length = len(data) / float(sample_rate)
    for i in range(0, math.floor(total_length/segment_length)):
        segment = data[i * sample_rate * segment_length : (i+1) * sample_rate * segment_length]

        max_sound = max(segment[:]) #looks at loudest peak in set of peaks
        avg_sound = np.median(segment[:]) #looks at median of noise

        # variable for the sliders if yall want
        distance = beat_count.calculate_distance(sample_rate, min_xbill_period) 
        prominence = beat_count.calculate_prominence(max_sound, avg_sound) * prominence_scale

        peaks = beat_count.peak_count(segment, distance, prominence)
        for p in peaks:
            peaklist.append((p + (i * sample_rate * segment_length) + initial_index))
        seg_bpm = beat_count.bpm(sample_rate, segment, peaks)
        info_listbox.insert(tk.END, f"bpm: {seg_bpm}, [{time.strftime('%H:%M:%S', time.gmtime(int(initial_index/sample_rate + (i * segment_length))))}]")
        bpm_arr.append(seg_bpm)
    return beat_count.calculate_average_bpm(bpm_arr),peaklist

def dofilter():
    print("Adjusting filter")

    #get inputs
    minimum=option_time1.get()
    maximum=option_time2.get()

    #input check
    if (not isHHMMSS(minimum) or not isHHMMSS(maximum)):
        info_listbox.insert(tk.END, "\nPlease insert times in hh:mm:ss format\n")
        return 1

    #convert inputs into sample rate based indicies
    start = toIndex(list(map(int,minimum.split(':')))) * sample_rate
    end = toIndex(list(map(int,maximum.split(':')))) * sample_rate

    #input check
    if (start >= end):
        info_listbox.insert(tk.END, "Please check that start time is earlier than end time")
        return 1

    if (end > len(data) or start < 0):
        info_listbox.insert(tk.END, "Please check that the selected time range is within the length of the file")
        return 1

    info_listbox.delete(0,tk.END)
    avgbpm,peaks = peak_count_data(start, sample_rate,data[start:end],5,period_slider.get(),prominence_slider.get())

    #clear plot and plot points
    ax1.cla()
    ax1.plot(data[start:end])

    peaks = list(map(lambda x: x-start, peaks))

    ax1.plot(peaks, data[start:end][peaks], "x")
    info_listbox.insert(tk.END, f"Overall bpm: {avgbpm}")


    num_labels = 10 if((end-start)/sample_rate >= 10) else 5
    labels = np.arange(start/sample_rate,end/sample_rate,(end-start)/(num_labels*sample_rate))
    labels_rounded = [round(num, 1) for num in labels]
    
    vals = [(num*sample_rate - start) for num in labels_rounded]
    ax1.set_xticks(vals)

    labels_rounded = [time.strftime('%H:%M:%S', time.gmtime(int(num))) for num in labels_rounded]
    
    ax1.set_xticklabels(labels_rounded)

    ax1.set_xlabel('Time (hh:mm:ss)', fontsize=16)
    ax1.set_ylabel('Signal Strength', fontsize=16)
    
    canvas.draw()


window.bind('<Return>',dofilter)

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
t2_str.set("00:00:05")

option_label = tk.Label(master = option_frame, text = "Time Range (HH:MM:SS): ", justify = tk.LEFT)
option_time1 = tk.Entry(master = option_frame, textvariable=t1_str)
option_time2 = tk.Entry(master = option_frame, textvariable=t2_str)

option_slider_frame1 = tk.Frame(master = option_frame)
option_slider_label1 = tk.Label(master = option_slider_frame1, text = "Minimum Period Slider: ", justify = tk.LEFT)
period_slider = tk.Scale(master = option_slider_frame1, from_=0, to_=1, resolution=0.01, orient='horizontal')
option_slider_label1.pack(side=tk.TOP)
period_slider.pack(side=tk.BOTTOM)

option_slider_frame2 = tk.Frame(master = option_frame)
option_slider_label2 = tk.Label(master = option_slider_frame2, text = "Prominence Slider: ", justify = tk.LEFT)
prominence_slider = tk.Scale(master = option_slider_frame2, from_=0, to_=1, resolution=0.01, orient='horizontal')
option_slider_label2.pack(side=tk.TOP)
prominence_slider.pack(side=tk.BOTTOM)

option_button = tk.Button(text = "Adjust Range", master = option_frame, command = dofilter)

period_slider.set(0.09)
prominence_slider.set(0.96)

option_label.pack(side = tk.LEFT)
option_time1.pack(side = tk.LEFT)
option_time2.pack(side = tk.LEFT)
option_slider_frame1.pack(side=tk.LEFT, expand=True)
option_slider_frame2.pack(side=tk.LEFT, expand=True)
option_button.pack(side = tk.LEFT)

option_button.configure(state='disable')

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

#canvas_width = 500
#canvas_height = 500
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
