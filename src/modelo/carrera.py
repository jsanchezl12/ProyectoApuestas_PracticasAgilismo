from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Carrera(Base):
    __tablename__ = 'carrera'

    id = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Abierta = Column(Boolean)
    Ganador = Column(String)
    Ganancia_Casa = Column(Integer)
    Competidores = relationship('Competidor', cascade='all, delete, delete-orphan')
    # carr_gans = Column(Integer, ForeignKey('carr_gan.id'))
    #grupo_apuestas = relationship('Grupo_Apuesta', cascade='all, delete, delete-orphan')
    Apuestas = relationship('Apuesta', cascade='all, delete, delete-orphan')
    Ganancias = relationship('Ganancia', cascade='all, delete, delete-orphan')
