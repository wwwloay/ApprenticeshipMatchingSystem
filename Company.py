class Company:
    def __init__(self, CompanyId, CompanyName, Type, Specialty, CommercialRegisterNumber, NumberOfEmployees, Location, TelephoneNumber):
        self.CompanyId = CompanyId
        self.CompanyName = CompanyName
        self.Type = Type
        self.Specialty = Specialty
        self.CommercialRegisterNumber = CommercialRegisterNumber
        self.NumberOfEmployees = NumberOfEmployees
        self.Location = Location
        self.TelephoneNumber = TelephoneNumber
        self.AvailableJobs = []  # Placeholder for associated apprenticeship openings

    def __repr__(self):
        return f"Company(name={self.CompanyName}, specialty={self.Specialty}, location={self.Location})"