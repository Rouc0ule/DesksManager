import tkinter as tk 
from myTkinter import GUITkinter

root = tk.Tk()

def prunt():
    print('clicked !')

GUITkinter.Button(root, corner_radius=250, command=prunt)

root.mainloop()