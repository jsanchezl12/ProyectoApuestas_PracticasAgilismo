from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Apuesta(Base):
    __tablename__ = 'apuesta'

    id = Column(Integer, primary_key=True)
    Valor = Column(Integer)
    #Competidor = Column(String)
    Competidor = Column(String, ForeignKey('competidor.Nombre'))
    #Apostador = Column(Integer, ForeignKey('apostador.id'))
    Apostador = Column(String, ForeignKey('apostador.Nombre'))
    Carrera = Column(Integer, ForeignKey('carrera.id'))
    #grupo_apuesta = Column(Integer, ForeignKey('grupo_apuesta.id'))
    