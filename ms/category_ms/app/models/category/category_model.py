from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String

@dataclass
class Category(db.Model):
    __tablename__ = 'categories'
    category_id: int = Column(Integer, primary_key=True, autoincrement=True)
    time_category: str = Column(String(50), nullable=False)
    tyre_type: str = Column(String(50), nullable=False)
    gender: str = Column(String(50), nullable=False)