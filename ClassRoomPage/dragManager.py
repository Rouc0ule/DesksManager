import tkinter as tk

class DragManager:
    def __init__(self, canvas, grid_size=20):
        self.canvas = canvas
        self.item = None
        self.move_mode = True
        self.rotate_mode = False
        self.delete_mode = False
        self.grid_size = grid_size

    def add_draggable(self, tag):
        self.canvas.tag_bind(tag, '<ButtonPress-1>', self.on_start)
        self.canvas.tag_bind(tag, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(tag, '<ButtonRelease-1>', self.on_drop)

    def on_start(self, event):
        self.item = self.canvas.find_withtag(tk.CURRENT)[0]
        if self.delete_mode:
            self.delete_item(self.item)
            return
        elif self.rotate_mode:
            self.rotate_item(self.item)
            return
        elif self.move_mode:
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

    def rotate_item(self, item):
        tags = self.canvas.gettags(item)
        if tags:
            main_tag = tags[0]
            rotation_tag = next((tag for tag in tags if tag.startswith(f"{main_tag}_rotation_")), None)
            if rotation_tag:
                current_rotation = int(rotation_tag.split('_')[-1])
                new_rotation = (current_rotation + 90) % 360
                new_rotation_tag = f"{main_tag}_rotation_{new_rotation}"

                # Mise à jour des tags
                self.canvas.dtag(item, rotation_tag)
                self.canvas.addtag_withtag(new_rotation_tag, main_tag)

                # Rotation du rectangle
                x1, y1, x2, y2 = self.canvas.coords(main_tag)
                center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
                width, height = x2 - x1, y2 - y1
                if new_rotation in [90, 270]:
                    width, height = height, width
                new_coords = [center_x - width/2, center_y - height/2, center_x + width/2, center_y + height/2]
                self.canvas.coords(main_tag, *new_coords)

                # Rotation du texte
                self.rotate_text(main_tag, new_rotation)
    
    def rotate_text(self, tag, rotation):
        text_item = self.canvas.find_withtag(f"{tag}&&text")
        if text_item:
            x1, y1, x2, y2 = self.canvas.coords(tag)
            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.coords(text_item, center_x, center_y)
            self.canvas.itemconfig(text_item, angle=rotation)

    def update_grid_size(self, new_grid_size):
        self.grid_size = new_grid_size

    def on_drag(self, event):
        if not self.item or not self.move_mode:
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