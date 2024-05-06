# login_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from main_window import MainWindow
from models import Session, User

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Inicjalizacja interfejsu logowania
        self.setWindowTitle("Login Window")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.lbl_username = QLabel("Username:")
        layout.addWidget(self.lbl_username)
        self.txt_username = QLineEdit()
        layout.addWidget(self.txt_username)

        self.lbl_password = QLabel("Password:")
        layout.addWidget(self.lbl_password)
        self.txt_password = QLineEdit()
        layout.addWidget(self.txt_password)

        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def login(self):
        # Funkcja obsługująca logowanie
        username = self.txt_username.text()
        password = self.txt_password.text()

        session = Session()
        user = session.query(User).filter_by(Login=username, Haslo=password).first()
        session.close()

        if user:
            self.open_main_window(user)
            print("Zalogowano!")
        else:
            print("Zły login lub hasło")

    def open_main_window(self, user):
        self.main_window = MainWindow(user)
        self.main_window.show()
        self.close()
