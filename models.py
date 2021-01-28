from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.sql.expression import func
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    login_id = Column(String(36), nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
        
    def get_id(self):
        return self.login_id

class Topic(Base):
    __tablename__ = "topic"
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    description = Column(String(80), nullable=False)

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id'), nullable=False)
    username = Column(String(30), nullable=False)
    data = Column(DateTime, default=datetime.now)
    content = Column(String(80), nullable=False)
