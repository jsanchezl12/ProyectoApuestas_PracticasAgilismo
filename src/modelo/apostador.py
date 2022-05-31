from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Apostador(Base):
    __tablename__ = 'apostador'

    id = Column(Integer, primary_key=True)
    Nombre = Column(String)
    apuestas = relationship('Apuesta', cascade='all, delete, delete-orphan')
    ganancias = relationship('Ganancia', cascade='all, delete, delete-orphan')