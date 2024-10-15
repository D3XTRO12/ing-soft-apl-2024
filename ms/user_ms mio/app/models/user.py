from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    dni = Column(String(10))
    email = Column(String(50))
    gender = Column(String(1))
    age = Column(Integer)
    address = Column(String(100))
    phone = Column(String(9))
    role = Column(String(20))
