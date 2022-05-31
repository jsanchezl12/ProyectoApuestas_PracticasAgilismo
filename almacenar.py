from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.ganancia import Ganancia
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.carr_gan import Carr_Gan
from src.modelo.grupo_apuesta import Grupo_Apuesta
from src.modelo.declarative_base import Session, engine, Base

if __name__ == '__main__':

    #Crea la BD
    Base.metadata.create_all(engine)

    #Abre la sesión
    session = Session()
    
    #Crea un objeto de la clase Carrera
    carrera1 = Carrera(Nombre='Carrera 1', Abierta=True)
    carrera2 = Carrera(Nombre='Carrera 2', Abierta=True)

    session.add(carrera1)
    session.add(carrera2)

    #Commit
    session.commit()

    #Crea un objeto de la clase Competidor
    competidor1 = Competidor(Nombre='Juan Pablo Montoya', Probabilidad=float(0.15))
    competidor2 = Competidor(Nombre='Kimi Räikkönen', Probabilidad=float(0.2))
    competidor3 = Competidor(Nombre='Michael Schumacher', Probabilidad=float(0.65))

    competidor4 = Competidor(Nombre='Usain Bolt', Probabilidad=float(0.72))
    competidor5 = Competidor(Nombre='Lamont Marcell Jacobs', Probabilidad=float(0.13))
    competidor6 = Competidor(Nombre='Su Bingtian', Probabilidad=float(0.05))
    competidor7 = Competidor(Nombre='Robson da Silva', Probabilidad=float(0.1))

    session.add(competidor1)
    session.add(competidor2)
    session.add(competidor3)
    carrera1.Competidores = [competidor1, competidor2, competidor3]
    
    session.add(competidor4)
    session.add(competidor5)
    session.add(competidor6)
    session.add(competidor7)
    carrera2.Competidores = [competidor4, competidor5, competidor6, competidor7]

    #Commit
    session.commit()

    #Crea un objeto de la clase Apostador
    apostador1 = Apostador(Nombre='Pepe Pérez')
    apostador2 = Apostador(Nombre='Ana Andrade')
    apostador3 = Apostador(Nombre='Aymara Castillo')

    session.add(apostador1)
    session.add(apostador2)
    session.add(apostador3)

    #Commit
    session.commit()

    #Crea un objeto de la clase Grupo_Apuesta
    grupo_apuesta1 = Grupo_Apuesta()
    grupo_apuesta2 = Grupo_Apuesta()

    session.add(grupo_apuesta1)
    session.add(grupo_apuesta2)

    grupo_apuesta1.Carrera = carrera1.id
    grupo_apuesta2.Carrera = carrera2.id

    #Commit
    session.commit()

    #Crea un objeto de la clase Apuesta
    apuesta1 = Apuesta(Valor=10, Competidor=competidor1.Nombre)
    apuesta2 = Apuesta(Valor=25, Competidor=competidor3.Nombre)
    apuesta3 = Apuesta(Valor=14, Competidor=competidor1.Nombre)
    apuesta4 = Apuesta(Valor=45, Competidor=competidor4.Nombre)

    session.add(apuesta1)
    session.add(apuesta2)
    session.add(apuesta3)
    session.add(apuesta4)

    apuesta1.Apostador = apostador1.id  
    apuesta2.Apostador = apostador2.id
    apuesta3.Apostador = apostador3.id
    apuesta4.Apostador = apostador3.id

    grupo_apuesta1.Apuestas = [apuesta1, apuesta2, apuesta3]    
    grupo_apuesta2.Apuestas = [apuesta4]
    

    #Commit
    session.commit()

    #crea un objeto de la clase Ganancia
    carr_ganancia1 = Carr_Gan(Ganancia_Casa=4)
    carr_ganancia2 = Carr_Gan(Ganancia_Casa=-10)

    
    session.add(carr_ganancia1)
    session.add(carr_ganancia2)

    carr_ganancia1.Carrera = carrera1.id
    carr_ganancia2.Carrera = carrera2.id

    #Commit
    session.commit()

    #Crea un objeto de la clase Ganancia
    ganancia1 = Ganancia(Ganancia_Valor=13)
    ganancia2 = Ganancia(Ganancia_Valor=0)
    ganancia3 = Ganancia(Ganancia_Valor=15)

    ganancia4 = Ganancia(Ganancia_Valor=32)
    ganancia5 = Ganancia(Ganancia_Valor=12)
    ganancia6 = Ganancia(Ganancia_Valor=34)

    session.add(ganancia1)
    session.add(ganancia2)
    session.add(ganancia3)
    session.add(ganancia4)
    session.add(ganancia5)
    session.add(ganancia6)

    ganancia1.Apostador = apostador1.id
    ganancia2.Apostador = apostador2.id
    ganancia3.Apostador = apostador3.id
    ganancia4.Apostador = apostador1.id
    ganancia5.Apostador = apostador2.id
    ganancia6.Apostador = apostador3.id

    carr_ganancia1.Ganancias = [ganancia1, ganancia2, ganancia3]
    carr_ganancia2.Ganancias = [ganancia4, ganancia5, ganancia6]

    carrera1.carr_gans = carr_ganancia1.id
    carrera2.carr_gans = carr_ganancia2.id

    #Commit
    session.commit()

    #Cierra la sesión
    session.close()
    





