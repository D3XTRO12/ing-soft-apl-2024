from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
