from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.ganancia import Ganancia
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.carr_gan import Carr_Gan
from src.modelo.grupo_apuesta import Grupo_Apuesta
from src.modelo.declarative_base import Session, engine, Base

if __name__ == "__main__":
    #Abrir la session de la BD
    session = Session()
    apost = 'Pepe Pérez'
    nombrenew = 'Pepe Cadena'
    idapost = -1
    apostadores = session.query(Apostador).all()
    for apostador in apostadores:
        if apostador.Nombre == apost:
            idapost = apostador.id
            break

    if idapost != -1:        
        apostadorBase = session.query(Apostador).get(idapost)
        apostadorBase.Nombre = nombrenew
        session.commit()
        print('Apostador actualizado')
    else:
        print('Apostador no encontrado')
    
    carrera = session.query(Carrera).get(2)
    carrera.Abierta = False
    carrera.Ganador = 'Usain Bolt'
    session.commit()
    session.close()

