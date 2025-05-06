class Company:
    def __init__(self, company_id, company_name, kind, specialty, commercial_register_number, number_of_employees, location, telephone_number, email, password):
        self.company_id = company_id
        self.company_name = company_name
        self.kind = kind
        self.specialty = specialty
        self.commercial_register_number = commercial_register_number
        self.number_of_employees = number_of_employees
        self.location = location
        self.telephone_number = telephone_number
        self.email = email
        self.password = password

    def __repr__(self):
        return f"Company(name={self.company_name}, specialty={self.specialty}, location={self.location})"