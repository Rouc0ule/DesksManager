import tkinter as tk
from PIL import ImageTk, Image

class homePage:
    def __init__(self, root, theme):
        self.root = root

        self.search_img = ImageTk.PhotoImage(Image.open("Assets/{}_search.png".format(theme)).resize((25,25)))

        # WIDGETS

        self.leftframe = tk.Frame(self.root, width=400, highlightbackground="lightgray", highlightthickness=1)

        # Searchbar
        self.searchbar_frame = tk.Frame(self.leftframe, bg='lightgray')
        self.searchbar_entry = tk.Entry(self.searchbar_frame, font=("San Francisco", 9), relief=tk.FLAT, bg='lightgray')
        self.searchbar_btn = tk.Button(self.searchbar_frame, image=self.search_img, relief=tk.FLAT, bg='lightgray')

    def pack(self):
        self.leftframe.pack()
        self.searchbar_frame.pack(padx=10, pady=10, fill='x')
        self.searchbar_entry.pack(padx=(10,5), pady=5, side='left')
        self.searchbar_btn.pack(padx=(10,5), pady=5, side='right')

