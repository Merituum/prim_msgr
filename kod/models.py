# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('mysql+pymysql://root:@localhost/prim_msgr')
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Login = Column(String(50), nullable=False)
    Haslo = Column(String(100), nullable=False)
    PytaniePomocnicze = Column(String(255), nullable=False)
    OdpowiedzNaPytanie = Column(String(255), nullable=False)

    sent_messages = relationship('Message', back_populates='sender', foreign_keys='Message.ID_wysylajacego')
    received_messages = relationship('Message', back_populates='receiver', foreign_keys='Message.ID_odbierajacego')

class Message(Base):
    __tablename__ = 'Wiadomosci'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_wysylajacego = Column(Integer, ForeignKey('Users.ID'), nullable=False)
    ID_odbierajacego = Column(Integer, ForeignKey('Users.ID'), nullable=False)
    content = Column(String(255), nullable=False)

    sender = relationship('User', foreign_keys=[ID_wysylajacego], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[ID_odbierajacego], back_populates='received_messages')
