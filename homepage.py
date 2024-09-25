import tkinter as tk
from PIL import ImageTk, Image

class homePage:
    def __init__(self, root, theme):
        self.root = root

        self.search_img = ImageTk.PhotoImage(Image.open("Assets/{}_search.png".format(theme)).resize((25,25)))

        # WIDGETS

        self.leftframe = tk.Frame(self.root, width=400, highlightbackground="lightgray", highlightthickness=1)

        # Canvas Searchbar

        self.searchbar_canvas = tk.Canvas(self.leftframe, height=70, width=380, highlightthickness=0)
        self.searchbar_rect = self.rounded_rectangle(self.searchbar_canvas, 12, 12, 360, 50, fill='lightgray', tags='searchbar_rect')
        self.searchbar_entry = tk.Entry(font=("San Francisco", 15), width=25, relief=tk.FLAT, bg='lightgray')
        self.searchbar_entry_window = self.searchbar_canvas.create_window(167, 37, window=self.searchbar_entry, tags='searchbar_entry')
        self.searchbar_btn = tk.Button(image=self.search_img, relief=tk.FLAT, bg='lightgray')
        self.searchbar_btn_window = self.searchbar_canvas.create_window(342, 37, window=self.searchbar_btn, tags='searchbar_btn')

        # Lier les événements au canvas et aux widgets
        for item in [self.searchbar_canvas, self.searchbar_entry, self.searchbar_btn]:
            item.bind('<Enter>', self.on_searchbar_hover)
            item.bind('<Leave>', self.on_searchbar_leave)
            item.bind('<Button-1>', self.on_searchbar_click)

        # Scrollable Frame

        self.scrollable_frame = tk.Frame(self.leftframe)
        self.scrollable_list_canvas = tk.Canvas(self.scrollable_frame, width=360)
        self.scrollable_list_frame = tk.Frame(self.scrollable_list_canvas)
        self.scrollable_list_frame_id = self.scrollable_list_canvas.create_window((0, 0), window=self.scrollable_list_frame, anchor="nw")
        self.scrollable_scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.scrollable_list_canvas.yview)
        self.scrollable_list_canvas.configure(yscrollcommand=self.scrollable_scrollbar.set)

        self.scrollable_list_canvas.xview_moveto(0)
        self.scrollable_list_canvas.yview_moveto(0)

        for classe, nb_students in [('3°4', 43), ('6°3', 35), ('4°1', 38), ('5°6', 40),
                                    ('3°4', 43), ('6°3', 35), ('4°1', 38), ('5°6', 40)]:
            self.add_class(classe, nb_students)


        # Searchbar
        self.searchbar_frame = tk.Frame(self.leftframe, bg='lightgray')
        self.searchbar_entry2 = tk.Entry(self.searchbar_frame, font=("San Francisco", 9), relief=tk.FLAT, bg='lightgray')
        self.searchbar_btn2 = tk.Button(self.searchbar_frame, image=self.search_img, relief=tk.FLAT, bg='lightgray')
        
        self.scrollable_list_frame.bind('<Configure>', self._configure_interior)
        self.scrollable_list_canvas.bind('<Configure>', self._configure_canvas)
        self.scrollable_list_frame.bind("<Configure>", self.on_frame_configure)
        self.scrollable_list_canvas.bind('<Configure>', self.on_canvas_configure)


    def pack(self):
        self.leftframe.pack(fill='y', side='left')
        self.searchbar_canvas.pack(fill='x')

        self.scrollable_frame.pack(fill='both', expand=True)
        self.scrollable_list_canvas.pack(side='left', fill='both', expand=True)
        self.scrollable_scrollbar.pack(side='right', fill='y')

        self.searchbar_frame.pack(padx=10, pady=10, fill='x')
        self.searchbar_entry2.pack(padx=(10,5), pady=5, side='left', expand=True, fill='x')
        self.searchbar_btn2.pack(padx=(10,5), pady=5, side='right')
    
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
        frame.pack(pady=5)
        frame.pack_propagate(False)

        canvas = tk.Canvas(frame, width=360, height=100, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        rect = self.rounded_rectangle(canvas, 14, 12, 340, 80, fill='lightgray', tags='class_rect')
        canvas.create_text(50, 40, text=classe, font=("San Francisco", 20, 'bold'), tags='class_text')
        canvas.create_text(60, 70, text=f"{nb_students} élèves", font=("San Francisco", 12), tags='class_text')

        canvas.tag_bind('class_rect', '<Enter>', lambda e: self.on_hover(e, canvas))
        canvas.tag_bind('class_rect', '<Leave>', lambda e: self.on_leave(e, canvas))
        canvas.tag_bind('class_text', '<Enter>', lambda e: self.on_hover(e, canvas))
        canvas.tag_bind('class_text', '<Leave>', lambda e: self.on_leave(e, canvas))

        return frame


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


    def _configure_interior(self):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.scrollable_list_frame.winfo_reqwidth(), self.scrollable_list_frame.winfo_reqheight())
        self.scrollable_list_canvas.config(scrollregion="0 0 %s %s" % size)
        if self.scrollable_list_frame.winfo_reqwidth() != self.scrollable_list_canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.scrollable_list_canvas.config(width=self.scrollable_list_frame.winfo_reqwidth())
    
    def _configure_canvas(self):
        if self.scrollable_list_frame.winfo_reqwidth() != self.scrollable_list_canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.scrollable_list_canvas.itemconfigure(self.scrollable_list_frame_id, width=self.scrollable_list_canvas.winfo_width())

    def on_frame_configure(self, event=None):
        self.scrollable_list_canvas.configure(scrollregion=self.scrollable_list_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        width = event.width
        self.scrollable_list_canvas.itemconfig(self.scrollable_list_frame_id, width=width)

    def on_hover(self, event, canvas):
        canvas.itemconfig('class_rect', fill='#a0a0a0')
        canvas.config(cursor="hand2")

    def on_leave(self, event, canvas):
        canvas.itemconfig('class_rect', fill='lightgray')
        canvas.config(cursor="")

    def on_searchbar_hover(self, event):
        self.searchbar_canvas.itemconfig('searchbar_rect', fill='#a0a0a0')
        self.searchbar_entry.config(bg='#a0a0a0')
        self.searchbar_btn.config(bg='#a0a0a0')
        self.searchbar_canvas.config(cursor="hand2")
        self.searchbar_btn.config(cursor="hand2")

    def on_searchbar_leave(self, event):
        # Vérifier si le curseur est toujours sur un des éléments de la barre de recherche
        x, y = self.searchbar_canvas.winfo_pointerxy()
        widget_under_cursor = self.searchbar_canvas.winfo_containing(x, y)
        if widget_under_cursor in [self.searchbar_canvas, self.searchbar_entry, self.searchbar_btn]:
            return

        self.searchbar_canvas.itemconfig('searchbar_rect', fill='lightgray')
        self.searchbar_entry.config(bg='lightgray')
        self.searchbar_btn.config(bg='lightgray')
        self.searchbar_canvas.config(cursor="")
        self.searchbar_btn.config(cursor="")

    def on_searchbar_click(self, event):
        self.searchbar_entry.focus_set()
        # Assurez-vous que l'effet de survol est appliqué même après le clic
        self.on_searchbar_hover(event)