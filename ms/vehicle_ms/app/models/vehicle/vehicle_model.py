from dataclasses import dataclass
from app import db
from sqlalchemy import Column, Integer, String

@dataclass
class Vehicle(db.Model):
    __tablename__ = 'Vehicle'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    time: str = Column(String(250))
    tyre_type: str = Column(String(250))
    fuel: str = Column(String(250))
    bodywork: str = Column(String(250))