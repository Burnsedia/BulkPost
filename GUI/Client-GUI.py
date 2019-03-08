import tkinter as tk
from tkinter import *

LARGE_FONT = ("Monospace", 12)
class root(Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.title = "BulkPost"
        container = tk.Frame()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = StartPage(self,container)
        self.frames[StartPage] = frame
        frame.grid(row=0, column = 0, sticky = "nsew")

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controler):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Manu", font= LARGE_FONT)
        label.pack(pady = 10, padx=10)



root =root()

root.mainloop()