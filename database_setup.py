import sys

from sqlalchemy                 import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import relationship
from sqlalchemy                 import create_engine

# creates instance of declarative base
Base = declarative_base()

class Category(Base):
  __tablename__ = 'categories'

  name = Column(String(80), nullable=False, unique=True)
  id   = Column(Integer, primary_key = True)

class Item(Base):
  __tablename__   = 'items'

  name          = Column(String(80), nullable=False, primary_key=True)
  description   = Column(String(250))
  id            = Column(Integer)
  category_id = Column(Integer, ForeignKey('categories.id'), primary_key = True)
  category = relationship(Category)

# create database and add tables and columns
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.create_all(engine)
