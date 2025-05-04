class ApprenticeshipOpening:
    def __init__(self, specialization, location, stipend, required_skills, opening_id=None):
        self.opening_id = opening_id  # Optional: Assigned by the database
        self.specialization = specialization
        self.location = location
        self.stipend = stipend
        self.required_skills = required_skills  # List of skills

    def __repr__(self):
        return f"Opening(specialization={self.specialization}, location={self.location}, stipend={self.stipend})"