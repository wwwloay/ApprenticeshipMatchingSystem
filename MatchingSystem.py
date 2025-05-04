import sqlite3
from Company import Company
from Student import Student
from ApprenticeshipOpening import ApprenticeshipOpening


class MatchingSystem:
    def __init__(self, db_name="apprenticeship.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def initialize_db(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Companies (
                    CompanyId INTEGER PRIMARY KEY AUTOINCREMENT,
                    CompanyName TEXT NOT NULL,
                    Type TEXT,
                    Specialty TEXT,
                    CommercialRegisterNumber TEXT UNIQUE,
                    NumberOfEmployees INTEGER,
                    Location TEXT,
                    TelephoneNumber TEXT,
                    Email TEXT UNIQUE,  -- Ensure Email column exists
                    Password TEXT       -- Ensure Password column exists
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Openings (
                    OpeningId INTEGER PRIMARY KEY AUTOINCREMENT,
                    CompanyId INTEGER,
                    Specialization TEXT NOT NULL,
                    Location TEXT NOT NULL,
                    Stipend REAL NOT NULL,
                    RequiredSkills TEXT NOT NULL,
                    FOREIGN KEY (CompanyId) REFERENCES Companies(CompanyId)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Students (
                    StudentId TEXT PRIMARY KEY,
                    Name TEXT NOT NULL,
                    MobileNumber TEXT NOT NULL,
                    Email TEXT NOT NULL,
                    GPA REAL NOT NULL,
                    Specialization TEXT NOT NULL,
                    Skills TEXT NOT NULL,
                    PreferredLocations TEXT NOT NULL,
                    Password TEXT NOT NULL  -- Ensure Password column exists
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def add_company(self, company):
        try:
            self.cursor.execute("""
                INSERT INTO Companies (
                    CompanyName, Type, Specialty, CommercialRegisterNumber,
                    NumberOfEmployees, Location, TelephoneNumber
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                company.CompanyName, company.Type, company.Specialty,
                company.CommercialRegisterNumber, company.NumberOfEmployees,
                company.Location, company.TelephoneNumber
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding company: {e}")

    def add_opening(self, company_id, opening):
        try:
            # Validate stipend > 0
            if opening.stipend <= 0:
                raise ValueError("Stipend must be a positive number.")

            self.cursor.execute("""
                INSERT INTO Openings (CompanyId, Specialization, Location, Stipend, RequiredSkills)
                VALUES (?, ?, ?, ?, ?)
            """, (
                company_id, opening.specialization, opening.location,
                opening.stipend, ",".join(opening.required_skills)
            ))
            self.conn.commit()
            print("Apprenticeship opening added successfully!")  # Debug confirmation
        except sqlite3.Error as e:
            print(f"Database error adding opening: {e}")
        except ValueError as ve:
            print(f"Validation error: {ve}")

    def add_student(self, student):
        try:
            # Validate GPA between 0 and 5
            if not (0 <= student.gpa <= 5):
                raise ValueError("GPA must be between 0 and 5.")

            self.cursor.execute("""
                INSERT INTO Students (
                    StudentId, Name, MobileNumber, Email, GPA, Specialization, Skills, PreferredLocations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student.student_id, student.name, student.mobile_number, student.email,
                student.gpa, student.specialization, ",".join(student.skills),
                ",".join(student.preferred_locations)
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding student: {e}")
        except ValueError as ve:
            print(f"Validation error: {ve}")

    def match_students_to_openings(self):
        try:
            # Fetch all openings and students
            self.cursor.execute("SELECT * FROM Openings")
            openings = self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM Students")
            students = self.cursor.fetchall()

            matches = []
            for opening in openings:
                opening_id, company_id, specialization, location, stipend, required_skills = opening
                required_skills = set(required_skills.split(","))

                for student in students:
                    student_id, name, mobile, email, gpa, stud_specialization, skills, preferred_locations = student
                    skills = set(skills.split(","))
                    preferred_locations = preferred_locations.split(",")

                    # Check specialization and location match
                    if stud_specialization == specialization and location in preferred_locations:
                        # Check skill overlap
                        if not required_skills.isdisjoint(skills):
                            matches.append({
                                "StudentName": name,
                                "GPA": gpa,
                                "OpeningSpecialization": specialization,
                                "Location": location,
                                "Stipend": stipend
                            })

            # Sort matches by GPA (descending)
            matches.sort(key=lambda x: x["GPA"], reverse=True)
            return matches
        except sqlite3.Error as e:
            print(f"Error matching students to openings: {e}")
            return []
    
    def get_student_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM Students WHERE StudentId = ?", (student_id,))
        return self.cursor.fetchone()
    
    def get_company_by_email(self, email):
        self.cursor.execute("SELECT * FROM Companies WHERE Email = ?", (email,))
        row = self.cursor.fetchone()
        if row:
            return {
                "CompanyId": row[0],
                "CompanyName": row[1],
                "Type": row[2],
                "Specialty": row[3],
                "CommercialRegisterNumber": row[4],
                "NumberOfEmployees": row[5],
                "Location": row[6],
                "TelephoneNumber": row[7],
                "Email": row[8],
                "Password": row[9]
            }
        return None
    
    def get_student_by_email(self, email):
        self.cursor.execute("SELECT * FROM Students WHERE Email = ?", (email,))
        row = self.cursor.fetchone()
        if row:
            return {
                "StudentId": row[0],
                "Name": row[1],
                "MobileNumber": row[2],
                "Email": row[3],
                "GPA": row[4],
                "Specialization": row[5],
                "Skills": row[6],
                "PreferredLocations": row[7],
                "Password": row[8]
            }
        return None