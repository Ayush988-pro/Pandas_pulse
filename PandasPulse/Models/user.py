from operator import index

from pydantic import BaseModel
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    email = Column(String(255),unique=True)
    password = Column(String(255))

class UserCreate(BaseModel):
    email: str
    password: str
