import unittest
from faker import Faker
import random

from src.logica.LogicaEPorra import Logica_EPorra, Carrera, Competidor, Apostador, Ganancia, Apuesta
from src.modelo.declarative_base import Session

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

class Otros_TestCase(unittest.TestCase):
    def test_verCarrera(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        race = self.logica.dar_carreraById(id_carrera)
        self.assertEqual(race.get('Nombre'),nombre_carrera)
        tearDown(self)
    
    def test_editarCarrera(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_carrera2 = self.data_factory.name()
        rslt = self.logica.editar_carrera(id_carrera-1, nombre_carrera2)
        race = self.logica.dar_carreraById(id_carrera)
        self.assertEqual(race.get('Nombre'),nombre_carrera2)
        tearDown(self)

    def test_editarApostador(self):
        setUp(self)
        nombre_apostador = self.data_factory.name()
        self.logica.aniadir_apostador(nombre_apostador)
        apostador_id = self.logica.get_apostadorid(nombre_apostador)
        nombre_apostador2 = self.data_factory.name()
        self.logica.editar_apostador(apostador_id-1, nombre_apostador2)
        apostador = self.logica.get_apostador(apostador_id-1)
        self.assertEqual(apostador.get('Nombre'), nombre_apostador2)
        tearDown(self)
    
    def test_eliminarApostador(self):
        setUp(self)
        nombre_apostador = self.data_factory.name()
        self.logica.aniadir_apostador(nombre_apostador)
        apostador_id = self.logica.get_apostadorid(nombre_apostador)
        self.logica.eliminar_apostador(apostador_id-1)
        apostador = self.logica.get_apostador(apostador_id-1)
        self.assertEqual(apostador, None)
        tearDown(self)
    
    def test_eliminarApuesta(self):
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
        self.logica.eliminar_apuesta(id_carrera-1, id_carrera-1)
        apuesta = self.logica.dar_apuesta_comp(id_carrera-1, nombre_competidor, nombre_apostador)
        self.assertEqual(apuesta, None)
        tearDown(self)
        