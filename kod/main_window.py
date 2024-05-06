from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from messenger_interface import MessengerInterface
class MainWindow(QWidget):
    def __init__(self, logged_in_user):
        super().__init__()
        self.logged_in_user = logged_in_user
        self.init_ui()
    
    def init_ui(self):
        self.lbl_welcome = QLabel(f"Witamy w prim_msgr, {self.logged_in_user.Login}!")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_welcome)
        # self.layout.addWidget(QPushButton("Wyloguj", clicked=self.logout))

        # Utworzenie interfejsu Messenger
        self.messenger_interface = MessengerInterface(self.logged_in_user)

        # Ustawienie układu dla głównego okna
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.messenger_interface)
        self.setLayout(main_layout)

        self.setWindowTitle("Dashboard - prim_msgr")
        self.setGeometry(200, 200, 1600, 900)
