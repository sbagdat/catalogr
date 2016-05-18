import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# creates instance of declarative base
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer)
    name = Column(String(250), nullable=False, primary_key=True)
    description = Column(String(750), nullable=False)
    category_id = Column(
        Integer, ForeignKey('categories.id'), primary_key=True)
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)


# create database and add tables and columns
engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.create_all(engine)
