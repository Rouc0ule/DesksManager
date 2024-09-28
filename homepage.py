import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import ImageTk, Image
from dataManager import DataManager

class HomePage:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.data_manager = DataManager('Json/classes.json')
        self.load_images()
        self.setup_frames()
        self.setup_widgets()
        self.load_classes()

    def load_images(self):
        self.search_img = self.load_image("search")
        self.trash_img = self.load_image("delete")
        self.edit_img = self.load_image("edit")
        self.plus_img = self.load_image("plus_circle")

    def load_image(self, name):
        return ImageTk.PhotoImage(Image.open(f"Assets/{self.theme}_{name}.png").resize((25, 25)))

    def setup_frames(self):
        self.left_frame = self.create_frame(self.root, width=400)
        self.right_frame = self.create_frame(self.root, width=400)

    def create_frame(self, parent, width=None, **kwargs):
        frame = tk.Frame(parent, highlightbackground="lightgray", highlightthickness=1, **kwargs)
        if width:
            frame.config(width=width)
        return frame

    def setup_widgets(self):
        self.setup_searchbar()
        self.setup_scrollable_frame()
        self.setup_add_button()

    def setup_searchbar(self):
        self.searchbar_canvas = self.create_canvas(self.left_frame, height=70, width=380)
        self.create_searchbar_elements()
        self.bind_searchbar_events()

    def create_canvas(self, parent, **kwargs):
        return tk.Canvas(parent, highlightthickness=0, **kwargs)

    def create_searchbar_elements(self):
        self.searchbar_rect = self.rounded_rectangle(self.searchbar_canvas, 12, 12, 360, 50, fill='lightgray', tags='searchbar_rect')
        self.searchbar_entry = tk.Entry(font=("San Francisco", 15), width=25, relief=tk.FLAT, highlightthickness=0, bg='lightgray')
        self.searchbar_entry_window = self.searchbar_canvas.create_window(167, 37, window=self.searchbar_entry, tags='searchbar_entry')
        self.searchbar_btn = self.searchbar_canvas.create_image(342, 37, image=self.search_img, tags='searchbar_btn')

    def bind_searchbar_events(self):
        self.searchbar_canvas.bind('<Enter>', self.on_searchbar_hover)
        self.searchbar_canvas.bind('<Leave>', self.on_searchbar_leave)
        self.searchbar_canvas.bind('<Button-1>', self.on_searchbar_click)
        self.searchbar_entry.bind('<Enter>', self.on_searchbar_hover)
        self.searchbar_entry.bind('<Leave>', self.on_searchbar_leave)
        self.searchbar_entry.bind('<Button-1>', self.on_searchbar_click)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Enter>', self.on_searchbar_hover)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Leave>', self.on_searchbar_leave)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Button-1>', self.on_searchbar_click)

    def setup_scrollable_frame(self):
        self.scrollable_frame = tk.Frame(self.left_frame)
        self.scrollable_list_canvas = self.create_canvas(self.scrollable_frame, width=360, height=0)
        self.scrollable_list_frame = tk.Frame(self.scrollable_list_canvas)
        self.scrollable_list_frame_id = self.scrollable_list_canvas.create_window((0, 0), window=self.scrollable_list_frame, anchor="nw")
        self.scrollable_scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.scrollable_list_canvas.yview)
        self.scrollable_list_canvas.configure(yscrollcommand=self.scrollable_scrollbar.set)
        self.bind_scrollable_events()

    def bind_scrollable_events(self):
        self.scrollable_list_frame.bind('<Configure>', self.configure_interior)
        self.scrollable_list_canvas.bind('<Configure>', self.configure_canvas)
        self.scrollable_list_frame.bind("<Configure>", self.on_frame_configure)
        self.scrollable_list_canvas.bind('<Configure>', self.on_canvas_configure)
        self.scrollable_list_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_list_frame.bind("<MouseWheel>", self.on_mousewheel)

    def setup_add_button(self):
        self.add_btn_canvas = self.create_canvas(self.left_frame, height=80, width=380)
        self.create_add_button()

    def load_classes(self):
        classes = self.data_manager.load_classes()
        for classe in classes:
            self.add_class(classe['name'], len(classe.get('students_list', [])))

    def pack_widgets(self):
        self.left_frame.pack(fill='y', side='left')
        self.right_frame.pack(fill='both', expand=True, side='right')
        self.searchbar_canvas.pack(fill='x')
        self.scrollable_frame.pack(fill='both', expand=True)
        self.scrollable_list_canvas.pack(side='left', fill='both', expand=True)
        self.scrollable_scrollbar.pack(side='right', fill='y')
        self.add_btn_canvas.pack(fill='x')

    def rounded_rectangle(self, canvas, x, y, width, height, r=25, **kwargs):
        points = [
            x+r, y, x+r, y, x+width-r, y, x+width-r, y, x+width, y, x+width, y+r, x+width, y+r,
            x+width, y+height-r, x+width, y+height-r, x+width, y+height, x+width-r, y+height,
            x+width-r, y+height, x+r, y+height, x+r, y+height, x, y+height, x, y+height-r,
            x, y+height-r, x, y+r, x, y+r, x, y
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def add_class(self, classe, nb_students):
        frame = tk.Frame(self.scrollable_list_frame, width=360, height=100)
        frame.pack()
        frame.pack_propagate(False)
        canvas = self.create_canvas(frame, width=360, height=100)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.create_class_elements(canvas, classe, nb_students)
        self.bind_class_events(canvas, classe)
        return frame

    def create_class_elements(self, canvas, classe, nb_students):
        original_dims = (14, 12, 340, 80)
        self.rounded_rectangle(canvas, *original_dims, fill='lightgray', tags='class_rect')
        canvas.create_text(25, 40, text=classe, font=("San Francisco", 20, 'bold'), anchor='w', tags='class_text')
        canvas.create_text(25, 70, text=f"{nb_students} élèves", font=("San Francisco", 12), anchor='w', tags='class_text')
        canvas.create_image(332, 70, image=self.trash_img, tags='trash_btn')
        canvas.original_dims = original_dims

    def bind_class_events(self, canvas, classe):
        canvas.tag_bind('trash_btn', '<Enter>', lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind('trash_btn', '<Leave>', lambda e: canvas.config(cursor=""))
        canvas.tag_bind('trash_btn', '<Button-1>', lambda e: self.on_trash_click(classe))
        canvas.tag_bind('class_rect', '<Enter>', lambda e: self.on_class_hover(e, canvas))
        canvas.tag_bind('class_rect', '<Leave>', lambda e: self.on_class_leave(e, canvas))
        canvas.tag_bind('class_text', '<Enter>', lambda e: self.on_class_hover(e, canvas))
        canvas.tag_bind('class_text', '<Leave>', lambda e: self.on_class_leave(e, canvas))
        canvas.bind("<MouseWheel>", self.on_mousewheel)
        canvas.tag_bind('class_rect', '<Button-1>', lambda e, c=classe: self.display_class_details(c))
        canvas.tag_bind('class_text', '<Button-1>', lambda e, c=classe: self.display_class_details(c))

    def create_add_button(self):
        self.create_circle(self.add_btn_canvas, 40, 40, 25, fill='lightgray', outline='', tags='add_btn_circle')
        self.add_btn_canvas.create_text(40, 40, text='+', font=('San Francisco', 30), tags='add_btn_text')
        self.add_btn_canvas.addtag_withtag('add_btn', 'add_btn_circle')
        self.add_btn_canvas.addtag_withtag('add_btn', 'add_btn_text')
        self.add_btn_canvas.tag_bind('add_btn', '<Enter>', self.on_add_btn_hover)
        self.add_btn_canvas.tag_bind('add_btn', '<Leave>', self.on_add_btn_leave)
        self.add_btn_canvas.tag_bind('add_btn', '<Button-1>', self.add_new_class)

    def create_circle(self, canvas, x, y, r, **kwargs):
        return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def configure_interior(self, event=None):
        size = (self.scrollable_list_frame.winfo_reqwidth(), self.scrollable_list_frame.winfo_reqheight())
        self.scrollable_list_canvas.config(scrollregion="0 0 %s %s" % size)
        if self.scrollable_list_frame.winfo_reqwidth() != self.scrollable_list_canvas.winfo_width():
            self.scrollable_list_canvas.config(width=self.scrollable_list_frame.winfo_reqwidth())

    def configure_canvas(self, event=None):
        if self.scrollable_list_frame.winfo_reqwidth() != self.scrollable_list_canvas.winfo_width():
            self.scrollable_list_canvas.itemconfigure(self.scrollable_list_frame_id, width=self.scrollable_list_canvas.winfo_width())

    def on_frame_configure(self, event=None):
        self.scrollable_list_canvas.configure(scrollregion=self.scrollable_list_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        width = event.width
        self.scrollable_list_canvas.itemconfig(self.scrollable_list_frame_id, width=width)

    def on_class_hover(self, event, canvas):
        if not hasattr(canvas, 'is_hovering') or not canvas.is_hovering:
            canvas.is_hovering = True
            x, y, width, height = canvas.original_dims
            grow = 5
            new_dims = (x-grow, y-grow, width+2*grow, height+2*grow)
            canvas.delete('class_rect')
            self.rounded_rectangle(canvas, *new_dims, fill='#a0a0a0', tags='class_rect')
            canvas.config(cursor="hand2")
            canvas.tag_raise('class_text')
            canvas.tag_raise('trash_btn')

    def on_class_leave(self, event, canvas):
        if hasattr(canvas, 'is_hovering') and canvas.is_hovering:
            canvas.is_hovering = False
            canvas.delete('class_rect')
            self.rounded_rectangle(canvas, *canvas.original_dims, fill='lightgray', tags='class_rect')
            canvas.config(cursor="")
            canvas.tag_raise('class_text')
            canvas.tag_raise('trash_btn')

    def on_searchbar_hover(self, event):
        self.searchbar_canvas.itemconfig('searchbar_rect', fill='#a0a0a0')
        self.searchbar_entry.config(bg='#a0a0a0')
        self.searchbar_canvas.itemconfig('searchbar_btn', image=self.search_img)
        self.searchbar_canvas.config(cursor="xterm")

    def on_searchbar_leave(self, event):
        x, y = self.searchbar_canvas.winfo_pointerxy()
        widget_under_cursor = self.searchbar_canvas.winfo_containing(x, y)
        if widget_under_cursor in [self.searchbar_canvas, self.searchbar_entry]:
            return
        self.searchbar_canvas.itemconfig('searchbar_rect', fill='lightgray')
        self.searchbar_entry.config(bg='lightgray')
        self.searchbar_canvas.itemconfig('searchbar_btn', image=self.search_img)
        self.searchbar_canvas.config(cursor="")

    def on_searchbar_click(self, event):
        if event.widget == self.searchbar_entry:
            self.searchbar_entry.focus_set()
        elif 'searchbar_btn' in self.searchbar_canvas.gettags('current'):
            print("Search button clicked!")
        self.on_searchbar_hover(event)

    def on_mousewheel(self, event):
        self.scrollable_list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_add_btn_hover(self, event):
        self.add_btn_canvas.itemconfig('add_btn_circle', fill='#a0a0a0')
        self.add_btn_canvas.itemconfig('add_btn_text', fill='black')
        self.add_btn_canvas.config(cursor="hand2")

    def on_add_btn_leave(self, event):
        self.add_btn_canvas.itemconfig('add_btn_circle', fill='lightgray')
        self.add_btn_canvas.itemconfig('add_btn_text', fill='black')
        self.add_btn_canvas.config(cursor="")

    def add_new_class(self, event):
        classes = self.data_manager.load_classes()
        new_class_number = len(classes) + 1
        new_class_name = f"Nouvelle classe {new_class_number}"
        new_class = {"name": new_class_name, "students_list": []}
        self.data_manager.add_class(new_class)
        self.add_class(new_class_name, 0)
        self.display_class_details(new_class_name)

    def on_trash_click(self, classe):
        print(f"Suppression de la classe {classe}")
        self.data_manager.remove_class(classe)
        
        for widget in self.scrollable_list_frame.winfo_children():
            canvas = widget.winfo_children()[0]
            if canvas.type('class_text') == 'text':
                text_item = canvas.find_withtag('class_text')[0]
                if canvas.itemcget(text_item, 'text') == classe:
                    widget.destroy()
                    break
        
        self.configure_interior()
        self.on_frame_configure()

    def display_class_details(self, classe):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        class_details = self.data_manager.get_class_details(classe)

        if class_details:
            details_frame = self.create_frame(self.right_frame)
            students_frame = self.create_frame(self.right_frame)

            details_frame.pack(side='left', fill='both', expand=True)
            students_frame.pack(side='right', fill='both', expand=True)
            
            self.details_canvas = self.create_canvas(details_frame)
            self.details_canvas.pack(fill='both')

            self.details_canvas.create_image(30, 50, image=self.edit_img, tag='edit_btn')
            self.class_name_text = self.details_canvas.create_text(50, 50, text='Classe : ' + class_details.get('name', ''), font=("San Francisco", 20, 'bold'), anchor='w')
            self.details_canvas.create_text(50, 80, text=('{} élèves'.format(len(class_details.get('students_list', [])))), font=("San Francisco", 17, 'italic'), anchor='w')

            self.details_canvas.tag_bind('edit_btn', '<Enter>', lambda e: self.details_canvas.config(cursor="hand2"))
            self.details_canvas.tag_bind('edit_btn', '<Leave>', lambda e: self.details_canvas.config(cursor=""))
            self.details_canvas.tag_bind('edit_btn', '<Button-1>', lambda e: self.edit_class_name(classe))

            self.create_student_list(students_frame, class_details)

            self.create_rounded_button(students_frame, 0, 0, 150, 40, text='Button', icon=self.plus_img, padx=5, pady=5)

        else:
            tk.Label(self.right_frame, text="Aucun détail disponible pour cette classe", 
                    font=("San Francisco", 14)).pack()

    def edit_class_name(self, classe):
        current_name = self.data_manager.get_class_details(classe)['name']
        entry = tk.Entry(self.details_canvas, font=("San Francisco", 20, 'bold'))
        entry.insert(0, current_name)
        entry_window = self.details_canvas.create_window(50, 50, window=entry, anchor='w')
        
        def save_new_name(event):
            new_name = entry.get()
            if new_name and new_name != current_name:
                self.data_manager.update_class_name(classe, new_name)
                self.details_canvas.itemconfig(self.class_name_text, text='Classe : ' + new_name)
                self.update_class_list()
            self.details_canvas.delete(entry_window)
            self.details_canvas.itemconfig(self.class_name_text, state='normal')

        entry.bind('<Return>', save_new_name)
        entry.bind('<FocusOut>', save_new_name)
        entry.focus_set()
        self.details_canvas.itemconfig(self.class_name_text, state='hidden')

    def update_class_list(self):
        for widget in self.scrollable_list_frame.winfo_children():
            widget.destroy()
        self.load_classes()

    def create_student_list(self, parent_frame, class_details):
        student_scrollable_frame = tk.Frame(parent_frame)
        student_scrollable_frame.pack(fill='both', expand=True)

        student_canvas = self.create_canvas(student_scrollable_frame, width=360, height=0)
        student_scrollbar = tk.Scrollbar(student_scrollable_frame, orient="vertical", command=student_canvas.yview)

        student_inner_frame = tk.Frame(student_canvas)

        student_canvas.configure(yscrollcommand=student_scrollbar.set)
        student_canvas.create_window((0, 0), window=student_inner_frame, anchor="nw")

        for student in class_details.get('students_list', []):
            self.add_student_to_list(student_inner_frame, student)

        student_inner_frame.bind("<Configure>", lambda e: student_canvas.configure(scrollregion=student_canvas.bbox("all")))

        student_canvas.pack(side="left", fill="y", expand=True)
        student_scrollbar.pack(side="right", fill="y")

    def add_student_to_list(self, parent_frame, student):
        student_frame = tk.Frame(parent_frame, width=360, height=75)
        student_frame.pack()
        student_frame.pack_propagate(False)

        canvas = self.create_canvas(student_frame, width=360, height=75)
        canvas.pack(fill=tk.BOTH, expand=True)

        original_dims = (5, 5, 350, 65)
        self.rounded_rectangle(canvas, *original_dims, fill='lightgray', tags='student_rect')

        canvas.create_text(25, 37, text=f"{student['firstname']} {student['lastname']}", 
                        font=("San Francisco", 16), anchor='w', tags='student_text')
        canvas.create_image(335, 50, image=self.trash_img, tags='trash_btn')

        canvas.original_dims = original_dims

        self.bind_student_events(canvas, student)

    def bind_student_events(self, canvas, student):
        canvas.tag_bind('trash_btn', '<Enter>', lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind('trash_btn', '<Leave>', lambda e: canvas.config(cursor=""))
        canvas.tag_bind('trash_btn', '<Button-1>', lambda e: self.remove_student(student))

        canvas.tag_bind('student_rect', '<Enter>', lambda e: self.on_student_hover(e, canvas))
        canvas.tag_bind('student_rect', '<Leave>', lambda e: self.on_student_leave(e, canvas))
        canvas.tag_bind('student_text', '<Enter>', lambda e: self.on_student_hover(e, canvas))
        canvas.tag_bind('student_text', '<Leave>', lambda e: self.on_student_leave(e, canvas))

    def on_student_hover(self, event, canvas):
        if not hasattr(canvas, 'is_hovering') or not canvas.is_hovering:
            canvas.is_hovering = True
            canvas.delete('student_rect')
            self.rounded_rectangle(canvas, 0, 0, 360, 75, fill='#a0a0a0', tags='student_rect')
            canvas.config(cursor="hand2")
            canvas.tag_raise('student_text')
            canvas.tag_raise('trash_btn')

    def on_student_leave(self, event, canvas):
        if hasattr(canvas, 'is_hovering') and canvas.is_hovering:
            canvas.is_hovering = False
            canvas.delete('student_rect')
            self.rounded_rectangle(canvas, 5, 5, 350, 65, fill='lightgray', tags='student_rect')
            canvas.config(cursor="")
            canvas.tag_raise('student_text')
            canvas.tag_raise('trash_btn')

    def on_student_trash_click(self, student):
        # Implement student deletion logic here
        pass

    def add_student(self, classe):
        firstname = simpledialog.askstring("Nouvel élève", "Prénom de l'élève:")
        if firstname:
            lastname = simpledialog.askstring("Nouvel élève", "Nom de l'élève:")
            if lastname:
                new_student = {"firstname": firstname, "lastname": lastname}
                self.data_manager.add_student(classe, new_student)
                self.display_class_details(classe)

    def remove_student(self, classe, student):
        if messagebox.askyesno("Supprimer l'élève", f"Voulez-vous vraiment supprimer {student['firstname']} {student['lastname']} ?"):
            self.data_manager.remove_student(classe, f"{student['firstname']} {student['lastname']}")
            self.display_class_details(classe)

    def create_rounded_button(self, parent, x, y, width, height, text, icon, padx=0, pady=0, command=None):
        canvas = self.create_canvas(parent, width=width, height=height)
        canvas.pack(padx=padx, pady=pady)
        self.rounded_rectangle(canvas, x, y, x + width, y + height, r=30, fill='lightgray', tags='capsule')
        canvas.create_image(x + height // 2, y + height // 2, image=icon)
        canvas.create_text(x + height + 10, y + height // 2, text=text, font=('San Francisco', 14), anchor='w')
        
        canvas.tag_bind('capsule', '<Enter>', lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind('capsule', '<Leave>', lambda e: canvas.config(cursor=""))
        canvas.tag_bind('capsule', '<Button-1>', command)
        
        return canvas