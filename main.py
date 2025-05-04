import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QFormLayout, QMessageBox, QTabWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Company import Company
from Student import Student
from MatchingSystem import MatchingSystem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apprenticeship Matching System")
        self.setGeometry(100, 100, 500, 400)

        # Initialize MatchingSystem
        self.matching_system = MatchingSystem()
        self.matching_system.connect()
        self.matching_system.initialize_db()

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Add buttons for Company and Student
        self.company_button = QPushButton("Company")
        self.student_button = QPushButton("Student")

        self.company_button.clicked.connect(self.show_login_window)
        self.student_button.clicked.connect(self.show_login_window)

        # Add a title label
        self.title_label = QLabel("Welcome to the Apprenticeship Matching System")
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Style the buttons
        self.style_buttons()

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.company_button)
        self.layout.addWidget(self.student_button)

    def style_buttons(self):
        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        self.company_button.setStyleSheet(button_style.replace("#4CAF50", "#008CBA"))
        self.student_button.setStyleSheet(button_style)

    def show_login_window(self):
        sender = self.sender()
        user_type = "Company" if sender == self.company_button else "Student"
        self.login_window = LoginWindow(user_type, self.matching_system)
        self.login_window.show()


class LoginWindow(QWidget):
    def __init__(self, user_type, matching_system):
        super().__init__()
        self.user_type = user_type
        self.matching_system = matching_system
        self.setWindowTitle(f"{user_type} Login/Sign Up")
        self.setGeometry(200, 200, 400, 300)

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tabs for Login and Sign Up
        self.tabs = QTabWidget()
        self.login_tab = QWidget()
        self.signup_tab = QWidget()

        self.tabs.addTab(self.login_tab, "Login")
        self.tabs.addTab(self.signup_tab, "Sign Up")

        # Setup tabs
        self.setup_login_tab()
        self.setup_signup_tab()

        self.layout.addWidget(self.tabs)

    def setup_login_tab(self):
        layout = QFormLayout()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Email:", self.email_input)
        layout.addRow("Password:", self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.login_button)
        self.login_tab.setLayout(layout)

    def setup_signup_tab(self):
        layout = QFormLayout()

        self.inputs = {}
        fields = {
            "Company": ["CompanyName", "Type", "Specialty", "CommercialRegisterNumber", "NumberOfEmployees", "Location", "TelephoneNumber"],
            "Student": ["Name", "MobileNumber", "StudentId", "GPA", "Specialization", "PreferredLocations", "Skills"]
        }

        for field in fields[self.user_type]:
            self.inputs[field] = QLineEdit()
            layout.addRow(field, self.inputs[field])

        # Add Email and Password fields for Sign-Up
        self.email_input_signup = QLineEdit()
        self.password_input_signup = QLineEdit()
        self.password_input_signup.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Email:", self.email_input_signup)
        layout.addRow("Password:", self.password_input_signup)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.signup)

        layout.addWidget(self.signup_button)
        self.signup_tab.setLayout(layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        QMessageBox.information(self, "Success", f"{self.user_type} login successful!")
        if self.user_type == "Company":
            self.show_company_dashboard()
        elif self.user_type == "Student":
            self.show_student_dashboard()

    def signup(self):
        data = {key: input_field.text() for key, input_field in self.inputs.items()}
        email = self.email_input_signup.text()
        password = self.password_input_signup.text()

        if any(not value for value in data.values()) or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if self.user_type == "Company":
            company = Company(
                CompanyId=None,
                CompanyName=data["CompanyName"],
                Type=data["Type"],
                Specialty=data["Specialty"],
                CommercialRegisterNumber=data["CommercialRegisterNumber"],
                NumberOfEmployees=int(data["NumberOfEmployees"]),
                Location=data["Location"],
                TelephoneNumber=data["TelephoneNumber"]
            )
            self.matching_system.add_company(company)
            QMessageBox.information(self, "Success", "Company registered successfully!")

        elif self.user_type == "Student":
            student = Student(
                name=data["Name"],
                mobile_number=data["MobileNumber"],
                email=email,
                student_id=data["StudentId"],
                gpa=float(data["GPA"]),
                specialization=data["Specialization"],
                skills=data["Skills"].split(","),
                preferred_locations=data["PreferredLocations"].split(",")
            )
            self.matching_system.add_student(student)
            QMessageBox.information(self, "Success", "Student registered successfully!")

        self.close()

    def show_company_dashboard(self):
        self.company_dashboard = CompanyDashboard(self.matching_system)
        self.company_dashboard.show()

    def show_student_dashboard(self):
        self.student_dashboard = StudentDashboard(self.matching_system)
        self.student_dashboard.show()


class CompanyDashboard(QWidget):
    def __init__(self, matching_system):
        super().__init__()
        self.matching_system = matching_system
        self.setWindowTitle("Company Dashboard")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Matching Results:")
        self.layout.addWidget(self.label)

        matches = self.matching_system.match_students_to_openings()
        if matches:
            for match in matches:
                self.layout.addWidget(QLabel(f"Student: {match['StudentName']}, GPA: {match['GPA']}"))
        else:
            self.layout.addWidget(QLabel("No matches found."))


class StudentDashboard(QWidget):
    def __init__(self, matching_system):
        super().__init__()
        self.matching_system = matching_system
        self.setWindowTitle("Student Dashboard")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Your Profile:")
        self.layout.addWidget(self.label)


if __name__ == "__main__":
    def handle_exception(exc_type, exc_value, exc_traceback):
        error_message = f"An unexpected error occurred:\n{exc_value}"
        QMessageBox.critical(None, "Error", error_message)

    sys.excepthook = handle_exception  # Override the default exception handler

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Modern style
    window = MainWindow()
    window.show()
    sys.exit(app.exec())