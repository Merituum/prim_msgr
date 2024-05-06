# messenger_interface.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal
from sqlalchemy.orm import sessionmaker
from models import *

# Tworzenie sesji
Session = sessionmaker(bind=engine)

class MessengerInterface(QWidget):
    messages_changed = pyqtSignal()

    def __init__(self, logged_in_user):
        super().__init__()
        self.logged_in_user = logged_in_user
        self.init_ui()
        self.messages_changed.connect(self.load_messages)

    def init_ui(self):
        # Inicjalizacja interfejsu użytkownika
        self.setWindowTitle("Messenger - prim_msgr")
        self.setGeometry(200, 200, 900, 400)

        layout = QHBoxLayout()

        # Lista użytkowników
        self.list_users = QListWidget()
        layout.addWidget(self.list_users)

        # Pole do wyświetlania wiadomości
        self.txt_message = QTextEdit()
        layout.addWidget(self.txt_message)

        # Pole do wprowadzania tekstu
        self.txt_input = QLineEdit()
        layout.addWidget(self.txt_input)

        # Przycisk do wysyłania wiadomości
        self.btn_send = QPushButton("Send")
        self.btn_send.clicked.connect(self.send_message)
        layout.addWidget(self.btn_send)

        self.setLayout(layout)

    def load_messages(self):
        # Funkcja do wczytywania wiadomości
        session = Session()
        # Tutaj należy dodać logikę wczytywania wiadomości
        session.close()

    def send_message(self):
        # Funkcja do wysyłania wiadomości
        message_content = self.txt_input.text()
        if message_content:
            session = Session()
            # Tutaj należy dodać logikę wysyłania wiadomości
            session.close()
            self.messages_changed.emit()
            self.txt_input.clear()
