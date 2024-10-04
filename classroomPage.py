import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from dragManager import DragManager
from uniqueTagGenerator import UniqueTagGenerator
from GUI import GUIButton

class ClassroomPage:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.grid_size = 20
        self.load_images()
        self.setup_frames()
        self.setup_canvas()
        self.setup_widgets()
        self.pack_widgets()
        self.drag_manager.move_mode = True
        self.move()
        
    def load_images(self):
        image_names = ["plus_rectangle", "person_badge_plus_fill", "delete", "rotate_left", "move", "plus_circle"]
        self.plus_rectangle_img = self.load_image('plus_rectangle')
        self.person_badge_plus_fill_img = self.load_image('person_badge_plus_fill')
        self.delete_img = self.load_image('delete')
        self.rotate_left_img = self.load_image('rotate_left')
        self.move_img = self.load_image('move')
        self.plus_circle_img = self.load_image('plus_circle')
        print(self.plus_rectangle_img)

    def load_image(self, name, size=(25, 25)):
        return ImageTk.PhotoImage(Image.open(f"Assets/{self.theme}_{name}.png").resize(size))

    def setup_frames(self):
        self.bottom_frame = tk.Frame(self.root)
        # self.control_frame = tk.LabelFrame(self.bottom_frame, text='Commands', width=400)
        # self.control_topframe = tk.Frame(self.control_frame)
        # self.control_middleframe = tk.Frame(self.control_frame)
        # self.control_bottomframe = tk.Frame(self.control_frame)
        self.canvas_frame = tk.Frame(self.root)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.canvas_frame, width=1000, height=800, background="#383", highlightthickness=0)
        self.drag_manager = DragManager(self.canvas, self.grid_size)
        self.canvas.bind('<Configure>', lambda event: self.create_grid())
        self.tag_generator = UniqueTagGenerator()

    def setup_widgets(self):
        self.add_student_btn = GUIButton(self.bottom_frame, width=35, radius=20, text='', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', image=self.person_badge_plus_fill_img, compound='left', command=self.add_student)
        self.add_desk_btn = GUIButton(self.bottom_frame, width=35, radius=20, text='', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', image=self.plus_rectangle_img, compound='left', command=self.add_desk)
        self.move_btn = GUIButton(self.bottom_frame, radius=20, text='Move', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', image=None, command=self.move)
        self.rotate_btn = GUIButton(self.bottom_frame, radius=20, text='Rotate', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', image=None, command=self.rotate)
        self.delete_btn = GUIButton(self.bottom_frame, radius=20, text='Delete', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', image=None, command=self.delete)

    def pack_widgets(self):
        self.bottom_frame.pack(side='bottom', anchor='sw')
        # self.control_frame.pack()
        # self.control_topframe.pack(fill='x')
        # self.control_middleframe.pack(fill='x')
        # self.control_bottomframe.pack(fill='x')
        self.canvas_frame.pack(side='right', padx=10)

        self.add_student_btn.pack(side='left', padx=5, pady=5)
        self.add_desk_btn.pack(side='left', padx=5, pady=5)
        self.move_btn.pack(side='left', padx=5, pady=5)
        self.rotate_btn.pack(side='left', padx=5, pady=5)
        self.delete_btn.pack(side='left', padx=5, pady=5)
        
        self.canvas.pack()

    def create_grid(self):
        self.canvas.delete('grid_line')
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i in range(0, w, self.grid_size):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill='#3aa13a', width=0.5)
        for i in range(0, h, self.grid_size):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line', fill='#3aa13a', width=0.5)

    def add_desk(self):
        x1, y1 = 20, 20  
        width, height = 8 * self.grid_size, 4 * self.grid_size
        x2, y2 = x1 + width, y1 + height
        
        self.set_modes(True, False, False)
        
        tag = self.tag_generator.next_tag()
        rotation_tag = f"{tag}_rotation_0"

        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#662100", tags=(tag, rotation_tag))
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Desk', fill="#ffffff", tags=(tag, rotation_tag))
        
        self.drag_manager.add_draggable(tag)

    def add_student(self):
        x1, y1 = 20, 20  
        width, height = 4 * self.grid_size, 2 * self.grid_size
        x2, y2 = x1 + width, y1 + height

        self.set_modes(True, False, False)
        
        tag = self.tag_generator.next_tag()
        rotation_tag = f"{tag}_rotation_0"

        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#000066", outline="#0000ff", tags=(tag, rotation_tag))
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Student', fill="#ffffff", tags=(tag, rotation_tag))
        
        self.drag_manager.add_draggable(tag)

    def rotate(self):
        self.set_modes(False, True, False)

    def delete(self):
        self.set_modes(False, False, True)

    def move(self):
        self.set_modes(True, False, False)

    def set_modes(self, is_move_mode, is_rotate_mode, is_delete_mode):
        self.drag_manager.move_mode = is_move_mode
        self.drag_manager.rotate_mode = is_rotate_mode
        self.drag_manager.delete_mode = is_delete_mode
        if is_move_mode:
            self.move_btn.color = '#8d8d8d'
            self.move_btn.hover_color = '#5a5a5a'
        else:
            self.move_btn.color = '#d3d3d3'
            self.move_btn.hover_color = '#a0a0a0'

        if is_rotate_mode:
            self.rotate_btn.color = '#8d8d8d'
            self.rotate_btn.hover_color = '#5a5a5a'
        else:
            self.rotate_btn.color = '#d3d3d3'
            self.rotate_btn.hover_color = '#a0a0a0'

        if is_delete_mode:
            self.delete_btn.color = '#8d8d8d'
            self.delete_btn.hover_color = '#5a5a5a'
        else:
            self.delete_btn.color = '#d3d3d3'
            self.delete_btn.hover_color = '#a0a0a0'
        
        self.move_btn.update_button_size()
        self.rotate_btn.update_button_size()
        self.delete_btn.update_button_size()
