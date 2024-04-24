from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTextEdit, QLineEdit, QPushButton

# Połączenie z bazą danych
engine = create_engine('mysql+pymysql://root:@localhost/prim_msgr')
Base = declarative_base()

# Definicja modelu użytkownika
class User(Base):
    __tablename__ = 'Users'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Login = Column(String(50), nullable=False)
    Haslo = Column(String(100), nullable=False)
    PytaniePomocnicze = Column(String(255), nullable=False)
    OdpowiedzNaPytanie = Column(String(255), nullable=False)

    sent_messages = relationship('Message', back_populates='sender', foreign_keys='Message.ID_wysylajacego')
    received_messages = relationship('Message', back_populates='receiver', foreign_keys='Message.ID_odbierajacego')

# Definicja modelu wiadomości
class Message(Base):
    __tablename__ = 'Wiadomosci'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_wysylajacego = Column(Integer, ForeignKey('Users.ID'), nullable=False)
    ID_odbierajacego = Column(Integer, ForeignKey('Users.ID'), nullable=False)
    content = Column(String(255), nullable=False)

    sender = relationship('User', foreign_keys=[ID_wysylajacego], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[ID_odbierajacego], back_populates='received_messages')

# Inicjalizacja bazy danych
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class MessengerInterface(QWidget):
    def __init__(self, logged_in_user):
        super().__init__()
        self.logged_in_user = logged_in_user
        self.init_ui()

    def init_ui(self):
        self.lista_users = QListWidget()
        self.txt_message = QTextEdit()
        self.txt_input = QLineEdit()
        self.selected_user = None

        main_layout = QHBoxLayout()

        # Układ dla listy użytkowników
        users_layout = QVBoxLayout()
        users_layout.addWidget(QLabel("Lista użytkowników"))
        users_layout.addWidget(self.lista_users)

        # Układ dla pola wiadomości
        messages_layout = QVBoxLayout()
        messages_layout.addWidget(QLabel("Wiadomości"))
        messages_layout.addWidget(self.txt_message)

        # Układ dla pola wpisywania wiadomości
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.txt_input)
        input_layout.addWidget(QPushButton("Wyślij", clicked=self.send_message))

        main_layout.addLayout(users_layout)
        main_layout.addLayout(messages_layout)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

        self.setWindowTitle("Messenger - prim_msgr")
        self.setGeometry(200, 200, 400, 400)

        # Wczytaj użytkowników z bazy danych i dodaj ich do listy
        self.load_users_from_database()

        # Połącz zdarzenie zaznaczenia użytkownika z funkcją obsługi
        self.lista_users.itemClicked.connect(self.select_user)

    def load_users_from_database(self):
        session = Session()
        users = session.query(User).filter(User.Login != self.logged_in_user.Login).all()
        for user in users:
            self.lista_users.addItem(user.Login)

    def select_user(self, item):
        # Zapisz zaznaczonego użytkownika
        self.selected_user = item.text()

    def send_message(self):
       # Sprawdź, czy użytkownik został wybrany
        if self.selected_user:
        # Pobierz treść wiadomości
            message_content = self.txt_input.text()
            if message_content:
                session = Session()
                receiver = session.query(User).filter_by(Login=self.selected_user).first()

                if receiver:
                    message = Message(ID_wysylajacego=self.logged_in_user.ID, ID_odbierajacego=receiver.ID, content=message_content)
                    session.add(message)
                
                # Wydrukowanie zapytania SQL
                    print(f"SQL: {session.query(Message).filter_by(ID_wysylajacego=self.logged_in_user.ID, ID_odbierajacego=receiver.ID, content=message_content).statement}")
                
                    session.commit()
                    print(f"Wysłano wiadomość do użytkownika {self.selected_user}: {message_content}")
                # Wyczyść pole wpisywania wiadomości
                    self.txt_input.clear()
                else:
                    print("Nie znaleziono odbiorcy.")
            else:
                print("Nie można wysłać pustej wiadomości.")
        else:
            print("Proszę wybrać użytkownika, aby wysłać wiadomość.")

class MainWindow(QWidget):
    def __init__(self, logged_in_user):
        super().__init__()
        self.logged_in_user = logged_in_user
        self.init_ui()

    def init_ui(self):
        self.lbl_welcome = QLabel(f"Witamy w prim_msgr, {self.logged_in_user.Login}!")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_welcome)
        self.layout.addWidget(QPushButton("Wyloguj", clicked=self.logout))

        # Utworzenie interfejsu Messenger
        self.messenger_interface = MessengerInterface(self.logged_in_user)

        # Ustawienie układu dla głównego okna
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.messenger_interface)
        self.setLayout(main_layout)

        self.setWindowTitle("Dashboard - prim_msgr")
        self.setGeometry(200, 200, 600, 400)

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Tworzenie etykiet, pól tekstowych, przycisków logowania i rejestracji
        self.lbl_username = QLabel("Username:")
        self.lbl_password = QLabel("Password:")
        self.txt_username = QLineEdit()
        self.txt_password = QLineEdit()
        self.btn_login = QPushButton("Login")
        self.btn_register = QPushButton("Register")

        # Ustawienie pola hasła na tryb hasła
        self.txt_password.setEchoMode(QLineEdit.Password)

        # Ustawienie układu dla przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_login)
        button_layout.addWidget(self.btn_register)

        # Ustawienie układu dla etykiet, pól tekstowych i przycisków
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_username)
        self.layout.addWidget(self.txt_username)
        self.layout.addWidget(self.lbl_password)
        self.layout.addWidget(self.txt_password)
        self.layout.addLayout(button_layout)

        # Ustawienie głównego układu okna
        self.setLayout(self.layout)

        # Połączenie przycisków z funkcjami obsługującymi logowanie i rejestrację
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_registration_fields)

        # Ustawienia okna
        self.setWindowTitle("Login Window")
        self.setGeometry(200, 200, 300, 150)

    def login(self):
        # Funkcja obsługująca logowanie
        username = self.txt_username.text()
        password = self.txt_password.text()

        session = Session()
        user = session.query(User).filter_by(Login=username, Haslo=password).first()
        if user:
            self.open_main_window(user)
            print("Zalogowano!")
        else:
            print("Zły login lub hasło")

    def open_main_window(self, user):
        self.main_window = MainWindow(user)
        self.main_window.show()
        self.close()

    def show_registration_fields(self):
        # Funkcja wyświetlająca pola rejestracji po naciśnięciu przycisku rejestracji
        # Ukrycie etykiet i pól logowania
        self.lbl_username.hide()
        self.lbl_password.hide()
        self.txt_username.hide()
        self.txt_password.hide()
        self.btn_login.hide()
        self.btn_register.hide()

        # Stworzenie nowych pól rejestracji
        self.lbl_new_username = QLabel("New Username:")
        self.lbl_new_password = QLabel("New Password:")
        self.lbl_security_question = QLabel("Security Question:")
        self.lbl_security_answer = QLabel("Security Answer:")
        self.txt_new_username = QLineEdit()
        self.txt_new_password = QLineEdit()
        self.txt_security_question = QLineEdit()
        self.txt_security_answer = QLineEdit()
        self.btn_register_confirm = QPushButton("Register")

        # Ustawienie pola nowego hasła na tryb hasła
        self.txt_new_password.setEchoMode(QLineEdit.Password)
        self.txt_security_answer.setEchoMode(QLineEdit.Password)

        # Dodanie pól rejestracji do głównego układu
        self.layout.addWidget(self.lbl_new_username)
        self.layout.addWidget(self.txt_new_username)
        self.layout.addWidget(self.lbl_new_password)
        self.layout.addWidget(self.txt_new_password)
        self.layout.addWidget(self.lbl_security_question)
        self.layout.addWidget(self.txt_security_question)
        self.layout.addWidget(self.lbl_security_answer)
        self.layout.addWidget(self.txt_security_answer)
        self.layout.addWidget(self.btn_register_confirm)

        # Połączenie przycisku z funkcją obsługującą rejestrację
        self.btn_register_confirm.clicked.connect(self.register)

    def register(self):
        # Funkcja obsługująca rejestrację
        new_username = self.txt_new_username.text()
        new_password = self.txt_new_password.text()
        security_question = self.txt_security_question.text()
        security_answer = self.txt_security_answer.text()

        session = Session()
        user = User(Login=new_username, Haslo=new_password, PytaniePomocnicze=security_question, OdpowiedzNaPytanie=security_answer)
        session.add(user)
        session.commit()

        print("User registered successfully!")

if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()
