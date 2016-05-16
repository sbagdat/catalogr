import sys

from sqlalchemy                 import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import relationship
from sqlalchemy                 import create_engine

# creates instance of declarative base
Base = declarative_base()

class Category(Base):
  __tablename__ = 'categories'

  name = Column(String(80), nullable=False)
  id   = Column(Integer, primary_key = True)

class Item(Base):
  __tablename__   = 'items'

  name          = Column(String(80), nullable=False)
  description   = Column(String(250))
  price         = Column(String(8))
  id            = Column(Integer, primary_key = True)
  category_id = Column(Integer, ForeignKey('categories.id'))
  category = relationship(Category)

# create database and add tables and columns
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.create_all(engine)
