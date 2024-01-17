from typing import List
from typing import Optional
from app.Services.DatabaseService import Base

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    picture_id = Column(Integer, ForeignKey('picture.id'))
    picture = relationship("Picture", back_populates="tags")

    def __init__(self, name):
        self.name = name