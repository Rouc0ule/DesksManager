import json

class DataManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_classes(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_classes(self, classes):
        with open(self.file_path, 'w') as file:
            json.dump(classes, file, indent=2)

    def add_class(self, new_class):
        classes = self.load_classes()
        classes.append(new_class)
        self.save_classes(classes)

    def remove_class(self, class_name):
        classes = self.load_classes()
        classes = [c for c in classes if c['name'] != class_name]
        self.save_classes(classes)

    def update_class(self, updated_class):
        classes = self.load_classes()
        for i, c in enumerate(classes):
            if c['name'] == updated_class['name']:
                classes[i] = updated_class
                break
        self.save_classes(classes)
