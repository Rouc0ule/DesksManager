import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from ClassRoomPage.dragManager import DragManager
from ClassRoomPage.uniqueTagGenerator import UniqueTagGenerator
from RTkinter.widgets.RTkButton import RTkButton
from themeManager import ThemeManager

class ClassroomPage:
    def __init__(self, root, theme, grid_size):
        self.root = root
        self.theme_manager = ThemeManager()
        self.theme = self.theme_manager.set_current_theme(theme)
        root.configure(bg=self.theme_manager.get_color("background"))
        self.grid_size = grid_size
        self.load_images()
        self.setup_frames()
        self.setup_canvas()
        self.setup_widgets()
        self.pack_widgets()
        self.drag_manager.move_mode = True
        self.move()
        
    def load_images(self):
        self.plus_rectangle_img = self.load_image('plus_rectangle')
        self.person_badge_plus_fill_img = self.load_image('person_badge_plus_fill', size=(20,20))
        self.delete_img = self.load_image('delete')
        self.rotate_left_img = self.load_image('rotate_left')
        self.move_img = self.load_image('move')
        self.plus_circle_img = self.load_image('plus_circle')
        print(self.plus_rectangle_img)

    def load_image(self, name, size=(25, 25)):
        return ImageTk.PhotoImage(Image.open(f"Assets/{self.theme}_{name}.png").resize(size))

    def setup_frames(self):
        self.bottom_frame = tk.Frame(self.root, bg=self.theme_manager.get_color("frame_bg"))
        # self.control_frame = tk.LabelFrame(self.bottom_frame, text='Commands', width=400)
        # self.control_topframe = tk.Frame(self.control_frame)
        # self.control_middleframe = tk.Frame(self.control_frame)
        # self.control_bottomframe = tk.Frame(self.control_frame)
        self.canvas_frame = tk.Frame(self.root)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.canvas_frame, width=1300, height=800, background="#383", highlightthickness=0)
        self.drag_manager = DragManager(self.canvas, self.grid_size)
        self.canvas.bind('<Configure>', lambda event: self.create_grid())
        self.tag_generator = UniqueTagGenerator()

    def setup_widgets(self):
        self.add_student_btn = RTkButton(self.bottom_frame, width=35, radius=20, text='', font=('San Francisco', 10), color='#d3d3d3', hover_color='#a0a0a0', image=self.person_badge_plus_fill_img, compound='left', command=self.add_student)
        self.add_desk_btn = RTkButton(self.bottom_frame, width=35, radius=20, text='', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', image=self.plus_rectangle_img, compound='left', command=self.add_desk)
        self.move_btn = RTkButton(self.bottom_frame, radius=20, text='Move', font=('San Francisco', 10), text_color='#000000', color='#d3d3d3', hover_color='#a0a0a0', image=None, command=self.move)
        self.rotate_btn = RTkButton(self.bottom_frame, radius=20, text='Rotate', font=('San Francisco', 10), text_color=self.theme_manager.get_color("button_fg"), color=self.theme_manager.get_color("button_bg"), hover_color=self.theme_manager.get_color("button_hover"), image=None, command=self.rotate)
        self.delete_btn = RTkButton(self.bottom_frame, radius=20, text='Delete', font=('San Francisco', 10), text_color=self.theme_manager.get_color("button_fg"), color=self.theme_manager.get_color("button_bg"), hover_color=self.theme_manager.get_color("button_hover"), image=None, command=self.delete)
        self.var = tk.DoubleVar()
        self.slider = tk.Scale(self.bottom_frame, from_=10, to=200, resolution=5, orient=tk.HORIZONTAL, variable = self.var, command=self.scale_grid)

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
        self.slider.pack()
        
        self.canvas.pack()

    def create_grid(self):
        self.canvas.delete('grid_line')
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i in range(0, w, self.grid_size):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill='#3aa13a', width=0.5)
        for i in range(0, h, self.grid_size):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line', fill='#3aa13a', width=0.5)
        self.canvas.tag_lower('grid_line')

    def resize_canvas_items(self, old_grid_size, new_grid_size):
        scale_factor = new_grid_size / old_grid_size
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if 'desk' in tags or 'student' in tags:
                x1, y1, x2, y2 = self.canvas.coords(item)
                new_coords = [
                    round(x1 * scale_factor / new_grid_size) * new_grid_size,
                    round(y1 * scale_factor / new_grid_size) * new_grid_size,
                    round(x2 * scale_factor / new_grid_size) * new_grid_size,
                    round(y2 * scale_factor / new_grid_size) * new_grid_size
                ]
                self.canvas.coords(item, *new_coords)
            elif 'text' in tags:
                x, y = self.canvas.coords(item)
                new_coords = [
                    round(x * scale_factor / new_grid_size) * new_grid_size,
                    round(y * scale_factor / new_grid_size) * new_grid_size
                ]
                self.canvas.coords(item, *new_coords)
                current_font = self.canvas.itemcget(item, 'font')
                if current_font:
                    try:
                        font = tk.font.Font(font=current_font)
                        new_size = int(font.cget('size') * scale_factor)
                        new_font = font.copy()
                        new_font.configure(size=new_size)
                        self.canvas.itemconfig(item, font=new_font)
                    except tk.TclError:
                        pass

        self.drag_manager.update_grid_size(new_grid_size)
        self.create_grid()

    def add_desk(self):
        x1, y1 = 20, 20
        width, height = 8 * self.grid_size, 4 * self.grid_size
        x2, y2 = x1 + width, y1 + height
        
        self.set_modes(True, False, False)
        
        tag = self.tag_generator.next_tag()
        rotation_tag = f"{tag}_rotation_0"

        item = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#662100", tags=(tag, rotation_tag, 'desk'))
        text = self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Desk', fill="#ffffff", tags=(tag, rotation_tag, 'text'))
        
        self.drag_manager.add_draggable(tag)

    def add_student(self):
        x1, y1 = 20, 20
        width, height = 4 * self.grid_size, 2 * self.grid_size
        x2, y2 = x1 + width, y1 + height

        self.set_modes(True, False, False)
        
        tag = self.tag_generator.next_tag()
        rotation_tag = f"{tag}_rotation_0"

        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#000066", outline="#0000ff", tags=(tag, rotation_tag, 'student'))
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Student', fill="#ffffff", tags=(tag, rotation_tag, 'text'), font=('San Francisco', int(self.grid_size/3)))
        
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
            self.move_btn.color = self.theme_manager.get_color("button_bg")
            self.move_btn.hover_color = self.theme_manager.get_color("button_hover")

        if is_rotate_mode:
            self.rotate_btn.color = '#8d8d8d'
            self.rotate_btn.hover_color = '#5a5a5a'
        else:
            self.rotate_btn.color = self.theme_manager.get_color("button_bg")
            self.rotate_btn.hover_color = self.theme_manager.get_color("button_hover")

        if is_delete_mode:
            self.delete_btn.color = '#8d8d8d'
            self.delete_btn.hover_color = '#5a5a5a'
        else:
            self.delete_btn.color = self.theme_manager.get_color("button_bg")
            self.delete_btn.hover_color = self.theme_manager.get_color("button_hover")
        
        self.move_btn.update_button_size()
        self.rotate_btn.update_button_size()
        self.delete_btn.update_button_size()

    def scale_grid(self, value):
        old_grid_size = self.grid_size
        self.grid_size = int(value)
        self.resize_canvas_items(old_grid_size, self.grid_size)