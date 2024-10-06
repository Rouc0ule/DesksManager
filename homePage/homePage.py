import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import ImageTk, Image
from homePage.dataManager import DataManager
from themeManager import ThemeManager

class HomePage:
    def __init__(self, root, theme):
        self.root = root
        self.data_manager = DataManager('Json/classes.json')
        self.sort_type = 'Date'
        self.sort_order = 'Descending'
        self.load_images()
        self.setup_frames()
        self.setup_widgets()
        self.load_classes()
        self.display_no_class_selected_message()
        self.theme_manager = ThemeManager()
        self.theme = self.theme_manager.set_current_theme(theme)
        
    def load_images(self):
        self.search_img = self.load_image("search")
        self.search_img_large = self.load_image("search", size=(30,30))
        self.trash_img = self.load_image("delete")
        self.trash_img_large = self.load_image("delete", size=(30, 30))
        self.edit_img = self.load_image("edit")
        self.edit_img_large = self.load_image("edit", size=(30,30))
        self.plus_img = self.load_image("plus_circle")
        self.warning_img_large = self.load_image("exclamationmark_triangle", size=(100,100))
        self.chevron_img = self.load_image("chevron_up")
        self.chevron_img_large = self.load_image("chevron_up", size=(30,30))

    def load_image(self, name, size=(25, 25)):
        return ImageTk.PhotoImage(Image.open(f"Assets/{self.theme}_{name}.png").resize(size))

    def setup_frames(self):
        self.left_frame = self.create_frame(self.root, width=400)
        self.right_frame = self.create_frame(self.root, width=400)

    def create_frame(self, parent, width=None, **kwargs):
        frame = tk.Frame(parent, highlightbackground="#d3d3d3", highlightthickness=1, **kwargs)
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
        self.searchbar_rect = self.rounded_rectangle(self.searchbar_canvas, 12, 12, 360, 50, fill='#d3d3d3', tags='searchbar_rect')
        self.searchbar_entry = tk.Entry(font=("San Francisco", 15), width=25, relief=tk.FLAT, highlightthickness=0, bg='#d3d3d3')
        self.searchbar_entry_window = self.searchbar_canvas.create_window(167, 37, window=self.searchbar_entry, tags='searchbar_entry')
        self.searchbar_btn = self.searchbar_canvas.create_image(342, 37, image=self.search_img, tags='searchbar_btn')

    def bind_searchbar_events(self):
        self.searchbar_canvas.bind('<Enter>', self.on_searchbar_hover)
        self.searchbar_canvas.bind('<Leave>', self.on_searchbar_leave)
        self.searchbar_canvas.tag_bind('searchbar_rect', '<Button-1>', self.on_searchbar_click)
        self.searchbar_entry.bind('<Enter>', self.on_searchbar_hover)
        self.searchbar_entry.bind('<Leave>', self.on_searchbar_leave)
        self.searchbar_entry.bind('<Button-1>', self.on_searchbar_click)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Enter>', self.on_search_btn_hover)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Leave>', self.on_search_btn_leave)
        self.searchbar_canvas.tag_bind('searchbar_btn', '<Button-1>', self.on_search_btn_click)
        self.searchbar_entry.bind('<Return>', self.on_search_btn_click)

    def on_search_btn_hover(self, event):
        self.searchbar_canvas.itemconfig('searchbar_btn', image=self.search_img_large)
        self.searchbar_canvas.config(cursor="hand2")

    def on_search_btn_leave(self, event):
        self.searchbar_canvas.itemconfig('searchbar_btn', image=self.search_img)
        self.searchbar_canvas.config(cursor="xterm")

    
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
        self.create_sort_btn()

    def load_classes(self):
        classes = self.data_manager.load_classes()
        self.sort_classes()

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
        self.rounded_rectangle(canvas, *original_dims, fill='#d3d3d3', tags='class_rect')
        canvas.create_text(25, 40, text=classe, font=("San Francisco", 20, 'bold'), anchor='w', tags='class_text')
        canvas.create_text(25, 70, text=f"{nb_students} élèves", font=("San Francisco", 12), anchor='w', tags='class_text')
        canvas.create_image(332, 70, image=self.trash_img, tags='trash_btn')
        canvas.original_dims = original_dims

    def bind_class_events(self, canvas, classe):
        canvas.tag_bind('trash_btn', '<Enter>', lambda e: self.on_trash_hover(canvas, True))
        canvas.tag_bind('trash_btn', '<Leave>', lambda e: self.on_trash_hover(canvas, False))
        canvas.tag_bind('trash_btn', '<Button-1>', lambda e: self.on_trash_click(classe))
        canvas.tag_bind('class_rect', '<Enter>', lambda e: self.on_class_hover(e, canvas))
        canvas.tag_bind('class_rect', '<Leave>', lambda e: self.on_class_leave(e, canvas))
        canvas.tag_bind('class_text', '<Enter>', lambda e: self.on_class_hover(e, canvas))
        canvas.tag_bind('class_text', '<Leave>', lambda e: self.on_class_leave(e, canvas))
        canvas.bind("<MouseWheel>", self.on_mousewheel)
        canvas.tag_bind('class_rect', '<Button-1>', lambda e, c=classe: self.display_class_details(c))
        canvas.tag_bind('class_text', '<Button-1>', lambda e, c=classe: self.display_class_details(c))

    def on_trash_hover(self, canvas, is_hover):
        if is_hover:
            canvas.itemconfig('trash_btn', image=self.trash_img_large)
            canvas.config(cursor="hand2")
        else:
            canvas.itemconfig('trash_btn', image=self.trash_img)
            canvas.config(cursor="")

    def create_add_button(self):
        self.create_circle(self.add_btn_canvas, 40, 40, 25, fill='#d3d3d3', outline='', tags='add_btn_circle')
        self.add_btn_canvas.create_text(40, 40, text='+', font=('San Francisco', 30), tags='add_btn_text')
        self.add_btn_canvas.addtag_withtag('add_btn', 'add_btn_circle')
        self.add_btn_canvas.addtag_withtag('add_btn', 'add_btn_text')
        self.add_btn_canvas.tag_bind('add_btn', '<Enter>', self.on_add_btn_hover)
        self.add_btn_canvas.tag_bind('add_btn', '<Leave>', self.on_add_btn_leave)
        self.add_btn_canvas.tag_bind('add_btn', '<Button-1>', self.add_new_class)

    def create_circle(self, canvas, x, y, r, **kwargs):
        return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def create_sort_btn(self):
        self.date_btn = self.rounded_rectangle(self.add_btn_canvas, 90, 25, 110, 30, r=20, fill='#d3d3d3', tags='type_btn')
        self.add_btn_canvas.create_text(100, 40, text='Date', font=('San Francisco', 13), anchor='w', tags='type_btn_text')
        self.add_btn_canvas.create_image(180, 40, image=self.chevron_img, tags='type_btn_chevron')
        
        self.order_btn = self.rounded_rectangle(self.add_btn_canvas, 210, 25, 130, 30, r=20, fill='#d3d3d3', tags='order_btn')
        self.add_btn_canvas.create_text(220, 40, text='Descending', font=('San Francisco', 13), anchor='w', tags='order_btn_text')
        self.add_btn_canvas.create_image(320, 40, image=self.chevron_img, tags='order_btn_chevron')

        self.date_dropdown = self.create_dropdown_menu(120, ['Date', 'Name', 'Students'])
        self.order_dropdown = self.create_dropdown_menu(120, ['Ascending', 'Descending'])

        self.add_btn_canvas.tag_bind('type_btn', '<Enter>', lambda e: self.on_sort_btn_hover(e, 'type_btn'))
        self.add_btn_canvas.tag_bind('type_btn', '<Leave>', lambda e: self.on_sort_btn_leave(e, 'type_btn'))
        self.add_btn_canvas.tag_bind('type_btn', '<Button-1>', lambda e: self.toggle_dropdown(self.date_dropdown, 'type_btn'))
        self.add_btn_canvas.tag_bind('type_btn_text', '<Enter>', lambda e: self.on_sort_btn_hover(e, 'type_btn'))
        self.add_btn_canvas.tag_bind('type_btn_text', '<Leave>', lambda e: self.on_sort_btn_leave(e, 'type_btn'))
        self.add_btn_canvas.tag_bind('type_btn_text', '<Button-1>', lambda e: self.toggle_dropdown(self.date_dropdown, 'type_btn'))
        self.add_btn_canvas.tag_bind('type_btn_chevron', '<Enter>', lambda e: self.on_sort_btn_hover(e, 'type_btn', image=True))
        self.add_btn_canvas.tag_bind('type_btn_chevron', '<Leave>', lambda e: self.on_sort_btn_leave(e, 'type_btn'))
        self.add_btn_canvas.tag_bind('type_btn_chevron', '<Button-1>', lambda e: self.toggle_dropdown(self.date_dropdown, 'type_btn'))

        self.add_btn_canvas.tag_bind('order_btn', '<Enter>', lambda e: self.on_sort_btn_hover(e, 'order_btn'))
        self.add_btn_canvas.tag_bind('order_btn', '<Leave>', lambda e: self.on_sort_btn_leave(e, 'order_btn'))
        self.add_btn_canvas.tag_bind('order_btn', '<Button-1>', lambda e: self.toggle_dropdown(self.order_dropdown, 'order_btn'))
        self.add_btn_canvas.tag_bind('order_btn_text', '<Enter>', lambda e: self.on_sort_btn_hover(e, 'order_btn'))
        self.add_btn_canvas.tag_bind('order_btn_text', '<Leave>', lambda e: self.on_sort_btn_leave(e, 'order_btn'))
        self.add_btn_canvas.tag_bind('order_btn_text', '<Button-1>', lambda e: self.toggle_dropdown(self.order_dropdown, 'order_btn'))
        self.add_btn_canvas.tag_bind('order_btn_chevron', '<Enter>', lambda e: self.on_sort_btn_hover(e, 'order_btn', image=True))
        self.add_btn_canvas.tag_bind('order_btn_chevron', '<Leave>', lambda e: self.on_sort_btn_leave(e, 'order_btn'))
        self.add_btn_canvas.tag_bind('order_btn_chevron', '<Button-1>', lambda e: self.toggle_dropdown(self.order_dropdown, 'order_btn'))

    def on_sort_btn_hover(self, event, btn_tag, image=False):
        self.add_btn_canvas.itemconfig(btn_tag, fill='#a0a0a0')
        if image:
            self.add_btn_canvas.itemconfig('{}_chevron'.format(btn_tag), image=self.chevron_img_large)
        self.add_btn_canvas.config(cursor="hand2")

    def on_sort_btn_leave(self, event, btn_tag):
        self.add_btn_canvas.itemconfig(btn_tag, fill='#d3d3d3')
        self.add_btn_canvas.itemconfig('{}_chevron'.format(btn_tag), image=self.chevron_img)
        self.add_btn_canvas.config(cursor="")

    def create_dropdown_menu(self, width, options):
        menu = tk.Toplevel(self.root)
        menu.withdraw()
        menu.overrideredirect(True)
        
        menu_canvas = tk.Canvas(menu, width=width, height=len(options) * 30, highlightthickness=0)
        menu_canvas.pack()

        self.rounded_rectangle(menu_canvas, 0, 0, width, len(options) * 30, r=20, fill='#b7b7b7', tags='menu_bg')
        
        for i, option in enumerate(options):
            y_pos = i * 30 + 15
            self.rounded_rectangle(menu_canvas, 0, y_pos-15, width, 30, r=20, fill='#b7b7b7', tags=f'option_{i}')
            menu_canvas.create_text(10, y_pos, text=option, anchor='w', font=('San Francisco', 12), tags=f'text_{i}')
            
            menu_canvas.tag_bind(f'option_{i}', '<Enter>', lambda e, i=i: self.on_option_hover(menu_canvas, i))
            menu_canvas.tag_bind(f'option_{i}', '<Leave>', lambda e, i=i: self.on_option_leave(menu_canvas, i))
            menu_canvas.tag_bind(f'option_{i}', '<Button-1>', lambda e, opt=option: self.on_option_select(opt, menu))
            menu_canvas.tag_bind(f'text_{i}', '<Enter>', lambda e, i=i: self.on_option_hover(menu_canvas, i))
            menu_canvas.tag_bind(f'text_{i}', '<Leave>', lambda e, i=i: self.on_option_leave(menu_canvas, i))
            menu_canvas.tag_bind(f'text_{i}', '<Button-1>', lambda e, opt=option: self.on_option_select(opt, menu))
        
        menu.bind('<Leave>', lambda e: self.hide_dropdown(menu))
        
        return menu

    def hide_dropdown(self, menu):
        menu.withdraw()

    def on_option_hover(self, canvas, i):
        canvas.itemconfig(f'option_{i}', fill='#a0a0a0')
        canvas.tag_raise(f'text_{i}')

    def on_option_leave(self, canvas, i):
        canvas.itemconfig(f'option_{i}', fill='#b7b7b7')

    def on_option_select(self, option, menu):
        menu.withdraw()
        if menu == self.date_dropdown:
            self.update_sort_btn_text('type_btn', option)
            self.sort_type = option
        elif menu == self.order_dropdown:
            self.update_sort_btn_text('order_btn', option)
            self.sort_order = option
        self.sort_classes()

    def sort_classes(self):
        classes = self.data_manager.load_classes()
        
        if self.sort_type == 'Date':
            classes.sort(key=lambda x: x.get('creation_date', ''))
        elif self.sort_type == 'Name':
            classes.sort(key=lambda x: x['name'])
        elif self.sort_type == 'Students':
            classes.sort(key=lambda x: len(x.get('students_list', [])))
        
        if self.sort_order == 'Descending':
            classes.reverse()
        
        for widget in self.scrollable_list_frame.winfo_children():
            widget.destroy()
        
        for classe in classes:
            self.add_class(classe['name'], len(classe.get('students_list', [])))
        
        self.configure_interior()
        self.on_frame_configure()

    def update_sort_btn_text(self, btn_tag, new_text):
        text_tag = f'{btn_tag}_text'
        self.add_btn_canvas.itemconfig(text_tag, text=new_text)

    def reset_sort_buttons(self):
        self.update_sort_btn_text('type_btn', 'Date')
        self.update_sort_btn_text('order_btn', 'Ascending')

    def toggle_dropdown(self, dropdown, button):
        if dropdown.winfo_viewable():
            dropdown.withdraw()
        else:
            button_bbox = self.add_btn_canvas.bbox(button)
            x = self.add_btn_canvas.winfo_rootx() + button_bbox[0]
            y = self.add_btn_canvas.winfo_rooty() + button_bbox[1] - dropdown.winfo_reqheight()
            dropdown.geometry(f"+{x}+{y}")
            dropdown.deiconify()
            dropdown.focus_set()

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
            self.rounded_rectangle(canvas, *canvas.original_dims, fill='#d3d3d3', tags='class_rect')
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
        self.searchbar_canvas.itemconfig('searchbar_rect', fill='#d3d3d3')
        self.searchbar_entry.config(bg='#d3d3d3')
        self.searchbar_canvas.itemconfig('searchbar_btn', image=self.search_img)
        self.searchbar_canvas.config(cursor="")

    def on_searchbar_click(self, event):
        self.searchbar_entry.focus_set()
        self.on_searchbar_hover(event)

    def on_search_btn_click(self, event=None):
        search_text = self.searchbar_entry.get().lower()
        self.filter_classes(search_text)

    def filter_classes(self, search_text):
        for widget in self.scrollable_list_frame.winfo_children():
            widget.destroy()
        
        classes = self.data_manager.load_classes()
        filtered_classes = [classe for classe in classes if search_text in classe['name'].lower()]
        
        for classe in filtered_classes:
            self.add_class(classe['name'], len(classe.get('students_list', [])))
        
        self.configure_interior()
        self.on_frame_configure()

    def on_mousewheel(self, event):
        self.scrollable_list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_add_btn_hover(self, event):
        self.add_btn_canvas.itemconfig('add_btn_circle', fill='#a0a0a0')
        self.add_btn_canvas.itemconfig('add_btn_text', fill='black', font=('San Francisco', 33))
        self.add_btn_canvas.config(cursor="hand2")

    def on_add_btn_leave(self, event):
        self.add_btn_canvas.itemconfig('add_btn_circle', fill='#d3d3d3')
        self.add_btn_canvas.itemconfig('add_btn_text', fill='black', font=('San Francisco', 30))
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
        self.display_no_class_selected_message()

    def display_class_details(self, classe=None):
        if classe is None or self.data_manager.get_class_details(classe) is None:
            self.display_no_class_selected_message()
            return

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        class_details = self.data_manager.get_class_details(classe)

        details_frame = self.create_frame(self.right_frame)
        students_frame = self.create_frame(self.right_frame)

        details_frame.pack(side='left', fill='both', expand=True)
        students_frame.pack(side='right', fill='both', expand=True)
        
        self.details_canvas = self.create_canvas(details_frame)
        self.details_canvas.pack(fill='both')

        self.details_canvas.create_image(30, 50, image=self.edit_img, tag='edit_btn')
        self.class_name_text = self.details_canvas.create_text(50, 50, text='Classe : ' + class_details.get('name', ''), font=("San Francisco", 20, 'bold'), anchor='w')
        self.details_canvas.create_text(50, 80, text=('{} élèves'.format(len(class_details.get('students_list', [])))), font=("San Francisco", 17, 'italic'), anchor='w')

        self.details_canvas.tag_bind('edit_btn', '<Enter>', lambda e: self.on_edit_hover(self.details_canvas, True))
        self.details_canvas.tag_bind('edit_btn', '<Leave>', lambda e: self.on_edit_hover(self.details_canvas, False))
        self.details_canvas.tag_bind('edit_btn', '<Button-1>', lambda e: self.edit_class_name(classe))

        self.student_list_name_canvas = self.create_canvas(students_frame, width=360, height=50)
        self.student_list_name_canvas.pack()
        self.student_list_name_canvas.create_text(180, 25, text='STUDENT LIST', font=("San Francisco", 17, 'bold'))

        self.create_student_list(students_frame, class_details)

        self.create_rounded_button(students_frame, 250, 50, text='Add Student', icon=self.plus_img, padx=5, pady=5, command=lambda event: self.add_student(classe))

    def display_no_class_selected_message(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        
        message_canvas = self.create_canvas(self.right_frame, width=500, height=500)
        message_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        message_canvas.create_image(250, 200, image=self.warning_img_large)
        message_canvas.create_text(250, 275, text="Aucune classe n'est sélectionnée", font=("San Francisco", 20, 'bold'))

    def on_edit_hover(self, canvas, is_hover):
        if is_hover:
            canvas.itemconfig('edit_btn', image=self.edit_img_large)
            canvas.config(cursor="hand2")
        else:
            canvas.itemconfig('edit_btn', image=self.edit_img)
            canvas.config(cursor="")

    def edit_class_name(self, classe):
        class_details = self.data_manager.get_class_details(classe)
        if class_details is None:
            print(f"La classe {classe} n'existe plus.")
            return
        current_name = class_details['name']
        entry = tk.Entry(self.details_canvas, font=("San Francisco", 20, 'bold'))
        entry.insert(0, current_name)
        entry_window = self.details_canvas.create_window(50, 50, window=entry, anchor='w')
        
        def save_new_name(event):
            new_name = entry.get()
            if new_name and new_name != current_name:
                self.data_manager.update_class_name(classe, new_name)
                self.update_class_list()
                self.display_class_details(class_details['name'])
            
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

        student_canvas = self.create_canvas(student_scrollable_frame, width=360, height=200) 
        student_scrollbar = tk.Scrollbar(student_scrollable_frame, orient="vertical", command=student_canvas.yview)

        student_inner_frame = tk.Frame(student_canvas)

        student_canvas.configure(yscrollcommand=student_scrollbar.set)
        student_canvas.create_window((0, 0), window=student_inner_frame, anchor="nw")

        for student in class_details.get('students_list', []):
            self.add_student_to_list(student_inner_frame, class_details['name'], student)

        student_inner_frame.bind("<Configure>", lambda e: student_canvas.configure(scrollregion=student_canvas.bbox("all")))

        student_canvas.pack(side="left", fill="y", expand=True)
        student_scrollbar.pack(side="right", fill="y")

        student_canvas.bind("<MouseWheel>", self.on_student_mousewheel)
        student_inner_frame.bind("<MouseWheel>", self.on_student_mousewheel)

        self.student_canvas = student_canvas

    def on_student_mousewheel(self, event):
        self.student_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_student_to_list(self, parent_frame, classe, student):
        student_frame = tk.Frame(parent_frame, width=360, height=75)
        student_frame.pack()
        student_frame.pack_propagate(False)

        canvas = self.create_canvas(student_frame, width=360, height=75)
        canvas.pack(fill=tk.BOTH, expand=True)

        original_dims = (5, 5, 350, 65)
        self.rounded_rectangle(canvas, *original_dims, fill='#d3d3d3', tags='student_rect')

        canvas.create_text(25, 37, text=f"{student['firstname']} {student['lastname']}", 
                        font=("San Francisco", 16), anchor='w', tags='student_text')
        canvas.create_image(335, 50, image=self.trash_img, tags='trash_btn')

        canvas.original_dims = original_dims

        self.bind_student_events(canvas, classe, student)

    def bind_student_events(self, canvas, classe, student):
        canvas.tag_bind('trash_btn', '<Enter>', lambda e: self.on_trash_hover(canvas, True))
        canvas.tag_bind('trash_btn', '<Leave>', lambda e: self.on_trash_hover(canvas, False))
        canvas.tag_bind('trash_btn', '<Button-1>', lambda e: self.remove_student(classe, student))

        canvas.tag_bind('student_rect', '<Enter>', lambda e: self.on_student_hover(e, canvas))
        canvas.tag_bind('student_rect', '<Leave>', lambda e: self.on_student_leave(e, canvas))
        canvas.tag_bind('student_text', '<Enter>', lambda e: self.on_student_hover(e, canvas))
        canvas.tag_bind('student_text', '<Leave>', lambda e: self.on_student_leave(e, canvas))
        canvas.bind("<MouseWheel>", self.on_student_mousewheel)

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
            self.rounded_rectangle(canvas, 5, 5, 350, 65, fill='#d3d3d3', tags='student_rect')
            canvas.config(cursor="")
            canvas.tag_raise('student_text')
            canvas.tag_raise('trash_btn')

    def add_student(self, classe):
        firstname = simpledialog.askstring("Nouvel élève", "Prénom de l'élève:")
        if firstname:
            lastname = simpledialog.askstring("Nouvel élève", "Nom de l'élève:")
            if lastname:
                new_student = {"firstname": firstname, "lastname": lastname}
                self.data_manager.add_student(classe, new_student)
                self.display_class_details(classe)
                self.update_class_list()

    def remove_student(self, classe, student):
        if messagebox.askyesno("Supprimer l'élève", f"Voulez-vous vraiment supprimer {student['firstname']} {student['lastname']} ?"):
            self.data_manager.remove_student(classe, f"{student['firstname']} {student['lastname']}")
            self.display_class_details(classe)
            self.update_class_list()

    def create_rounded_button(self, parent, width, height, text, padx=0, pady=0, icon=None, command=None):
        canvas_width , canvas_height = width + 6, height + 6
        canvas = self.create_canvas(parent, width=canvas_width, height=canvas_height)
        canvas.pack(padx=padx, pady=pady)

        self.rounded_rectangle(canvas, 3, 3, width, height, r=30, fill='#d3d3d3', tags='rounded_rect')
        canvas.create_text(canvas_width // 2, canvas_height // 2, text=text, font=('San Francisco', 14), tags='text')
        canvas.create_image(25, canvas_height // 2, image=icon, tags='icon')

        canvas.tag_bind('rounded_rect', '<Enter>', lambda event: self._on_button_over(canvas, width, height))
        canvas.tag_bind('rounded_rect', '<Leave>', lambda event: self._on_button_leave(canvas, width, height))
        canvas.tag_bind('text', '<Enter>', lambda event: self._on_button_over(canvas, width, height))
        canvas.tag_bind('text', '<Leave>', lambda event: self._on_button_leave(canvas, width, height))
        canvas.tag_bind('icon', '<Enter>', lambda event: self._on_button_over(canvas, width, height))
        canvas.tag_bind('icon', '<Leave>', lambda event: self._on_button_leave(canvas, width, height))
        
        if command:
            canvas.tag_bind('rounded_rect', '<Button-1>', command)
            canvas.tag_bind('text', '<Button-1>', command)
            canvas.tag_bind('icon', '<Button-1>', command)

        return canvas

    def _on_button_over(self, canvas, width, height):
        if canvas.cget('cursor') != "hand2":
            canvas.config(cursor="hand2")
            canvas.delete('rounded_rect')
            self.rounded_rectangle(canvas, 0, 0, width+6, height+6, r=30, fill='#a0a0a0', tags='rounded_rect')
            canvas.tag_raise('text')
            canvas.tag_raise('icon')

    def _on_button_leave(self, canvas, width, height):
        if canvas.cget('cursor') != "":
            canvas.config(cursor="")
            canvas.delete('rounded_rect')
            self.rounded_rectangle(canvas, 3, 3, width, height, r=30, fill='#d3d3d3', tags='rounded_rect')
            canvas.tag_raise('text')
            canvas.tag_raise('icon')