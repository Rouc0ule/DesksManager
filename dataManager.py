import json

class DataManager:
    def __init__(self, json_file):
        self.json_file = json_file
        self.classes = self.load_classes()

    def load_classes(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    def save_classes(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.classes, file, indent=4)

    def update_class_name(self, old_name, new_name):
        for classe in self.classes:
            if classe['name'] == old_name:
                classe['name'] = new_name
                break
        self.save_classes()

    def add_class(self, new_class):
        if 'students_list' not in new_class:
            new_class['students_list'] = []
        self.classes.append(new_class)
        self.save_classes()

    def remove_class(self, class_name):
        self.classes = [c for c in self.classes if c['name'] != class_name]
        self.save_classes()

    def update_class(self, updated_class):
        for i, c in enumerate(self.classes):
            if c['name'] == updated_class['name']:
                self.classes[i] = updated_class
                break
        self.save_classes()

    def get_class_details(self, class_name):
        for classe in self.classes:
            if classe['name'] == class_name:
                return classe
        return None

    def add_student(self, class_name, student):
        for classe in self.classes:
            if classe['name'] == class_name:
                if 'students_list' not in classe:
                    classe['students_list'] = []
                classe['students_list'].append(student)
                break
        self.save_classes()

    def remove_student(self, class_name, student_name):
        for classe in self.classes:
            if classe['name'] == class_name:
                classe['students_list'] = [s for s in classe['students_list'] if s['firstname'] + ' ' + s['lastname'] != student_name]
                break
        self.save_classes()