import tkinter as tk

def add_desk():
    desk = tk.Label(plan_root, text='DESK', bg='orange', fg='white', width=10)
    desk.place(x=10, y=10)
    deskdrag = myDragManager()
    deskdrag.add_dragable_widget(desk)

def add_student():
    student = tk.Label(plan_root, text='STUDENT', bg='gray', fg='white', width=10)
    student.place(x=10, y=10)
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
        print(self.widget.winfo_rootx(), self.widget.winfo_rooty())

plan_root = tk.Tk()
plan_root.title('Plan')
plan_root.geometry('600x400+100+100')

commands_root = tk.Tk()
commands_root.title('Commands')
commands_root.geometry('250x400+700+100')

commands_frame = tk.Frame(commands_root)
commands_frame.pack(padx=20,pady=20)

add_desk_btn = tk.Button(commands_frame, text='Add Desk', command=add_desk)
add_desk_btn.grid(column=0, row=0, padx=5, pady=5)
add_student_btn = tk.Button(commands_frame, text='Add Student', command=add_student)
add_student_btn.grid(column=0, row=1, padx=5, pady=5)

plan_root.mainloop()
commands_root.mainloop()