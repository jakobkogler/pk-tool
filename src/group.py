class Group:
    def __init__(self, name, group_type='', instructor='', tutor1='', tutor2='',
                 substitute1='', substitute2='', students=None):
        self.name = name
        self.group_type = group_type
        self.instructor = instructor
        self.tutor1 = tutor1
        self.tutor2 = tutor2
        self.substitute1 = substitute1
        self.substitute2 = substitute2
        self.students = students if students else []

    def add_student(self, student):
        self.students.append(student)
