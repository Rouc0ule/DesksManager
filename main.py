import tkinter as tk
from PIL import ImageTk, Image
from dragManager import DragManager
from uniqueTagGenerator import UniqueTagGenerator
from jsonloader import JsonManager
from functions import create_grid, add_desk, add_student, move, rotate, delete, add_to_student_list, center_window
#import pywinstyles

def size():
    print('Size : {} x {}'.format(root.winfo_width(), root.winfo_height()))


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
plus_img = ImageTk.PhotoImage(Image.open("Assets/{}_plus_circle.png".format(theme)).resize((25,25)))

left_frame = tk.Frame(root)
left_frame.pack(side='left', padx=(20, 10))

control_frame = tk.LabelFrame(left_frame, text='Commands', width=400)
control_frame.pack()

add_desk_btn = tk.Button(control_frame, text='Add desk', font=("San Francisco", 9, 'bold'), image=add_desk_img, compound='left', relief=tk.RIDGE, width=100, height=25, command=lambda: add_desk(canvas, grid_size, tag_generator, drag_manager, move_btn, rotate_btn, delete_btn))
add_desk_btn.grid(row=0, column=0, padx=(10, 5), pady=5)

add_student_btn = tk.Button(control_frame, text='Add student', font=("San Francisco", 9, 'bold'), image=add_student_img, compound='left', relief=tk.RIDGE, width=100, height=25, command=lambda: add_student(canvas, grid_size, tag_generator, drag_manager, move_btn, rotate_btn, delete_btn))
add_student_btn.grid(row=0, column=1, padx=(5, 10), pady=5)

move_btn = tk.Button(control_frame, text='Move', font=("San Francisco", 9, 'bold'), image=move_img, compound='left', relief=tk.RIDGE, width=218, height=25, command=lambda: move(drag_manager, move_btn, rotate_btn, delete_btn))
move_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

rotate_btn = tk.Button(control_frame, text='Rotate', font=("San Francisco", 9, 'bold'), image=rotate_img, compound='left', relief=tk.RIDGE, width=100, height=25, command=lambda: rotate(drag_manager, move_btn, rotate_btn, delete_btn))
rotate_btn.grid(row=2, column=0, padx=(10, 5), pady=(5,10))

delete_btn = tk.Button(control_frame, text='Delete', font=("San Francisco", 9, 'bold'), image=delete_img, compound='left', relief=tk.RIDGE, width=100, height=25, command=lambda: delete(drag_manager, move_btn, rotate_btn, delete_btn))
delete_btn.grid(row=2, column=1, padx=(5, 10), pady=(5,10))

# size_btn = tk.Button(control_frame, text='Size', font=("San Francisco", 9, 'bold'), command=size)
# size_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

student_list_frame = tk.LabelFrame(left_frame, text='List')
student_list_frame.pack()

student_list_lastname_entry = tk.Entry(student_list_frame, font=("San Francisco", 9), relief=tk.RIDGE, width=31)
student_list_lastname_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5, ipady=4)

student_list_firstname_entry = tk.Entry(student_list_frame, font=("San Francisco", 9), relief=tk.RIDGE, width=31)
student_list_firstname_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, ipady=4)

add_to_student_list_btn = tk.Button(student_list_frame, text='Add to list', font=("San Francisco", 9, 'bold'), image=plus_img, compound='left', relief=tk.RIDGE, width=218, height=25, command=lambda: add_to_student_list(student_list_lastname_entry, student_list_firstname_entry, student_list_box))
add_to_student_list_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# s

student_list_box_frame = tk.Frame(student_list_frame)
student_list_box_frame.grid(row=4, pady=(5, 10))

student_list_box = tk.Listbox(student_list_box_frame, height=20, width=34)
student_list_box.pack(side='left', fill='y', padx=(7,0))

student_list_scrollbar = tk.Scrollbar(student_list_box_frame, orient='vertical')
student_list_scrollbar.pack(side='right', fill='y')

student_list_box.config(yscrollcommand=student_list_scrollbar.set)
student_list_scrollbar.config(command=student_list_box.yview)

canvas_frame = tk.Frame(root)
canvas_frame.pack(side='right', padx=10, pady=10)

canvas = tk.Canvas(canvas_frame, width=1000, height=800, background="#383", highlightthickness=0)
canvas.pack()

drag_manager = DragManager(canvas, grid_size)

canvas.bind('<Configure>', lambda event: create_grid(canvas, grid_size))
tag_generator = UniqueTagGenerator()

root.mainloop()