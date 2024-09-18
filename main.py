import tkinter as tk
from jsonloader import *
from PIL import ImageTk, Image
import pyautogui
import os
import pywinstyles

def add_desk():
    desk.place(x=0, y=0)

class myDragManager():
    def add_dragable_widget(self, widget):
        self.widget = widget
        self.root = widget.winfo_toplevel()

        self.widget.bind("<B1-Motion>", self.on_drag)
        self.widget.bind("<ButtonRelease>", self.on_drop)
        self.widget.configure(cursor="hand1")

    def on_drag(self, event):
        #x,y = pyautogui.position()
        self.widget.place(x=self.root.winfo_pointerx()-self.root.winfo_rootx()-(self.widget.winfo_width()/2), y=self.root.winfo_pointery()-self.root.winfo_rooty()-(self.widget.winfo_height()))
    
    def on_drop(self, event):
        #x,y = pyautogui.position()
        self.widget.place(x=self.root.winfo_pointerx()-self.root.winfo_rootx()-(self.widget.winfo_width()/2), y=self.root.winfo_pointery()-self.root.winfo_rooty()-(self.widget.winfo_height()))

root = tk.Tk()
root.title("DesksOrganiser")
root.geometry("800x500")
root.configure()
#pywinstyles.apply_style(root, "acrylic")

deskimg = ImageTk.PhotoImage(Image.open("Assets/deskpng.png").resize((125,50)))

# sideframe = tk.Frame(root, background='gray')
# sideframe.pack(side='left', fill='y')

# l1 = tk.Label(sideframe, text='Student list', font=("San Francisco", 10, "bold"))
# l1.pack(padx=50, pady=10)

topframe = tk.Frame(root, height=50, background='lightgray')
topframe.pack(side='top', fill='x')

add_desk_btn = tk.Button(topframe, text='Add desk', font=("San Francisco", 9), command=add_desk)
add_desk_btn.pack(padx=5,pady=5)

roomframe = tk.Frame(root, background='darkgray')
roomframe.pack(side='right', expand=True, fill="both")

desk = tk.Label(roomframe, image = deskimg, bg='darkgray')

print(desk.winfo_height)

#l = tk.Label(roomframe, text="Label").place(relx=0.5, rely=0.5)

mydrag1 = myDragManager()
mydrag1.add_dragable_widget(desk)

root.mainloop()