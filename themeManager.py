import json

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": self.load_theme("light_theme.json"),
            "dark": self.load_theme("dark_theme.json")
        }

    def load_theme(self, filename):
        with open(f"themes/{filename}", "r") as file:
            return json.load(file)

    def get_color(self, element):
        return self.themes[self.current_theme].get(element, "#000000")  # Default to black if not found

    def switch_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"

    def get_current_theme(self):
        return self.current_theme
    
    def set_current_theme(self, theme):
        self.current_theme = theme
        return self.current_theme