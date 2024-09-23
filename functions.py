import tkinter as tk
from jsonloader import JsonManager

def create_grid(canvas, grid_size):
    canvas.delete('grid_line')
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    for i in range(0, w, grid_size):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill='#3aa13a', width=0.5)
    for i in range(0, h, grid_size):
        canvas.create_line([(0, i), (w, i)], tag='grid_line', fill='#3aa13a', width=0.5)

def add_desk(canvas, grid_size, tag_generator, drag_manager, move_btn, rotate_btn, delete_btn):
    x1, y1 = 20, 20  
    width, height = 8 * grid_size, 4 * grid_size
    x2, y2 = x1 + width, y1 + height
    
    move_btn.state(['pressed'])
    drag_manager.move_mode = True
    rotate_btn.state(['!pressed'])
    drag_manager.rotate_mode = False
    delete_btn.state(['!pressed'])
    drag_manager.delete_mode = False

    tag = tag_generator.next_tag()
    rotation_tag = f"{tag}_rotation_0"

    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#662100", tags=(tag, rotation_tag))
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Desk', fill="#ffffff", tags=(tag, rotation_tag))
    
    drag_manager.add_draggable(tag)

def add_student(canvas, grid_size, tag_generator, drag_manager, move_btn, rotate_btn, delete_btn):
    x1, y1 = 20, 20  
    width, height = 4 * grid_size, 2 * grid_size
    x2, y2 = x1 + width, y1 + height

    move_btn.state(['pressed'])
    drag_manager.move_mode = True
    rotate_btn.state(['!pressed'])
    drag_manager.rotate_mode = False
    delete_btn.state(['!pressed'])
    drag_manager.delete_mode = False
    
    tag = tag_generator.next_tag()
    rotation_tag = f"{tag}_rotation_0"

    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#000066", outline="#0000ff", tags=(tag, rotation_tag))
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Student', fill="#ffffff", tags=(tag, rotation_tag))
    
    drag_manager.add_draggable(tag)

def rotate(drag_manager, move_btn, rotate_btn, delete_btn):
    move_btn.state(['!pressed'])
    drag_manager.move_mode = False
    delete_btn.state(['!pressed'])
    drag_manager.delete_mode = False
    
    if drag_manager.rotate_mode == False:
        rotate_btn.state(['pressed'])
        drag_manager.rotate_mode = True
    elif drag_manager.rotate_mode == True:
        rotate_btn.state(['!pressed'])
        drag_manager.rotate_mode = False

def delete(drag_manager, move_btn, rotate_btn, delete_btn):
    move_btn.state(['!pressed'])
    drag_manager.move_mode = False
    rotate_btn.state(['!pressed'])
    drag_manager.rotate_mode = False

    if drag_manager.delete_mode == False:
        delete_btn.state(['pressed'])
        drag_manager.delete_mode = True
    elif drag_manager.delete_mode == True:
        delete_btn.state(['!pressed'])
        drag_manager.delete_mode = False

def move(drag_manager, move_btn, rotate_btn, delete_btn):
    rotate_btn.state(['!pressed'])
    drag_manager.rotate_mode = False
    delete_btn.state(['!pressed'])
    drag_manager.delete_mode = False
    
    if drag_manager.move_mode == False:
        move_btn.state(['pressed'])
        drag_manager.move_mode = True
    elif drag_manager.move_mode == True:
        move_btn.state(['!pressed'])
        drag_manager.move_mode = False

def add_to_student_list(student_list_lastname_entry, student_list_firstname_entry, student_list_box):
    lastname = student_list_lastname_entry.get().strip().upper()
    firstname = student_list_firstname_entry.get().strip()
    
    if not lastname or not firstname:
        print("Nom ou prénom manquant")
        return
    
    text = f"{lastname}, {firstname}"
    student_list_box.insert(tk.END, text)
    
    print(f"Tentative d'ajout de l'étudiant : {lastname} {firstname}")
    
    json_manager = JsonManager()
    try:
        json_manager.add_student("4e2", lastname, firstname)
        print("Étudiant ajouté avec succès")
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'étudiant : {e}")
    
    student_list_lastname_entry.delete(0, tk.END)
    student_list_firstname_entry.delete(0, tk.END)

def center_window(root, width, height):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
