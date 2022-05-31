import unittest
from faker import Faker
import random

from src.logica.LogicaEPorra import Logica_EPorra, Carrera, Competidor, Apostador, Ganancia, Apuesta
from src.modelo.declarative_base import Session
    #TEST ENTREGA SEMANA 5
	#TEST HU001
def setUp(self):
    self.session = Session()
    self.logica = Logica_EPorra()
    # Generación de datos con libreria Faker
    self.data_factory = Faker()

def tearDown(self):
    self.session = Session()
    self.logica = Logica_EPorra()
    carreras = self.session.query(Carrera).all()
    for carrera in carreras:
        self.session.delete(carrera)
    
    competidores = self.session.query(Competidor).all()
    for competidor in competidores:
        self.session.delete(competidor)

    apostadores = self.session.query(Apostador).all()
    for apostador in apostadores:
        self.session.delete(apostador)
    
    apuestas = self.session.query(Apuesta).all()
    for apuesta in apuestas:
        self.session.delete(apuesta)
    
    ganancias = self.session.query(Ganancia).all()
    for ganancia in ganancias:
        self.session.delete(ganancia)

    self.session.commit()
    self.session.close()

class Semana6_TestCase(unittest.TestCase):
    def test_darApuestas(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_apostador = self.data_factory.name()
        self.logica.aniadir_apostador(nombre_apostador)
        nombre_competidor = self.data_factory.name()
        proba = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(id_carrera-1,nombre_competidor, proba)
        print(str(id_carrera) + ' ' + nombre_competidor + ' ' + nombre_apostador)
        valor = self.data_factory.pyint(10,100)
        rslt = self.logica.crear_apuesta(nombre_apostador, id_carrera-1, valor, nombre_competidor)
        self.assertIsNone(rslt)
        apuestas = self.logica.dar_apuestas_carrera(id_carrera-1)
        self.assertIsInstance(apuestas, list)
        self.assertGreater(len(apuestas),0)
        apost_id = self.logica.get_apostadorid(nombre_apostador)
        existe = False
        for apuesta in apuestas:
            if apuesta['Competidor'] == nombre_competidor and apuesta['Apostador'] == nombre_apostador and apuesta['Carrera'] == id_carrera:
                existe = True
        self.assertTrue(existe)
        tearDown(self)

    def test_crearApuesta(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_apostador = self.data_factory.name()
        rslt = self.logica.aniadir_apostador(nombre_apostador)
        nombre_competidor = self.data_factory.name()
        proba = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        rslt = self.logica.aniadir_competidor(id_carrera-1,nombre_competidor, proba)
        print(str(id_carrera) + ' ' + nombre_competidor + ' ' + nombre_apostador)
        valor = self.data_factory.pyint(10,100)
        rslt = self.logica.crear_apuesta(nombre_apostador, id_carrera-1, valor, nombre_competidor)
        self.assertIsNone(rslt)
        apuesta = self.logica.dar_apuesta_comp(id_carrera-1, nombre_competidor, nombre_apostador)
        #print(apuesta['Competidor'] + '-' + str(apuesta['Apostador']) + '-' + str(apuesta['Carrera']) + '-' + str(apuesta['Valor']))
        self.assertEqual(apuesta.get('Valor'), valor)
        self.assertEqual(apuesta.get('Competidor'), nombre_competidor)
        self.assertEqual(apuesta.get('Apostador'), nombre_apostador)
        self.assertEqual(apuesta.get('Carrera'), id_carrera)
        tearDown(self)
    
    #falta terminar_carrera
    def test_terminarCarrera(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_apostador = self.data_factory.name()
        rslt = self.logica.aniadir_apostador(nombre_apostador)
        nombre_competidor = self.data_factory.name()
        proba = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        rslt = self.logica.aniadir_competidor(id_carrera-1,nombre_competidor, proba)
        print(str(id_carrera) + ' ' + nombre_competidor + ' ' + nombre_apostador)
        valor = self.data_factory.pyint(10,100)
        rslt = self.logica.crear_apuesta(nombre_apostador, id_carrera-1, valor, nombre_competidor)
        self.assertIsNone(rslt)
        apuesta = self.logica.dar_apuesta_comp(id_carrera-1, nombre_competidor, nombre_apostador)
        rslt = self.logica.terminar_carrera(id_carrera-1, nombre_competidor)
        self.assertIsNone(rslt)
        race = self.logica.dar_carrera(id_carrera-1)
        self.assertFalse(race.get('Abierta'))
        self.assertEqual(race.get('Ganador'),nombre_competidor)   
        tearDown(self) 
    
    def test_darReporteGanancias(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_apostador = self.data_factory.name()
        self.logica.aniadir_apostador(nombre_apostador)
        nombre_competidor = self.data_factory.name()
        proba = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(id_carrera-1,nombre_competidor,proba)
        print(str(id_carrera) + ' ' + nombre_competidor + ' ' + nombre_apostador)
        valor = self.data_factory.pyint(10,100)
        rslt = self.logica.crear_apuesta(nombre_apostador, id_carrera-1, valor, nombre_competidor)
        self.assertIsNone(rslt)
        id_competidor = self.logica.dar_id_competidor(id_carrera-1, nombre_competidor)
        lista_ganancias, ganancias_casa = self.logica.dar_reporte_ganancias(id_carrera-1, id_competidor-1)
        tearDown(self)
    
