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
    carreras = session.query(Carrera).all()

    print('Las carreras almacenadas son')
    print('----------------------------------------------------')
    for carrera in carreras:
        print(carrera.Nombre)
        print('Status:' + str(carrera.Abierta))
        if not carrera.Abierta and carrera.Ganador != None:
            print('Ganador: ' + carrera.Ganador)
        print('--Competidores:')
        for competidor in carrera.Competidores:
            print(competidor.Nombre + ' Prob:' +str(competidor.Probabilidad))
        print('--Apuestas:')
        for grupo in carrera.grupo_apuestas:
            for apuesta in grupo.Apuestas:
                apost = session.query(Apostador).get(apuesta.Apostador)
                print(str(apuesta.Valor) + ' ' + apost.Nombre + ' -->' + str(apuesta.Competidor))
        print('--Ganancias:')
        ganan = session.query(Carr_Gan).get(carrera.carr_gans)
        
        for ganancia in ganan.Ganancias:
            apost = session.query(Apostador).get(ganancia.Apostador)
            print(str(ganancia.Ganancia_Valor) + ' ' + apost.Nombre)
        print(str(ganan.Ganancia_Casa) +' Ganancia Casa')
        print('----------------------------------------------------')
