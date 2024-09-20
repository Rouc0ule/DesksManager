import tkinter as tk
from PIL import ImageTk, Image

class DragManager:
    def __init__(self, canvas, grid_size=20):
        self.canvas = canvas
        self.item = None
        self.delete_mode = False
        self.grid_size = grid_size

    def add_draggable(self, tag):
        self.canvas.tag_bind(tag, '<ButtonPress-1>', self.on_start)
        self.canvas.tag_bind(tag, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(tag, '<ButtonRelease-1>', self.on_drop)

    def on_start(self, event):
        self.item = self.canvas.find_withtag(tk.CURRENT)[0]
        if self.delete_mode == True:
            self.delete_item(self.item)
            return
        self.start_x = event.x
        self.start_y = event.y
        tag = self.canvas.gettags(self.item)[0]
        self.canvas.tag_raise(tag)

    def delete_item(self, item):
        tags = self.canvas.gettags(item)
        if tags:
            tag = tags[0]
            self.canvas.delete(tag)
        else:
            self.canvas.delete(item)

    def on_drag(self, event):
        if not self.item:
            return
        
        tag = self.canvas.gettags(self.item)[0]
        coords = self.canvas.coords(tag)
        
        if len(coords) < 4:
            print(f"Warning: Invalid coordinates for item {self.item}")
            return
        
        width = coords[2] - coords[0]
        height = coords[3] - coords[1]
        
        new_x = round((event.x - width / 2) / self.grid_size) * self.grid_size
        new_y = round((event.y - height / 2) / self.grid_size) * self.grid_size
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        new_x = max(0, min(new_x, canvas_width - width))
        new_y = max(0, min(new_y, canvas_height - height))
        
        delta_x = new_x - coords[0]
        delta_y = new_y - coords[1]
        
        self.canvas.move(tag, delta_x, delta_y)
        self.canvas.tag_raise(tag) 

    def on_drop(self, event):
        self.item = None

def create_grid(event=None):
    canvas.delete('grid_line')
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    for i in range(0, w, grid_size):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill='#3aa13a', width=0.5)
    for i in range(0, h, grid_size):
        canvas.create_line([(0, i), (w, i)], tag='grid_line', fill='#3aa13a', width=0.5)

def add_desk():
    grid_size = 20
    x1, y1 = 20, 20  
    width, height = 8 * grid_size, 4 * grid_size
    x2, y2 = x1 + width, y1 + height
    
    tag = f"node-{len(canvas.find_all())}"
    
    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#662100", tags=tag)
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Desk', fill="#ffffff", tags=tag)
    
    drag_manager.add_draggable(tag)

def add_student():
    grid_size = 20
    x1, y1 = 20, 20  
    width, height = 4 * grid_size, 2 * grid_size
    x2, y2 = x1 + width, y1 + height
    
    tag = f"node-{len(canvas.find_all())}"
    
    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#000066", outline="#0000ff", tags=tag)
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Student', fill="#ffffff", tags=tag)
    
    drag_manager.add_draggable(tag)

def delete():
    global drag_manager
    if drag_manager.delete_mode == False :
        dlt_btn.config(relief=tk.SUNKEN)
        drag_manager.delete_mode = True
        print(drag_manager.delete_mode)
    elif drag_manager.delete_mode == True :
        dlt_btn.config(relief=tk.RAISED)
        drag_manager.delete_mode = False
        print(drag_manager.delete_mode)

root = tk.Tk()
root.title('DesksManager')

theme = 'light'
grid_size = 20

add_desk_img = ImageTk.PhotoImage(Image.open("Assets/{}_plus_rectangle.png".format(theme)).resize((25,25)))
add_student_img = ImageTk.PhotoImage(Image.open("Assets/{}_person_badge_plus_fill.png".format(theme)).resize((25,25)))
dlt_img = ImageTk.PhotoImage(Image.open("Assets/{}_delete.png".format(theme)).resize((25,25)))

control_frame = tk.Frame(root, width=400)
control_frame.pack(side='left')

add_desk_btn = tk.Button(control_frame, text='Add desk', font=("San Francisco", 9, 'bold'), image=add_desk_img, compound='left', width=100, command=add_desk)
add_desk_btn.grid(row=0, column=0, padx=(10, 5), pady=5)
add_student_btn = tk.Button(control_frame, text='Add student', font=("San Francisco", 9, 'bold'), image=add_student_img, compound='left', width=100, command=add_student)
add_student_btn.grid(row=0, column=1, padx=(5, 10), pady=5)

dlt_btn = tk.Button(control_frame, text='Delete', font=("San Francisco", 9, 'bold'), image=dlt_img, compound='left', width=218, command=delete)
dlt_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

canvas_frame = tk.Frame(root)
canvas_frame.pack(side='right')

canvas = tk.Canvas(canvas_frame, width=1000, height=800, background="#383")
canvas.pack(padx=8, pady=8)

drag_manager = DragManager(canvas, grid_size)

canvas.bind('<Configure>', create_grid)

root.mainloop()