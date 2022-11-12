from sqlalchemy import Column, VARCHAR, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from constants import ENGINE

engine = ENGINE
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    telegram_id = Column(INTEGER(unsigned=True), nullable=False)
    username = Column(VARCHAR(32), nullable=True)
    tasks = relationship('Task', back_populates="users")


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    name = Column(Text(255), nullable=False)
    description = Column(Text(255))
    deadline = Column(DateTime)
    is_completed = Column(Boolean, nullable=False)
    user_id = Column(INTEGER(unsigned=True), ForeignKey(User.id), nullable=False)
    users = relationship('User', back_populates="tasks")


Base.metadata.create_all(ENGINE)
