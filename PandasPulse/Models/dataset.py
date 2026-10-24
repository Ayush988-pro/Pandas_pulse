from sqlalchemy import (Column, Integer, String, Date, ForeignKey)
from Models.user import Base

class Dataset(Base):
    __tablename__ = "dataset"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    file_path = Column(String(500))
    owner_id = Column(Integer, ForeignKey("user.id"))
