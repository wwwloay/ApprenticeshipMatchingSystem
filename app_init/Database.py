import sqlite3


class Database:
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
            if not self.cursor:  # Ensure connection is established
                self.connect()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Companies (
                    CompanyId INTEGER PRIMARY KEY AUTOINCREMENT,
                    CompanyName TEXT NOT NULL,
                    Type TEXT,
                    Specialty TEXT,
                    CommercialRegisterNumber TEXT UNIQUE,
                    NumberOfEmployees INTEGER,
                    Location TEXT,
                    TelephoneNumber TEXT
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
                    PreferredLocations TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            self.close()


# Example usage
if __name__ == "__main__":
    db = Database()
    db.initialize_db()