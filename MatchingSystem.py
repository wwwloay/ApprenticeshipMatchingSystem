import sqlite3
from Company import Company
from Student import Student


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
                    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    kind TEXT,
                    specialty TEXT,
                    commercial_register_number TEXT UNIQUE,
                    number_of_employees INTEGER,
                    location TEXT,
                    telephone_number TEXT,
                    email TEXT UNIQUE,  -- Ensure email column exists
                    password TEXT       -- Ensure password column exists
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS openings (
                    OpeningId INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    specialization TEXT NOT NULL,
                    location TEXT NOT NULL,
                    Stipend REAL NOT NULL,
                    RequiredSkills TEXT NOT NULL,
                    FOREIGN KEY (company_id) REFERENCES Companies(company_id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    mobile_number TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    gpa REAL NOT NULL,
                    specialization TEXT NOT NULL,
                    skills TEXT NOT NULL,
                    preferred_locations TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def add_company(self, company):
        try:

            self.cursor.execute("""
                INSERT INTO Companies (
                    company_name, kind, specialty, commercial_register_number,
                    number_of_employees, location, telephone_number,
                    email,
                    password
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company.company_name, company.kind, company.specialty,
                company.commercial_register_number, company.number_of_employees,
                company.location, company.telephone_number,
                company.email,  # Include the email
                company.password  # Include the password
            ))
            self.conn.commit()
            print("Company added successfully!")  # Debug confirmation

        except sqlite3.Error as e:
            print(f"Error adding company: {e}")

    def add_opening(self, company_id, opening):
        try:
            # Validate stipend > 0
            if opening.stipend <= 0:
                raise ValueError("Stipend must be a positive number.")

            self.cursor.execute("""
                INSERT INTO openings (company_id, specialization, location, Stipend, RequiredSkills)
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
            # Validate gpa between 0 and 5
            if not (0 <= student.gpa <= 5):
                raise ValueError("gpa must be between 0 and 5.")

            self.cursor.execute("""
                INSERT INTO Students (
                    student_id, name, mobile_number, email, password, gpa, specialization, skills, preferred_locations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student.student_id, student.name, student.mobile_number, student.email, student.password,
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
            self.cursor.execute("SELECT * FROM openings")
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
                                "gpa": gpa,
                                "OpeningSpecialization": specialization,
                                "location": location,
                                "Stipend": stipend
                            })

            # Sort matches by gpa (descending)
            matches.sort(key=lambda x: x["gpa"], reverse=True)
            return matches
        except sqlite3.Error as e:
            print(f"Error matching students to openings: {e}")
            return []
    
    def get_student_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()
    
    def get_company_by_email(self, email):
        self.cursor.execute("SELECT * FROM Companies WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        # print(row)  # Debugging line to check the fetched row
        if row:
            return {
                "company_id": row[0],
                "company_name": row[1],
                "kind": row[2],
                "specialty": row[3],
                "commercial_register_number": row[4],
                "number_of_employees": row[5],
                "location": row[6],
                "telephone_number": row[7],
                "email": row[8],
                "password": row[9]
            }
        return None
    
    def get_student_by_email(self, email):
        self.cursor.execute("SELECT * FROM Students WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        if row:
            return {
                "student_id": row[0],
                "name": row[1],
                "mobile_number": row[2],
                "email": row[3],
                "password": row[4],
                "gpa": row[5],
                "specialization": row[6],
                "skills": row[7],
                "preferred_locations": row[8]
            }
        return None

    def get_openings_by_company_id(self, company_id):
        self.cursor.execute("SELECT * FROM openings WHERE company_id = ?", (company_id,))
        rows = self.cursor.fetchall()
        return [
            {
                "opening_id": row[0],
                "company_id": row[1],
                "specialization": row[2],
                "location": row[3],
                "stipend": row[4],
                "required_skills": row[5]
            }
            for row in rows
        ]

    def get_all_openings(self):
        self.cursor.execute("SELECT * FROM openings")
        rows = self.cursor.fetchall()
        return [
            {
                "opening_id": row[0],
                "company_id": row[1],
                "specialization": row[2],
                "location": row[3],
                "stipend": row[4],
                "required_skills": row[5]
            }
            for row in rows
        ]

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM Students")
        rows = self.cursor.fetchall()
        return [
            {
                "student_id": row[0],
                "name": row[1],
                "mobile_number": row[2],
                "email": row[3],
                "password": row[4],
                "gpa": row[5],
                "specialization": row[6],
                "skills": row[7],
                "preferred_locations": row[8]
            }
            for row in rows
        ]