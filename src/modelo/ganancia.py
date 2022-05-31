from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base

class Ganancia(Base):
    __tablename__ = 'ganancia'

    id = Column(Integer, primary_key=True)
    Ganancia_Valor = Column(Integer)
    #Apostador = Column(Integer, ForeignKey('apostador.id'))
    Apostador = Column(String, ForeignKey('apostador.Nombre'))
    #carr_gan = Column(Integer, ForeignKey('carr_gan.id'))
    Carrera = Column(Integer, ForeignKey('carrera.id'))