from filter import writeToFile
import tkinter as tk
from tkinter import filedialog
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import os
from scipy.io.wavfile import read

root = tk.Tk()

root.title("GUI!")
root.geometry("1000x1000")
row, column = root.grid_size()

#fig, ax = plt.figure(figsize=(4,5))
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=10, column=5, ipadx=40, ipady=20)

#naviation toolbar
toolbarFrame = tk.Frame(master=root)
toolbarFrame.grid(row=11,column=5)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

def browsefunc():
    filename = filedialog.askopenfilename(filetypes=(("wav files","*.wav"),("All files","*.*")))
    ent1.delete(0, tk.END)
    ent1.insert(tk.END, filename)

def write():
    global data
    global sample_rate
    sample_rate, data = writeToFile(ent1.get(), "deleteme.wav");
    b3['state'] = 'normal'
    dofilter()

def toIndex(arr):
    return (3600*arr[0] + 60*arr[1] + arr[2]) * sample_rate

def dofilter():
    minimum=ent2.get()
    mins = list(map(int,minimum.split(':')))
    maximum=ent3.get()
    maxs = list(map(int,maximum.split(':')))

    start = toIndex(mins)
    end = toIndex(maxs)

    #minimum = (int(minimum)) if (minimum != '') else 0
    #maximum = (int(maximum)) if (maximum != '') else 1024

    #input_data = read("deleteme.wav")[1]

    #plt.clf()
    ax.cla()
    ax.plot(data[start:end])
    canvas.draw()

    #specify window as master

def viewWav():
    pass
    

b1=tk.Button(root,text="Browse",font=40,command=browsefunc)
b2=tk.Button(root,text="filter",font=40,command=write)
b3=tk.Button(root,text="adjust range", font=40, command=dofilter)
b3['state'] = 'disabled'

e2_str=tk.StringVar()
e3_str=tk.StringVar()
e2_str.set("00:00:00")
e3_str.set("00:00:00")

ent1=tk.Entry(root,font=40)
ent2=tk.Entry(root,textvariable=e2_str,font=40)
ent3=tk.Entry(root,textvariable=e3_str,font=40)

b1.grid(row=0,column=0)
ent1.grid(row=2,column=0)

ent2.grid(row=5,column=0)

ent3.grid(row=5,column=1)

b3.grid(row=5,column=2)

b2.grid(row=6,column=0)

root.mainloop()
