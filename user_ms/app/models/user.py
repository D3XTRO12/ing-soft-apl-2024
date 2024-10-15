from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50))
    dni: str = Column(String(10))
    email: str = Column(String(50))
    gender: str = Column(String(1))
    age: int = Column(Integer)
    address: str = Column(String(100))
    phone: str = Column(String(9))
    role: str = Column(String(20))
