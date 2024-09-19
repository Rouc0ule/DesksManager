import tkinter as tk

class DragManager:
    def __init__(self, canvas, grid_size=20):
        self.canvas = canvas
        self.item = None
        self.grid_size = grid_size

    def add_draggable(self, tag):
        self.canvas.tag_bind(tag, '<ButtonPress-1>', self.on_start)
        self.canvas.tag_bind(tag, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(tag, '<ButtonRelease-1>', self.on_drop)

    def on_start(self, event):
        self.item = self.canvas.find_withtag(tk.CURRENT)[0]
        self.start_x = event.x
        self.start_y = event.y
        tag = self.canvas.gettags(self.item)[0]
        self.canvas.tag_raise(tag)  # Élever l'objet au-dessus des autres

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
        
        delta_x = new_x - coords[0]
        delta_y = new_y - coords[1]
        
        self.canvas.move(tag, delta_x, delta_y)
        self.canvas.tag_raise(tag)  # Maintenir l'objet au-dessus pendant le déplacement

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
    width, height = 4 * grid_size, 2 * grid_size
    x2, y2 = x1 + width, y1 + height
    
    tag = f"node-{len(canvas.find_all())}"
    
    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#662100", tags=tag)
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Desk', fill="#ffffff", tags=tag)
    
    drag_manager.add_draggable(tag)

def add_student():
    grid_size = 20
    x1, y1 = 20, 20  
    width, height = 2 * grid_size, 1 * grid_size
    x2, y2 = x1 + width, y1 + height
    
    tag = f"node-{len(canvas.find_all())}"
    
    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#000066", outline="#0000ff", tags=tag)
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Student', fill="#ffffff", tags=tag)
    
    drag_manager.add_draggable(tag)

root = tk.Tk()
root.title('DesksManager')
grid_size = 20

control_frame = tk.Frame(root)
control_frame.pack()

add_desk_btn = tk.Button(control_frame, text='Add desk', command=add_desk)
add_desk_btn.grid(row=0, column=0, padx=5)
add_student_btn = tk.Button(control_frame, text='Add student', command=add_student)
add_student_btn.grid(row=0, column=1, padx=5)


canvas = tk.Canvas(root, width=500, height=500, background="#383")
canvas.pack(padx=8, pady=8)

drag_manager = DragManager(canvas, grid_size)

canvas.bind('<Configure>', create_grid)

root.mainloop()
