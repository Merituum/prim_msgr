from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from PyQt5.QtWidgets import QApplication,QSizePolicy,QMessageBox, QWidget,QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal
import qtmodern.styles
# qtmodern.styles.dark(app)

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
    messages_changed = pyqtSignal()

    def __init__(self, logged_in_user):
        super().__init__()
        self.logged_in_user = logged_in_user
        self.init_ui()
        self.messages_changed.connect(self.load_messages)

    def init_ui(self):
        self.lista_users = QListWidget()
        self.txt_message = QTextEdit()
        self.txt_input = QLineEdit()
        self.selected_user = None

        main_layout = QHBoxLayout()

        # Układ dla listy użytkowników
        users_layout = QVBoxLayout()
        users_layout.addWidget(QLabel("Zalogowano jako " + self.logged_in_user.Login))
        users_layout.addWidget(QLabel("Lista użytkowników"))
        users_layout.addWidget(self.lista_users)
        self.lista_users.setMaximumWidth(150)  # Ustaw maksymalną szerokość listy użytkowników

        # Układ dla pola wiadomości
        messages_layout = QVBoxLayout()
        messages_layout.addWidget(QPushButton("Wyloguj",clicked=self.logout))
        messages_layout.addWidget(QLabel("Wiadomości"))
        messages_layout.addWidget(self.txt_message)
        self.txt_message.setMaximumWidth(400)  # Ustaw maksymalną szerokość pola wiadomości

        # Układ dla pola wpisywania wiadomości
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.txt_input)
        self.txt_input.setPlaceholderText("Wpisz wiadomość...")
        self.txt_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.txt_input.setMinimumHeight(720)  # Ustaw maksymalną szerokość pola do wpisywania wiadomości
        self.txt_input.setMinimumWidth(200)  # Ustaw minimalną szerokość pola do wpisywania wiadomości
        input_layout.addWidget(QPushButton("Wyślij", clicked=self.send_message))

        main_layout.addLayout(users_layout)
        main_layout.addLayout(messages_layout)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

        self.setWindowTitle("Messenger - prim_msgr")
        self.setGeometry(200, 200, 900, 400)

        # Wczytaj użytkowników z bazy danych i dodaj ich do listy
        self.load_users_from_database()

        # Połącz zdarzenie zaznaczenia użytkownika z funkcją obsługi
        self.lista_users.itemClicked.connect(self.select_user)
    def logout(self):
        # self.main_window.close()
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
        # self.main_window=MainWindow()
        # self.main_window.hide()
    def load_users_from_database(self):
        session = Session()
        users = session.query(User).filter(User.Login != self.logged_in_user.Login).all()
        for user in users:
            self.lista_users.addItem(user.Login)

    def select_user(self, item):
        # Zapisz zaznaczonego użytkownika
        self.selected_user = item.text()
        self.messages_changed.emit()

    def load_messages(self):
        if self.selected_user:
            session = Session()
            receiver = session.query(User).filter_by(Login=self.selected_user).first()
            if receiver:
                messages = session.query(Message).filter_by(ID_wysylajacego=self.logged_in_user.ID, ID_odbierajacego=receiver.ID).all()
                messages += session.query(Message).filter_by(ID_wysylajacego=receiver.ID, ID_odbierajacego=self.logged_in_user.ID).all()
                messages.sort(key=lambda x: x.ID)
                self.txt_message.setPlainText("\n".join([f"{message.sender.Login}: {message.content}" for message in messages]))
            else:
                print("Nie znaleziono odbiorcy.")
        else:
            print("Proszę wybrać użytkownika, aby zobaczyć wiadomości.")

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
                    self.messages_changed.emit()
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
        # self.layout.addWidget(QPushButton("Wyloguj", clicked=self.logout))

        # Utworzenie interfejsu Messenger
        self.messenger_interface = MessengerInterface(self.logged_in_user)

        # Ustawienie układu dla głównego okna
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.messenger_interface)
        self.setLayout(main_layout)

        self.setWindowTitle("Dashboard - prim_msgr")
        self.setGeometry(200, 200, 1600, 800)

    

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        qtmodern.styles.dark(app)
        # Tworzenie etykiet, pól tekstowych, przycisków logowania i rejestracji
        self.lbl_username = QLabel("Login:")
        self.lbl_password = QLabel("Hasło:")
        self.txt_username = QLineEdit()
        self.txt_password = QLineEdit()
        self.btn_login = QPushButton("Login")
        self.btn_register = QPushButton("Register")
        self.btn_forgot_password = QPushButton("Zapomniałeś hasła?")

        # Ustawienie pola hasła na tryb hasła
        self.txt_password.setEchoMode(QLineEdit.Password)

        # Ustawienie układu dla przycisków
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_login)
        button_layout.addWidget(self.btn_register)
        button_layout.addWidget(self.btn_forgot_password)

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
        self.btn_forgot_password.clicked.connect(self.show_forgot_password_fields)

        # Ustawienia okna
        self.setWindowTitle("Login Window")
        self.setGeometry(200, 200, 300, 150)
    def show_forgot_password_fields(self):
        self.forgot_password_window = ForgotPassword()
        self.forgot_password_window.show()
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
        #PRZEKAZANA REFERENCJA DO OKNA LOGOWANIA
        # self.main_window.login_window=self
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
        self.lbl_new_username = QLabel("Login:")
        self.lbl_new_password = QLabel("Hasło:")
        self.lbl_security_question = QLabel("Pytanie awaryjne:")
        self.lbl_security_answer = QLabel("Odpowiedź na pytanie:")
        self.txt_new_username = QLineEdit()
        self.txt_new_password = QLineEdit()
        self.txt_security_question = QLineEdit()
        self.txt_security_answer = QLineEdit()
        self.btn_register_confirm = QPushButton("Zarejestruj się")

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
        if not new_username or not new_password or not security_question or not security_answer:
            msg=QMessageBox()
            msg.setWindowTitle("Puste pola!")
            msg.setText("Wszystkie pola muszą być wypełnione!")
            msg.exec()
            return
        
        session = Session()
        
        existing = session.query(User).filter_by(Login=new_username).first()
        
        if existing:
            msg=QMessageBox()
            msg.setWindowTitle("Kradniesz nick!")
            msg.setText("Taki login już istnieje!")
            msg.exec()
            return
        user = User(Login=new_username, Haslo=new_password, PytaniePomocnicze=security_question, OdpowiedzNaPytanie=security_answer)
        session.add(user)
        session.commit()
        self.close()
        self.open_main_window(user)
        print("User registered successfully!")
class ForgotPassword(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.lbl_username = QLabel("Login")
        self.txt_username = QLineEdit()
        self.btn_confirm = QPushButton("Potwierdź")
        self.lbl_security_question = QLabel()
        self.txt_security_answer = QLineEdit()
        self.btn_confirm_answer = QPushButton("Potwierdź odpowiedź")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_username)
        self.layout.addWidget(self.txt_username)
        self.layout.addWidget(self.btn_confirm)
        self.layout.addWidget(self.lbl_security_question)
        self.layout.addWidget(self.txt_security_answer)
        self.layout.addWidget(self.btn_confirm_answer)

        self.setLayout(self.layout)

        self.btn_confirm.clicked.connect(self.confirm_username)
        self.btn_confirm_answer.clicked.connect(self.confirm_answer)

    def confirm_username(self):
        username = self.txt_username.text()
        session = Session()
        user = session.query(User).filter_by(Login=username).first()
        if user:
            self.lbl_security_question.setText(user.PytaniePomocnicze)
        else:
            self.lbl_security_question.setText("User not found.")

    def confirm_answer(self):
        username = self.txt_username.text()
        answer = self.txt_security_answer.text()
        session = Session()
        user = session.query(User).filter_by(Login=username).first()
        if user and user.OdpowiedzNaPytanie == answer:
            self.lbl_security_question.setText("Password reset successful.")
        else:
            self.lbl_security_question.setText("Incorrect answer.")

if __name__ == '__main__':
    # qtmodern.styles.dark(app)
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()
