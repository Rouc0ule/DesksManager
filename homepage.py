import tkinter as tk
from PIL import ImageTk, Image

class homePage:
    def __init__(self, root, theme):
        self.root = root

        self.search_img = ImageTk.PhotoImage(Image.open("Assets/{}_search.png".format(theme)).resize((25,25)))

        # WIDGETS

        self.leftframe = tk.Frame(self.root, width=400, highlightbackground="lightgray", highlightthickness=1)

        self.leftcanvas = tk.Canvas(self.leftframe, bg='gray')

        # Canvas Searchbar

        self.rounded_rectangle(10, 10, 360, 50, fill='lightgray')
        self.searchbar_entry = tk.Entry(font=("San Francisco", 9), relief=tk.FLAT, bg='lightgray')
        self.leftcanvas.create_window(10, 10, window=self.searchbar_entry)
        # Searchbar
        self.searchbar_frame = tk.Frame(self.leftframe, bg='lightgray')
        self.searchbar_entry2 = tk.Entry(self.searchbar_frame, font=("San Francisco", 9), relief=tk.FLAT, bg='lightgray')
        self.searchbar_btn = tk.Button(self.searchbar_frame, image=self.search_img, relief=tk.FLAT, bg='lightgray')

    def pack(self):
        self.leftframe.pack()
        self.leftcanvas.pack(fill='x')
        self.searchbar_frame.pack(padx=10, pady=10, fill='x')
        self.searchbar_entry2.pack(padx=(10,5), pady=5, side='left')
        self.searchbar_btn.pack(padx=(10,5), pady=5, side='right')
    
    def rounded_rectangle(self, x, y, width, height, r=25, **kwargs):    
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
        return self.leftcanvas.create_polygon(points, **kwargs, smooth=True)
