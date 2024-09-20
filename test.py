from tkinter import *
import math


WIDTH = 400
HEIGHT = 400
CANVAS_MID_X = WIDTH/2
CANVAS_MID_Y = HEIGHT/2
SIDE = WIDTH/4

root = Tk()
canvas = Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
canvas.pack()

vertices = [
                    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y - SIDE/2],
                    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y - SIDE/2],
                    [CANVAS_MID_X + SIDE/2, CANVAS_MID_Y + SIDE/2],
                    [CANVAS_MID_X - SIDE/2, CANVAS_MID_Y + SIDE/2]]

def rotate(points, angle):
    new_points = list(points)
    rad = angle * (math.pi/180)
    cos_val = math.cos(rad)
    sin_val = math.sin(rad)
    for coords in new_points:
        x_val =  coords[0] 
        y_val = coords[1]
        coords[0] = x_val * cos_val - y_val * sin_val
        coords[1] = x_val * sin_val + y_val * cos_val
    return new_points

def draw_square(points):
    canvas.create_polygon(points, fill="red")

def test():
    print ("vertices: ", vertices, "should be: ", "[[150, 150], [250, 150], [250, 250], [150, 250]]")


new_square = rotate(vertices, 10)
draw_square(new_square)
test()
mainloop()