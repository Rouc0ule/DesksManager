import tkinter as tk

plan_root = tk.Tk()
plan_root.title('Plan')
plan_root.geometry('600x400+100+100')

commands_root = tk.Tk()
commands_root.title('Commands')
commands_root.geometry('250x400+700+100')

commands_frame = tk.Frame(commands_root)
commands_frame.pack(padx=20,pady=20)

add_desk_btn = tk.Button(commands_frame, text='Add Desk')
add_desk_btn.grid(column=0, row=0, padx=5, pady=5)
add_student_btn = tk.Button(commands_frame, text='Add Student')
add_student_btn.grid(column=0, row=1, padx=5, pady=5)

plan_root.mainloop()
commands_root.mainloop()