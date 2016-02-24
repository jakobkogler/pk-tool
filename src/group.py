class Group:
    """
    Represent a group of students. Stores the names of the instructor and the tutors,
    and all the names, register-numbers and e-mails from students.
    """

    def __init__(self, name, group_type='', instructor='', tutor1='', tutor2='',
                 substitute1='', substitute2='', students=None):
        """
        Initializes a group
        """
        self.name = name
        self.group_type = group_type
        self.instructor = instructor
        self.tutor1 = tutor1
        self.tutor2 = tutor2
        self.substitute1 = substitute1
        self.substitute2 = substitute2
        self.students = students if students else []

    def add_student(self, student):
        """
        Adds a student to the group
        """
        self.students.append(student)
