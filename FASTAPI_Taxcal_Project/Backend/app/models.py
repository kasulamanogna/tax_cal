from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    incomes = relationship("IncomeEntry", back_populates="owner")
    tax_histories = relationship("TaxHistory", back_populates="user")

class IncomeEntry(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    regime = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="incomes")

class TaxHistory(Base):
    __tablename__ = "tax_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    year = Column(Integer)
    total_income = Column(Float)
    tax_paid = Column(Float)
    user = relationship("User", back_populates="tax_histories")