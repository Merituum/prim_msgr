# forgot_password_window.py
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from models import User, Session

class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.lbl_username = QLabel("Username:")
        self.txt_username = QLineEdit()
        session = Session()
        user = session.query(User).filter_by(Login=self.txt_username.text()).first()
        self.setWindowTitle("Zapomniałeś hasła?")
        #Zapytanie -> jezeli istnieje user o podanym nicku, to zwraca pytanie pomocnicze
        if user:
            security_question = user.PytaniePomocnicze
            self.txt_security_question.setText(security_question)
            security_answer = self.txt_sqcurity_answer.text()
            if user.OdpowiedzNaPytanie == security_answer:
                self.lbl_new_password = QLabel("New Password:")
                self.txt_new_password = QLineEdit()
                self.btn_confirm = QPushButton("Confirm")
                self.layout.addWidget(self.lbl_new_password)
                self.layout.addWidget(self.txt_new_password)
                self.layout.addWidget(self.btn_confirm)
                self.btn_confirm.clicked.connect(self.change_password)
            else:
                print("Zła odpowiedź na pytanie pomocnicze")
                QLabel("Zła odpowiedź na pytanie pomocnicze")
        else:
            print("Nie ma takiego użytkownika")
            QLabel("Nie ma takiego użytkownika")

