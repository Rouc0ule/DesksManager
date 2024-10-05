import tkinter as tk
from homePage import HomePage
from classroomPage import ClassroomPage
#import pywinstyles

class main(tk.Tk):
    def __init__(self): 
        tk.Tk.__init__(self)
        #pywinstyles.apply_style(root, "acrylic")

        self.theme = 'light'
        self.grid_size = 10
        self.number_of_items = 0
        self.Pages('classroom')

    def Pages(self, page):
        if page == 'homepage':
            self.varhomepage = HomePage(self, self.theme)
            self.varhomepage.pack_widgets()
        elif page == 'classroom':
            self.classroomPage = ClassroomPage(self, self.theme, self.grid_size)
            self.classroomPage.pack_widgets()

    def center_window(self, width, height):
        self.update_idletasks()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == '__main__':
    root = main()
    root.title('DesksManager')
    root.resizable(False, False)
    root.center_window(1300, 820)
    root.mainloop()