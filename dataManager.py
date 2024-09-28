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
        if 'students_list' not in new_class:
            new_class['students_list'] = []
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

    def get_class_details(self, class_name):
        classes = self.load_classes()
        for classe in classes:
            if classe['name'] == class_name:
                return classe
        return None

    def add_student(self, class_name, student):
        classes = self.load_classes()
        for classe in classes:
            if classe['name'] == class_name:
                if 'students_list' not in classe:
                    classe['students_list'] = []
                classe['students_list'].append(student)
                break
        self.save_classes(classes)

    def remove_student(self, class_name, student_name):
        classes = self.load_classes()
        for classe in classes:
            if classe['name'] == class_name:
                classe['students_list'] = [s for s in classe['students_list'] if s['firstname'] + ' ' + s['lastname'] != student_name]
                break
        self.save_classes(classes)
    
    def update_class_name(self, old_name, new_name):
        classes = self.load_classes()
        for classe in classes:
            if classe['name'] == old_name:
                classe['name'] = new_name
                break
        self.save_classes(classes)