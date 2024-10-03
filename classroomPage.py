import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from dragManager import DragManager
from uniqueTagGenerator import UniqueTagGenerator
from jsonloader import JsonManager
from functions import create_grid, add_desk, add_student, move, rotate, delete, center_window
from GUI import GUIButton

class ClassroomPage:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.grid_size = 20
        self.number_of_items = 0
        self.load_images()
        self.setup_frames()
        self.setup_widgets()
        self.setup_canvas()
        
    def load_images(self):
        self.add_desk_img = self.load_image("plus_rectangle")
        self.add_student_img = self.load_image("person_badge_plus_fill")
        self.delete_img = self.load_image("delete")
        self.rotate_img = self.load_image("rotate_left")
        self.move_img = self.load_image("move")
        self.plus_img = self.load_image("plus_circle")

    def load_image(self, name, size=(25, 25)):
        return ImageTk.PhotoImage(Image.open(f"Assets/{self.theme}_{name}.png").resize(size))

    def setup_frames(self):
        self.left_frame = tk.Frame(self.root)
        self.control_frame = tk.LabelFrame(self.left_frame, text='Commands', width=400)
        self.control_topframe = tk.Frame(self.control_frame)
        self.control_middleframe = tk.Frame(self.control_frame)
        self.control_bottomframe = tk.Frame(self.control_frame)
        self.student_list_frame = tk.LabelFrame(self.left_frame, text='List')
        self.student_list_topframe = tk.Frame(self.student_list_frame)
        self.student_list_middleframe = tk.Frame(self.student_list_frame)
        self.student_list_box_frame = tk.Frame(self.student_list_frame)
        self.canvas_frame = tk.Frame(self.root)

    def setup_widgets(self):
        # self.add_desk_btn = ttk.Button(self.control_topframe, text='Add desk', image=self.add_desk_img, compound='left', width=12, command=self.add_desk_command)
        # self.add_student_btn = ttk.Button(self.control_topframe, text='Add student', image=self.add_student_img, compound='left', width=12, command=self.add_student_command)
        # self.move_btn = ttk.Button(self.control_middleframe, text='Move', image=self.move_img, compound='left', command=self.move_command)
        self.rotate_btn = ttk.Button(self.control_bottomframe, text='Rotate', image=self.rotate_img, compound='left', width=12, command=self.rotate_command)
        self.delete_btn = ttk.Button(self.control_bottomframe, text='Delete', image=self.delete_img, compound='left', width=12, command=self.delete)

        self.add_desk_btn2 = GUIButton(self.control_topframe, text='Add desk', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', command=lambda: add_desk(self.canvas, self.grid_size, self.tag_generator, self.drag_manager, self.move_btn2, self.rotate_btn, self.delete_btn))
        self.add_student_btn2 = GUIButton(self.control_topframe, text='Add student', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', command=lambda: add_student(self.canvas, self.grid_size, self.tag_generator, self.drag_manager, self.move_btn2, self.rotate_btn, self.delete_btn))
        self.move_btn2 = GUIButton(self.control_middleframe, text='Move', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', command=lambda: move(self.drag_manager, self.move_btn2, self.rotate_btn, self.delete_btn))

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.canvas_frame, width=1000, height=800, background="#383", highlightthickness=0)
        self.drag_manager = DragManager(self.canvas, self.grid_size)
        self.canvas.bind('<Configure>', lambda event: create_grid(self.canvas, self.grid_size))
        self.tag_generator = UniqueTagGenerator()

    def pack_widgets(self):
        self.left_frame.pack(side='left', padx=(20, 10))
        self.control_frame.pack()
        self.control_topframe.pack(fill='x')
        self.control_middleframe.pack(fill='x')
        self.control_bottomframe.pack(fill='x')
        self.canvas_frame.pack(side='right', padx=10, pady=10)

        self.add_desk_btn2.pack(side='left', padx=(10, 5), pady=5)
        self.add_student_btn2.pack(side='right', padx=(5, 10), pady=5)
        self.move_btn2.pack(side='top', fill='x', padx=10, pady=5)
        self.rotate_btn.pack(side='left', padx=(10, 5), pady=(5,10))
        self.delete_btn.pack(side='right', padx=(5, 10), pady=(5,10))
        
        self.canvas.pack()

    def rotate_command(self):
        rotate(self.drag_manager, self.move_btn2, self.rotate_btn, self.delete_btn)

    def create_grid(self):
        self.canvas.delete('grid_line')
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        for i in range(0, w, self.grid_size):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill='#3aa13a', width=0.5)
        for i in range(0, h, self.grid_size):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line', fill='#3aa13a', width=0.5)

    def add_desk(self):
        x1, y1 = 20, 20  
        width, height = 8 * self.grid_size, 4 * self.grid_size
        x2, y2 = x1 + width, y1 + height
        
        self.move_btn2.color = '#8d8d8d'
        self.move_btn2.hover_color = '#5a5a5a'
        self.drag_manager.move_mode = True
        # rotate_btn.state('!pressed')
        self.drag_manager.rotate_mode = False
        # delete_btn.state('!pressed')
        self.drag_manager.delete_mode = False

        tag = self.tag_generator.next_tag()
        rotation_tag = f"{tag}_rotation_0"

        item = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#662100", tags=(tag, rotation_tag))
        text = self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Desk', fill="#ffffff", tags=(tag, rotation_tag))
        
        self.drag_manager.add_draggable(tag)

    def add_student(self):
        x1, y1 = 20, 20  
        width, height = 4 * self.grid_size, 2 * self.grid_size
        x2, y2 = x1 + width, y1 + height

        self.move_btn2.color = '#8d8d8d'
        self.move_btn2.hover_color = '#5a5a5a'
        self.drag_manager.move_mode = True
        # rotate_btn.state('!pressed')
        self.drag_manager.rotate_mode = False
        # delete_btn.state('!pressed')
        self.drag_manager.delete_mode = False
        
        tag = self.tag_generator.next_tag()
        rotation_tag = f"{tag}_rotation_0"

        item = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#000066", outline="#0000ff", tags=(tag, rotation_tag))
        text = self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Student', fill="#ffffff", tags=(tag, rotation_tag))
        
        self.drag_manager.add_draggable(tag)

    def rotate(self):
        self.move_btn2.color = '#d3d3d3'
        self.move_btn2.hover_color = '#a0a0a0'
        self.drag_manager.move_mode = False
        # delete_btn.state('!pressed')
        self.drag_manager.delete_mode = False
        
        if self.drag_manager.rotate_mode == False:
            # rotate_btn.state('pressed')
            self.drag_manager.rotate_mode = True
        elif self.drag_manager.rotate_mode == True:
            # rotate_btn.state('!pressed')
            self.drag_manager.rotate_mode = False

    def delete(self):
        # move_btn.state('!pressed')
        self.drag_manager.move_mode = False
        # rotate_btn.state('!pressed')
        self.drag_manager.rotate_mode = False

        if self.drag_manager.delete_mode == False:
            self.delete_btn.state('!pressed')
            self.drag_manager.delete_mode = True
        elif self.drag_manager.delete_mode == True:
            self.delete_btn.state('!pressed')
            self.drag_manager.delete_mode = False

    def move(self):
        # rotate_btn.color('green')
        self.drag_manager.rotate_mode = False
        # delete_btn.color('green')
        self.drag_manager.delete_mode = False
        
        if self.drag_manager.move_mode == False:
            self.move_btn2.color = '#8d8d8d'
            self.move_btn2.hover_color = '#5a5a5a'
            self.drag_manager.move_mode = True
        elif self.drag_manager.move_mode == True:
            self.move_btn2.color = '#d3d3d3'
            self.move_btn2.hover_color = '#a0a0a0'
            self.drag_manager.move_mode = False