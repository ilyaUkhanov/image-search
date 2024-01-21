from datetime import datetime
from typing import List, Set
from app.Services.DatabaseService import Base

from sqlalchemy import Column, Date, DateTime, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Picture(Base):
    __tablename__ = "picture"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    path = Column(String)
    creation_date = Column(DateTime)
    tags: Mapped[List["Tag"]] = relationship("Tag", back_populates="picture")

    def __init__(self, filename, path, tags):
        self.filename = filename
        self.path = path
        self.tags = tags
        self.creation_date = datetime.today()
    
    def __repr__(self) -> str:
        return f"Picture(id={self.id!r}, filename={self.filename!r}, path={self.path!r})"