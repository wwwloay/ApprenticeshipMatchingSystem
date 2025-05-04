class Company:
    def __init__(self, CompanyId, CompanyName, Type, Specialty, CommercialRegisterNumber, NumberOfEmployees, Location, TelephoneNumber, Email, Password):
        self.CompanyId = CompanyId
        self.CompanyName = CompanyName
        self.Type = Type
        self.Specialty = Specialty
        self.CommercialRegisterNumber = CommercialRegisterNumber
        self.NumberOfEmployees = NumberOfEmployees
        self.Location = Location
        self.TelephoneNumber = TelephoneNumber
        self.Email = Email
        self.Password = Password
        self.Openings = []
        self.AvailableJobs = []  # Placeholder for associated apprenticeship openings

    def __repr__(self):
        return f"Company(name={self.CompanyName}, specialty={self.Specialty}, location={self.Location})"