import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from filter import writeToFile

window = tk.Tk()
window.title("Heartbeat GUI")


fig, ax = plt.subplots()

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
    sample_rate, data = writeToFile(search_textbox.get(), "deleteme.wav")
    for child in option_frame.winfo_children():
        child.configure(state='normal')
    
    dofilter()

def dofilter():
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
    ax.cla()
    ax.plot(data[start:end])


    labels = np.arange(start/sample_rate,end/sample_rate,(end-start)/(20*sample_rate))
    labels_rounded = [round(num, 1) for num in labels]
    
    vals = [(num*sample_rate - start) for num in labels_rounded]
    ax.set_xticks(vals)
    
    ax.set_xticklabels(labels_rounded)
    #ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/sample_rate))
    #ax.xaxis.set_major_formatter(ticks_x)
    ax.set_xlabel('Time (seconds)', fontsize=16)
    ax.set_ylabel('Signal Strength', fontsize=16)
    
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
t2_str.set("00:00:10")

option_label = tk.Label(master = option_frame, text = "Adjust time range: ", justify = tk.LEFT)
option_time1 = tk.Entry(master = option_frame, textvariable=t1_str)
option_time2 = tk.Entry(master = option_frame, textvariable=t2_str)
option_button = tk.Button(text = "Adjust Range", master = option_frame, command = dofilter)

option_label.pack(side = tk.LEFT)
option_time1.pack(side = tk.LEFT)
option_time2.pack(side = tk.LEFT)
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