from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///tasks-sqlalchemy.db', echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)


class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(50))
    description = Column(String(300))
    deadline = Column(Integer)
    User = relationship('User')


Base.metadata.create_all(engine)
