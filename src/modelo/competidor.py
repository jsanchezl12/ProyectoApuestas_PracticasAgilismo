from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Competidor(Base):
    __tablename__ = 'competidor'

    id = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Probabilidad = Column(Float)
    Estado = Column(String)
    carrera = Column(Integer, ForeignKey('carrera.id'))
    