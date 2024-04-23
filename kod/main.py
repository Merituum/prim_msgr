import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    #XD TU BYL BŁAD XDD
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), nullable=False)
    haslo = Column(String(100), nullable=False)
    PytaniePomocnicze = Column(String(255), nullable=False)
    OdpowiedzNaPytanie = Column(String(255), nullable=False)

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

       
        # Debugowanie
        # print("Login - Username:", username)
        # print("Login - Password:", password)
        engine = create_engine('mysql+pymysql://root:@localhost/prim_msgr')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        user = session.query(User).filter_by(login=username, haslo=password).first()
        if user:
            def open_main_window(self):
            # Funkcja otwierająca główne okno aplikacji
                self.open_main_window()
            print("Zalogowano!")
            open_main_window(self)

        
        else:
            print("Zly login lub haslo")

    def open_main_window(self):
        #tworzenie tego okna do dashboardu
        self.main_window = MainWindow()
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
        #TODO - FIX NA WPISYWANIE DO BAZY PUSTYCH PÓL
    def register(self):
        # Funkcja obsługująca rejestrację
        new_username = self.txt_new_username.text()
        new_password = self.txt_new_password.text()
        security_question = self.txt_security_question.text()
        security_answer = self.txt_security_answer.text()

        # Połączenie z bazą danych
        # engine = create_engine('postgresql://localhost/prim_msgr')  # Ustawienia dostępu do bazy danych DLA POSTGRESQL
        engine = create_engine('mysql+pymysql://root:@localhost/prim_msgr')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Dodanie użytkownika do bazy danych
        # user = User(Username=new_username, Password=new_password, SecurityQuestion=security_question, SecurityAnswer=security_answer)
        # user = User(Login=new_username, Haslo=new_password, PytaniePomocnicze=security_question, OdpowiedzNaPytanie=security_answer)
        user = User(login=new_username, haslo=new_password, PytaniePomocnicze=security_question, OdpowiedzNaPytanie=security_answer)
        session.add(user)
        session.commit()

        print("User registered successfully!")
    
    # def LoginToApp(self):
    #     username = self.txt_username.text()
    #     haslo = self.txt_password.text()


#KLASA DO DASHBOARDU
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.lbl_welcome = QLabel("Witamy w prim_msgr!")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_welcome, alignment=Qt.AlignTop)
        self.layout.addWidget(QPushButton("Wyloguj", clicked=self.logout))
        self.setLayout(self.layout)
        self.setWindowTitle("Dashboard - prim_msgr")
        self.setGeometry(200, 200, 300, 150)
    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
    

        


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
