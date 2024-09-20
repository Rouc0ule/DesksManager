import tkinter as tk

class DragManager:
    def __init__(self, canvas, grid_size=20):
        self.canvas = canvas
        self.item = None
        self.rotate_mode = False
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