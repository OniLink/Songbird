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
root.geometry("500x500")
row, column = root.grid_size()

ent1=tk.Entry(root,font=40)
ent1.grid(row=2,column=2)

def browsefunc():
    filename = filedialog.askopenfilename(filetypes=(("wav files","*.wav"),("All files","*.*")))
    ent1.delete(0, tk.END)
    ent1.insert(tk.END, filename)

def write():
    writeToFile(ent1.get(), "deleteme.wav");
    dofilter()

def dofilter():
    fig = mpl.figure.Figure(figsize = (5,5), dpi=100)

    input_data = read("deleteme.wav")[1]

    plot1 = fig.add_subplot(111)
    plot1.plot(input_data)
    #plot1.title("Unfiltered")

    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=10,column=2)

    ent1=tk.Entry(root,font=40)
    ent1.grid(row=20,column=2)
    #ent1.bind('<Return>',function)

    #toolbar = NavigationToolbar2Tk(canvas, root)
    #toolbar.update()

    #canvas.get_tk_widget().grid(row=12,column=0)

    #plt.plot(input_data[0:1000])
    #plt.show()

def viewWav():
    pass
    

b1=tk.Button(root,text="Browse",font=40,command=browsefunc)
b2=tk.Button(root,text="filter",font=40,command=write)
b1.grid(row=2,column=12)
b2.grid(row=row,column=12)




root.mainloop()
