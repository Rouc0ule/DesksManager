import tkinter as tk

def create_grid(canvas, grid_size):
    canvas.delete('grid_line')
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    for i in range(0, w, grid_size):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill='#3aa13a', width=0.5)
    for i in range(0, h, grid_size):
        canvas.create_line([(0, i), (w, i)], tag='grid_line', fill='#3aa13a', width=0.5)

def add_desk(canvas, grid_size, tag_generator, drag_manager):
    x1, y1 = 20, 20  
    width, height = 8 * grid_size, 4 * grid_size
    x2, y2 = x1 + width, y1 + height
    
    tag = tag_generator.next_tag()

    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#662100", tags=tag)
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Desk', fill="#ffffff", tags=tag)
    
    drag_manager.add_draggable(tag)

def add_student(canvas, grid_size, tag_generator, drag_manager):
    x1, y1 = 20, 20  
    width, height = 4 * grid_size, 2 * grid_size
    x2, y2 = x1 + width, y1 + height
    
    tag = tag_generator.next_tag()

    item = canvas.create_rectangle(x1, y1, x2, y2, fill="#000066", outline="#0000ff", tags=tag)
    text = canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Student', fill="#ffffff", tags=tag)
    
    drag_manager.add_draggable(tag)

def delete(drag_manager, dlt_btn):
    if drag_manager.delete_mode == False:
        dlt_btn.config(relief=tk.SUNKEN)
        drag_manager.delete_mode = True
    elif drag_manager.delete_mode == True:
        dlt_btn.config(relief=tk.RAISED)
        drag_manager.delete_mode = False

def center_window(root):
    root.update_idletasks()
    width = 1300
    height = 820
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
