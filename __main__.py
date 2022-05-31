import sys
from PyQt5.QtWidgets import QApplication
from src.vista.InterfazEPorra import App_EPorra
from src.logica.Logica_mock import Logica_mock
from src.logica.LogicaEPorra import Logica_EPorra
import json

if __name__ == '__main__':
    # Punto inicial de la aplicación

    #Logica = Logica_mock()
    Logica = Logica_EPorra()
    #TEST Logica_EPorra
    # TEST Carrera
    # carreras = Logica.dar_carreras()
    # #print(carreras)
    # for carrera in carreras:
    #     print(carrera['Nombre'])
    
    # carr = Logica.dar_carrera(1)
    # if carr != None:
    #     print(carr['Nombre'])

    # Logica.crear_carrera('Carrera 3')
    # Logica.editar_carrera(2, "Carrera 2_")
    # carreras = Logica.dar_carreras()
    # for carrera in carreras:
    #     print(carrera['Nombre'])

    # Logica.terminar_carrera(1, 'Usain Bolt')        
    # Logica.eliminar_carrera(4)

    # TEST Competidores
    # competidores = Logica.dar_competidores_carrera(1)
    # for competidor in competidores:
    #     print(competidor['Nombre'] + '-->' + str(competidor['Probabilidad']))
    
    # competidor = Logica.dar_competidor(1, 1)
    # print(competidor['Nombre'])

    # #Logica.aniadir_competidor(1, 'Usain Bolt', 0.01)
    
    # Logica.editar_competidor(1, 1, 'Juan Pablo Montoya', 0.15)

    # competidores = Logica.dar_competidores_carrera(1)
    # for competidor in competidores:
    #     print(competidor['Nombre'] + '-->' + str(competidor['Probabilidad']))
    
    # Logica.eliminar_competidor(1, 8)
    # Logica.eliminar_competidor(1, 9)
    # carreras = Logica.dar_carreras()	
    # id_competidor = Logica.dar_id_competidor(carreras[0]['id'], 'Juan Pablo Montoya')
    # Logica.editar_competidor(carreras[0]['id'], id_competidor,'Juan Pablo Mogoyo', 0.14)
    # print(id_competidor)

    app = App_EPorra(sys.argv, Logica)
    sys.exit(app.exec_())