class Student:
    def __init__(self, name, mobile_number, email, password, student_id, gpa, specialization, skills, preferred_locations):
        self.name = name
        self.mobile_number = mobile_number
        self.email = email
        self.password = password
        self.student_id = student_id
        self.gpa = gpa
        self.specialization = specialization
        self.skills = skills  # List of skills
        self.preferred_locations = preferred_locations  # List of locations in order of preference
    
    def __repr__(self):
        return f"Student(name={self.name}, gpa={self.gpa}, specialization={self.specialization})"