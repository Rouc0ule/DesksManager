import tkinter as tk
from jsonloader import *
from PIL import ImageTk, Image
import pyautogui
import os
import pywinstyles

def add_desk():
    desk = tk.Label(roomframe, image = deskimg)
    desk.place(x=0, y=0)
    deskdrag = myDragManager()
    deskdrag.add_dragable_widget(desk)

def add_student():
    student = tk.Label(roomframe, image = studentimg)
    student.place(x=0, y=0)
    studentdrag = myDragManager()
    studentdrag.add_dragable_widget(student)

class myDragManager():
    def add_dragable_widget(self, widget):
        self.widget = widget
        self.root = widget.winfo_toplevel()

        self.widget.bind("<B1-Motion>", self.on_drag)
        self.widget.bind("<ButtonRelease>", self.on_drop)
        self.widget.configure(cursor="hand1")

    def on_drag(self, event):
        #x,y = pyautogui.position()
        self.widget.place(x=round(self.root.winfo_pointerx()-self.root.winfo_rootx()-(self.widget.winfo_width()/2), -1), y=round(self.root.winfo_pointery()-self.root.winfo_rooty()-(self.widget.winfo_height()), -1))
    
    def on_drop(self, event):
        #x,y = pyautogui.position()
        self.widget.place(x=round(self.root.winfo_pointerx()-self.root.winfo_rootx()-(self.widget.winfo_width()/2), -1), y=round(self.root.winfo_pointery()-self.root.winfo_rooty()-(self.widget.winfo_height()), -1))

root = tk.Tk()
root.title("DesksOrganiser")
root.geometry("800x500")
root.configure()
#pywinstyles.apply_style(root, "acrylic")

deskimg = ImageTk.PhotoImage(Image.open("Assets/deskpng.png").resize((100,50)))
studentimg = ImageTk.PhotoImage(Image.open("Assets/Person Fill.png").resize((50,50)))

# sideframe = tk.Frame(root, background='gray')
# sideframe.pack(side='left', fill='y')

# l1 = tk.Label(sideframe, text='Student list', font=("San Francisco", 10, "bold"))
# l1.pack(padx=50, pady=10)

topframe = tk.Frame(root, height=50, background='lightgray')
topframe.pack(side='top', fill='x')

add_desk_btn = tk.Button(topframe, text='Add desk', font=("San Francisco", 9), command=add_desk)
add_desk_btn.pack(padx=5,pady=5)

add_student_btn = tk.Button(topframe, text='Add Student', font=("San Francisco", 9), command=add_student)
add_student_btn.pack(padx=5,pady=5)

roomframe = tk.Frame(root, background='darkgray')
roomframe.pack(side='right', expand=True, fill="both")

#l = tk.Label(roomframe, text="Label").place(relx=0.5, rely=0.5)

root.mainloop()