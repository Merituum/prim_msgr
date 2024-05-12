from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from PyQt5.QtWidgets import QApplication,QDialog,QDialogButtonBox,QSizePolicy,QMessageBox, QWidget,QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTextEdit, QLineEdit, QPushButton
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
messages_changed = pyqtSignal()
class MessengerApp(QWidget):
    def __init__(self, logged_in_user):
        super().__init__()
        self.logged_in_user = logged_in_user
        self.selected_user = None
        self.init_ui()

    def init_ui(self):
        self.lbl_welcome = QLabel(f"Witamy w prim_msgr, {self.logged_in_user.Login}!")
        self.lista_users = QListWidget()
        self.txt_message = QTextEdit()
        self.txt_input = QLineEdit()

        main_layout = QHBoxLayout()

        # Układ dla listy użytkowników
        users_layout = QVBoxLayout()
        users_layout.addWidget(QLabel("Zalogowano jako " + self.logged_in_user.Login))
        users_layout.addWidget(QLabel("Lista użytkowników"))
        users_layout.addWidget(self.lista_users)
        self.lista_users.setMaximumWidth(150)  # Ustaw maksymalną szerokość listy użytkowników
        main_layout.addLayout(users_layout)

        # Układ dla pola wiadomości
        messages_layout = QVBoxLayout()
        messages_layout.addWidget(QPushButton("Wyloguj", clicked=self.logout))
        messages_layout.addWidget(QLabel("Wiadomości"))
        messages_layout.addWidget(self.txt_message)
        self.txt_message.setMaximumWidth(400)  # Ustaw maksymalną szerokość pola wiadomości
        main_layout.addLayout(messages_layout)

        # Układ dla pola wpisywania wiadomości
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.txt_input)
        self.txt_input.setPlaceholderText("Wpisz wiadomość...")
        self.txt_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.txt_input.setMinimumHeight(720)  # Ustaw maksymalną szerokość pola do wpisywania wiadomości
        self.txt_input.setMinimumWidth(200)  # Ustaw minimalną szerokość pola do wpisywania wiadomości
        input_layout.addWidget(QPushButton("Wyślij", clicked=self.send_message))

        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Dashboard - prim_msgr")
        self.setGeometry(200, 200, 1600, 800)

        # Wczytaj użytkowników z bazy danych i dodaj ich do listy
        self.load_users_from_database()

        # Połącz zdarzenie zaznaczenia użytkownika z funkcją obsługi
        self.lista_users.itemClicked.connect(self.select_user)

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

    def load_users_from_database(self):
        session = Session()
        users = session.query(User).filter(User.Login != self.logged_in_user.Login).all()
        for user in users:
            self.lista_users.addItem(user.Login)

    def select_user(self, item):
        # Zapisz zaznaczonego użytkownika
        self.selected_user = item.text()
        self.load_messages()

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
        if self.selected_user:
            message_content = self.txt_input.text()
            if message_content:
                session = Session()
                receiver = session.query(User).filter_by(Login=self.selected_user).first()
                if receiver:
                    message = Message(ID_wysylajacego=self.logged_in_user.ID, ID_odbierajacego=receiver.ID, content=message_content)
                    session.add(message)
                    session.commit()
                    print(f"Wysłano wiadomość do użytkownika {self.selected_user}: {message_content}")
                    self.txt_input.clear()
                    self.load_messages()
                else:
                    print("Nie znaleziono odbiorcy.")
            else:
                print("Nie można wysłać pustej wiadomości.")
        else:
            print("Proszę wybrać użytkownika, aby wysłać wiadomość.")


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
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
        self.main_window = MessengerApp(user)
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
        if not username:
            QMessageBox.warning(self, "Błąd", "Proszę podać login.")
            return
       
        session = Session()
        user = session.query(User).filter_by(Login=username).first()
        if user:
            self.lbl_security_question.setText(user.PytaniePomocnicze)
        else:
            QMessageBox.warning(self, "Błąd", "Nie znaleziono użytkownika.")

    def confirm_answer(self):
        username = self.txt_username.text()
        answer = self.txt_security_answer.text()
        if not answer:
            QMessageBox.warning(self, "Błąd", "Proszę podać odpowiedź.")
            return
        session = Session()
        user = session.query(User).filter_by(Login=username).first()
        if user and user.OdpowiedzNaPytanie == answer:
            # self.lbl_security_question.setText("Password reset successful.")
            
            self.reset_password_dialog = ResetPasswordDialog(username)
            self.reset_password_dialog.exec_()
        else:
            self.lbl_security_question.setText("Incorrect answer.")
class ResetPasswordDialog(QDialog):
    def __init__(self, username, parent=None):
        super(ResetPasswordDialog, self).__init__(parent)
        self.username = username
        self.setWindowTitle("Resetowanie hasła")
        self.lbl_new_password = QLabel("Nowe hasło:")
        self.txt_new_password = QLineEdit()
        self.btn_reset_password = QPushButton("Zresetuj hasło")
        self.btn_cancel = QPushButton("Anuluj")

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_new_password)
        layout.addWidget(self.txt_new_password)
        buttons = QDialogButtonBox()
        buttons.addButton(self.btn_reset_password, QDialogButtonBox.ActionRole)
        buttons.addButton(self.btn_cancel, QDialogButtonBox.RejectRole)
        layout.addWidget(buttons)
        self.setLayout(layout)

        self.btn_reset_password.clicked.connect(self.reset_password)
        self.btn_cancel.clicked.connect(self.reject)

    def reset_password(self):
        new_password = self.txt_new_password.text()

        if not new_password:
            QMessageBox.warning(self, "Błąd", "Proszę wprowadzić nowe hasło.")
            return

        
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(Login=self.username).first()
        user.Haslo = new_password
        session.commit()
        
        session.commit()
        QMessageBox.information(self, "Sukces", "Hasło zostało zresetowane pomyślnie.")
        self.accept()
if __name__ == '__main__':
    # qtmodern.styles.dark(app)
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()