import tkinter as tk
from PIL import ImageTk, Image
from dragManager import DragManager
from uniqueTagGenerator import UniqueTagGenerator
from functions import create_grid, add_desk, add_student, move, rotate, delete, center_window
#import pywinstyles

# def size():
#     print('Size : {} x {}'.format(root.winfo_width(), root.winfo_height()))

root = tk.Tk()
root.title('DesksManager')
root.resizable(False, False)
center_window(root, 1300, 820)
#pywinstyles.apply_style(root, "acrylic")

theme = 'light'
grid_size = 20
number_of_items = 0

add_desk_img = ImageTk.PhotoImage(Image.open("Assets/{}_plus_rectangle.png".format(theme)).resize((25,25)))
add_student_img = ImageTk.PhotoImage(Image.open("Assets/{}_person_badge_plus_fill.png".format(theme)).resize((25,25)))
delete_img = ImageTk.PhotoImage(Image.open("Assets/{}_delete.png".format(theme)).resize((25,25)))
rotate_img = ImageTk.PhotoImage(Image.open("Assets/{}_rotate_left.png".format(theme)).resize((25,25)))
move_img = ImageTk.PhotoImage(Image.open("Assets/{}_move.png".format(theme)).resize((25,25)))

control_frame = tk.LabelFrame(root, text='Commands', width=400)
control_frame.pack(side='left', padx=(20, 10))

add_desk_btn = tk.Button(control_frame, text='Add desk', font=("San Francisco", 9, 'bold'), image=add_desk_img, compound='left', width=100, command=lambda: add_desk(canvas, grid_size, tag_generator, drag_manager, move_btn, rotate_btn, delete_btn))
add_desk_btn.grid(row=0, column=0, padx=(10, 5), pady=5)

add_student_btn = tk.Button(control_frame, text='Add student', font=("San Francisco", 9, 'bold'), image=add_student_img, compound='left', width=100, command=lambda: add_student(canvas, grid_size, tag_generator, drag_manager, move_btn, rotate_btn, delete_btn))
add_student_btn.grid(row=0, column=1, padx=(5, 10), pady=5)

move_btn = tk.Button(control_frame, text='Move', font=("San Francisco", 9, 'bold'), image=move_img, compound='left', width=218, command=lambda: move(drag_manager, move_btn, rotate_btn, delete_btn))
move_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

rotate_btn = tk.Button(control_frame, text='Rotate', font=("San Francisco", 9, 'bold'), image=rotate_img, compound='left', width=100, command=lambda: rotate(drag_manager, move_btn, rotate_btn, delete_btn))
rotate_btn.grid(row=2, column=0, padx=(10, 5), pady=(5,10))

delete_btn = tk.Button(control_frame, text='Delete', font=("San Francisco", 9, 'bold'), image=delete_img, compound='left', width=100, command=lambda: delete(drag_manager, move_btn, rotate_btn, delete_btn))
delete_btn.grid(row=2, column=1, padx=(5, 10), pady=(5,10))

# size_btn = tk.Button(control_frame, text='Size', font=("San Francisco", 9, 'bold'), command=size)
# size_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

canvas_frame = tk.Frame(root)
canvas_frame.pack(side='right', padx=10, pady=10)

canvas = tk.Canvas(canvas_frame, width=1000, height=800, background="#383", highlightthickness=0)
canvas.pack()

drag_manager = DragManager(canvas, grid_size)

canvas.bind('<Configure>', lambda event: create_grid(canvas, grid_size))
tag_generator = UniqueTagGenerator()

root.mainloop()