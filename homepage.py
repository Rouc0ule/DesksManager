import tkinter as tk
from tkinter import simpledialog
from PIL import ImageTk, Image
from dataManager import DataManager

class homePage:
    def __init__(self, root, theme):
        self.root = root

        self.data_manager = DataManager('Json/classes.json')

        self.search_img = ImageTk.PhotoImage(Image.open("Assets/{}_search.png".format(theme)).resize((25,25)))
        self.trash_img = ImageTk.PhotoImage(Image.open("Assets/{}_delete.png".format(theme)).resize((25,25)))

        # WIDGETS

        self.leftframe = tk.Frame(self.root, width=400, highlightbackground="lightgray", highlightthickness=1)
        self.rightframe = tk.Frame(self.root, width=400, highlightbackground="lightgray", highlightthickness=1)

        # Canvas Searchbar

        self.searchbar_canvas = tk.Canvas(self.leftframe, height=70, width=380, highlightthickness=0)
        self.searchbar_rect = self.rounded_rectangle(self.searchbar_canvas, 12, 12, 360, 50, fill='lightgray', tags='searchbar_rect')
        self.searchbar_entry = tk.Entry(font=("San Francisco", 15), width=25, relief=tk.FLAT, highlightthickness=0, bg='lightgray')
        self.searchbar_entry_window = self.searchbar_canvas.create_window(167, 37, window=self.searchbar_entry, tags='searchbar_entry')
        self.searchbar_btn = self.searchbar_canvas.create_image(342, 37, image=self.search_img, tags='searchbar_btn')

        self.searchbar_canvas.bind('<Enter>', self.on_searchbar_hover)
        self.searchbar_canvas.bind('<Leave>', self.on_searchbar_leave)
        self.searchbar_canvas.bind('<Button-1>', self.on_searchbar_click)

        self.searchbar_entry.bind('<Enter>', self.on_searchbar_hover)
        self.searchbar_entry.bind('<Leave>', self.on_searchbar_leave)
        self.searchbar_entry.bind('<Button-1>', self.on_searchbar_click)

        self.searchbar_canvas.tag_bind('searchbar_btn', '<Enter>', self.on_searchbar_hover)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Leave>', self.on_searchbar_leave)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Button-1>', self.on_searchbar_click)

        # Scrollable Frame

        self.scrollable_frame = tk.Frame(self.leftframe)
        self.scrollable_list_canvas = tk.Canvas(self.scrollable_frame, width=360)
        self.scrollable_list_frame = tk.Frame(self.scrollable_list_canvas)
        self.scrollable_list_frame_id = self.scrollable_list_canvas.create_window((0, 0), window=self.scrollable_list_frame, anchor="nw")
        self.scrollable_scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.scrollable_list_canvas.yview)
        self.scrollable_list_canvas.configure(yscrollcommand=self.scrollable_scrollbar.set)

        self.scrollable_list_canvas.xview_moveto(0)
        self.scrollable_list_canvas.yview_moveto(0)

        classes = self.data_manager.load_classes()
        for classe in classes:
            self.add_class(classe['name'], classe['students'])

        # Searchbar
        self.add_btn_canvas = tk.Canvas(self.leftframe, height=80, width=380, highlightthickness=0)
        self.create_add_button()
        
        self.scrollable_list_frame.bind('<Configure>', self._configure_interior)
        self.scrollable_list_canvas.bind('<Configure>', self._configure_canvas)
        self.scrollable_list_frame.bind("<Configure>", self.on_frame_configure)
        self.scrollable_list_canvas.bind('<Configure>', self.on_canvas_configure)
        self.scrollable_list_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_list_frame.bind("<MouseWheel>", self._on_mousewheel)

        self._configure_interior()

    def pack(self):
        self.leftframe.pack(fill='y', side='left')
        self.rightframe.pack(fill='both', expand=True, side='right')

        self.searchbar_canvas.pack(fill='x')
        self.scrollable_frame.pack(fill='both', expand=True)
        self.scrollable_list_canvas.pack(side='left', fill='both', expand=True)
        self.scrollable_scrollbar.pack(side='right', fill='y')

        self.add_btn_canvas.pack(fill='x')
    
    def searchbar_rounded_rectangle(self, x, y, width, height, r=25, **kwargs):    
        points = [x+r, y,
                x+r, y,
                x+width-r, y,
                x+width-r, y,
                x+width, y,
                x+width, y+r,
                x+width, y+r,
                x+width, y+height-r,
                x+width, y+height-r,
                x+width, y+height,
                x+width-r, y+height,
                x+width-r, y+height,
                x+r, y+height,
                x+r, y+height,
                x, y+height,
                x, y+height-r,
                x, y+height-r,
                x, y+r,
                x, y+r,
                x, y]
        return self.searchbar_canvas.create_polygon(points, **kwargs, smooth=True)

    def add_class(self, classe, nb_students):
        frame = tk.Frame(self.scrollable_list_frame, width=360, height=100)
        frame.pack()
        frame.pack_propagate(False)

        canvas = tk.Canvas(frame, width=360, height=100, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        original_dims = (14, 12, 340, 80)
        rect = self.rounded_rectangle(canvas, *original_dims, fill='lightgray', tags='class_rect')
        canvas.create_text(50, 40, text=classe, font=("San Francisco", 20, 'bold'), tags='class_text')
        canvas.create_text(60, 70, text=f"{nb_students} élèves", font=("San Francisco", 12), tags='class_text')
        canvas.create_image(332, 70, image=self.trash_img, tags='trash_btn')

        canvas.original_dims = original_dims

        canvas.tag_bind('trash_btn', '<Enter>', lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind('trash_btn', '<Leave>', lambda e: canvas.config(cursor=""))
        canvas.tag_bind('trash_btn', '<Button-1>', lambda e: self.on_trash_click(classe))

        canvas.tag_bind('class_rect', '<Enter>', lambda e: self.on_class_hover(e, canvas))
        canvas.tag_bind('class_rect', '<Leave>', lambda e: self.on_class_leave(e, canvas))
        canvas.tag_bind('class_text', '<Enter>', lambda e: self.on_class_hover(e, canvas))
        canvas.tag_bind('class_text', '<Leave>', lambda e: self.on_class_leave(e, canvas))

        frame.bind("<MouseWheel>", self._on_mousewheel)
        canvas.bind("<MouseWheel>", self._on_mousewheel)
        canvas.tag_bind('class_rect', '<Button-1>', lambda e, c=classe: self.display_class_details(c))
        canvas.tag_bind('class_text', '<Button-1>', lambda e, c=classe: self.display_class_details(c))

        return frame

    def create_add_button(self):
        circle = self.create_circle(self.add_btn_canvas, 40, 40, 25, fill='lightgray', outline='', tags='add_btn_circle')
        
        self.add_btn_canvas.create_text(40, 40, text='+', font=('San Francisco', 30), tags='add_btn_text')
        
        self.add_btn_canvas.addtag_withtag('add_btn', 'add_btn_circle')
        self.add_btn_canvas.addtag_withtag('add_btn', 'add_btn_text')
        
        self.add_btn_canvas.tag_bind('add_btn', '<Enter>', self.on_add_btn_hover)
        self.add_btn_canvas.tag_bind('add_btn', '<Leave>', self.on_add_btn_leave)
        self.add_btn_canvas.tag_bind('add_btn', '<Button-1>', self.add_new_class)

    def rounded_rectangle(self, canvas, x, y, width, height, r=25, **kwargs):
        points = [x+r, y,
            x+r, y,
            x+width-r, y,
            x+width-r, y,
            x+width, y,
            x+width, y+r,
            x+width, y+r,
            x+width, y+height-r,
            x+width, y+height-r,
            x+width, y+height,
            x+width-r, y+height,
            x+width-r, y+height,
            x+r, y+height,
            x+r, y+height,
            x, y+height,
            x, y+height-r,
            x, y+height-r,
            x, y+r,
            x, y+r,
            x, y]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_circle(self, canvas, x, y, r, **kwargs):
        return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def _configure_interior(self):
        size = (self.scrollable_list_frame.winfo_reqwidth(), self.scrollable_list_frame.winfo_reqheight())
        self.scrollable_list_canvas.config(scrollregion="0 0 %s %s" % size)
        if self.scrollable_list_frame.winfo_reqwidth() != self.scrollable_list_canvas.winfo_width():
            self.scrollable_list_canvas.config(width=self.scrollable_list_frame.winfo_reqwidth())
    
    def _configure_canvas(self):
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

    def _on_mousewheel(self, event):
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
        name = simpledialog.askstring("Nouvelle classe", "Nom de la classe:")
        if name:
            students = simpledialog.askinteger("Nouvelle classe", "Nombre d'élèves:")
            if students is not None:
                new_class = {"name": name, "students": students}
                self.data_manager.add_class(new_class)
                self.add_class(name, students)

    def on_trash_click(self, classe):
        print(f"Suppression de la classe {classe}")
        self.data_manager.remove_class(classe)
        
        # Supprimer visuellement la classe
        for widget in self.scrollable_list_frame.winfo_children():
            canvas = widget.winfo_children()[0]
            if canvas.type('class_text') == 'text':
                text_item = canvas.find_withtag('class_text')[0]
                if canvas.itemcget(text_item, 'text') == classe:
                    widget.destroy()
                    break
        
        # Reconfigurer le scrollable frame
        self._configure_interior()
        self.on_frame_configure()


    def display_class_details(self, classe):
        # Effacez le contenu précédent
        for widget in self.rightframe.winfo_children():
            widget.destroy()

        # Créez un cadre interne pour contenir tous les widgets
        inner_frame = tk.Frame(self.rightframe)
        inner_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Affichez le nom de la classe
        tk.Label(inner_frame, text=classe, font=("San Francisco", 24, 'bold'), anchor='w', justify='left').pack(fill='x', pady=(0, 20))

        # Récupérez les détails de la classe depuis le gestionnaire de données
        class_details = self.data_manager.get_class_details(classe)

        if class_details:
            # Affichez le nombre d'élèves
            tk.Label(inner_frame, text=f"Nombre d'élèves: {class_details['students']}", font=("San Francisco", 18), anchor='w', justify='left').pack(fill='x', pady=(0, 10))

            # Affichez la liste des élèves
            tk.Label(inner_frame, text="Liste des élèves:", font=("San Francisco", 18), anchor='w', justify='left').pack(fill='x', pady=(0, 10))
            if 'students_list' in class_details and isinstance(class_details['students_list'], list):
                for student in class_details['students_list']:
                    tk.Label(inner_frame, text=f"{student['firstname']} {student['lastname']}", font=("San Francisco", 14), anchor='w', justify='left').pack(fill='x')
            else:
                tk.Label(inner_frame, text="Aucun détail d'élève disponible", font=("San Francisco", 14), anchor='w', justify='left').pack(fill='x')
        else:
            tk.Label(inner_frame, text="Aucun détail disponible pour cette classe", font=("San Francisco", 14), anchor='w', justify='left').pack(fill='x')


    def get_class_details(self, class_name):
        classes = self.load_classes()
        for classe in classes:
            if classe['name'] == class_name:
                return classe
        return None

