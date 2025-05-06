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
                    email TEXT UNIQUE,
                    password TEXT
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
                    email, password
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company.company_name, company.kind, company.specialty,
                company.commercial_register_number, company.number_of_employees,
                company.location, company.telephone_number,
                company.email, company.password
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding company: {e}")

    def add_student(self, student):
        try:
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

    def get_company_by_email(self, email):
        self.cursor.execute("SELECT * FROM Companies WHERE email = ?", (email,))
        row = self.cursor.fetchone()
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
    
    def get_student_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
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