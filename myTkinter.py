import tkinter as tk

class GUITkinter():

    def Button(parent, command, text='Custom Button', width=500, height=250, color='#0000FF', hover_color='#0000AA', corner_radius=25):
        c = tk.Canvas(parent, width=width, height=height, bg='gray')
        c.place(relx=0.5, rely=0.5)
        x1, y1, x2, y2 = 0, 0, width, height
        points = (x1+corner_radius, y1,
                 x2-corner_radius, y1,
                 x2, y1,
                 x2, y1+corner_radius,
                 x2, y2-corner_radius,
                 x2, y2,
                 x2-corner_radius, y2,
                 x1+corner_radius, y2,
                 x1, y2,
                 x1, y2-corner_radius,
                 x1, y1+corner_radius,
                 x1, y1)
        c.create_polygon(points, fill=color, smooth=True)
        c.create_oval(x1-10, y1-10, x1+10, y1+10, fill='red')
        c.create_oval(width-10, height-10, width+10, height+10, fill='red')