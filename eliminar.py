from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.ganancia import Ganancia
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.carr_gan import Carr_Gan
from src.modelo.grupo_apuesta import Grupo_Apuesta
from src.modelo.declarative_base import Session, engine, Base


def fn_can_delete_competidor(idComp):
    session = Session()
    carreras = session.query(Carrera).all()
    for carrera in carreras:
        for competidor in carrera.Competidores:
            if competidor.id == idComp and carrera.Abierta == False:
                return False

    return True        

if __name__ == "__main__":
    #Abrir la session de la BD
    session = Session()
    #eliminar competidor -- Su Bingtian
    competidor_name = 'Usain Bolt'
    idComp = -1
    competidores =  session.query(Competidor).all()
    for competidor in competidores:
        if competidor.Nombre == competidor_name:
            idComp = competidor.id
            break

    if idComp != -1:
        if fn_can_delete_competidor(idComp):
            competidorBase = session.query(Competidor).get(idComp)
            session.delete(competidorBase)
            session.commit()
            print('Competidor eliminado')
        else:
            print('No se puede eliminar el competidor')    
    else:
        print('Competidor no encontrado')
    
    session.close()