import json
from os import path

class JsonManager:
    def __init__(self):
        self.studentclasslistpath = 'Json/studentclass.json'
        
    def add_student(self, studentclass, lastname, firstname):
        if not path.isfile(self.studentclasslistpath):
            raise Exception("File not found")
        
        with open(self.studentclasslistpath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if "class" not in data:
            raise Exception("Structure 'class' not found in JSON")
        
        if studentclass not in data["class"]:
            raise Exception(f"Class {studentclass} not found")
        
        student_info = {"lastname": lastname, "firstname": firstname}
        
        if lastname not in data["class"][studentclass]:
            data["class"][studentclass][lastname] = student_info
        else:
            data["class"][studentclass][lastname] = student_info
        
        with open(self.studentclasslistpath, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def get_students(self, studentclass):
        if not path.isfile(self.studentclasslistpath):
            raise Exception("File not found")
        
        with open(self.studentclasslistpath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if "class" not in data or studentclass not in data["class"]:
            return []
        
        return list(data["class"][studentclass].values())

    def remove_student(self, studentclass, lastname):
        if not path.isfile(self.studentclasslistpath):
            raise Exception("File not found")
        
        with open(self.studentclasslistpath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if "class" not in data or studentclass not in data["class"]:
            raise Exception(f"Class {studentclass} not found")
        
        if lastname in data["class"][studentclass]:
            del data["class"][studentclass][lastname]
            
            with open(self.studentclasslistpath, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
        else:
            raise Exception(f"Student {lastname} not found in class {studentclass}")
