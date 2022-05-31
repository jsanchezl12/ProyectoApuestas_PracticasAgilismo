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

class Semana7_TestCase(unittest.TestCase):
    #Add Apostador
    def test_addApostador(self):
        setUp(self)
        nombre_apostador = self.data_factory.name()
        self.logica.aniadir_apostador(nombre_apostador)
        apostador_id = self.logica.get_apostadorid(nombre_apostador)
        apostador = self.logica.get_apostador(apostador_id-1)
        self.assertEqual(apostador.get('Nombre'), nombre_apostador)
        tearDown(self)
    
    #Dar Apostadores
    def test_darApostadores(self):
        setUp(self)
        nombre_apostador = self.data_factory.name()
        self.logica.aniadir_apostador(nombre_apostador)
        apostadores = self.logica.dar_apostadores()
        self.assertIsInstance(apostadores, list)
        existe = False
        for apostador in apostadores:
            if apostador.get('Nombre') == nombre_apostador:
                existe = True
        self.assertGreater(len(apostadores),0)
        self.assertTrue(existe)
        tearDown(self)

    #Editar apuestas 
    def test_editarApuesta(self):
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
        #print(str(valor))
        rslt = self.logica.crear_apuesta(nombre_apostador, id_carrera-1, valor, nombre_competidor)
        self.assertIsNone(rslt)
        apuesta = self.logica.dar_apuesta_comp(id_carrera-1, nombre_competidor, nombre_apostador)
        #print(apuesta['Competidor'] + '-' + str(apuesta['Apostador']) + '-' + str(apuesta['Carrera']) + '-' + str(apuesta['Valor']))
        self.assertEqual(apuesta.get('Valor'), valor)
        self.assertEqual(apuesta.get('Competidor'), nombre_competidor)
        self.assertEqual(apuesta.get('Apostador'), nombre_apostador)
        self.assertEqual(apuesta.get('Carrera'), id_carrera)
        new_valor = self.data_factory.pyint(20,100)
        #print(str(new_valor))
        rslt = self.logica.editar_apuesta(id_carrera-1,id_carrera-1,  new_valor)
        self.assertIsNone(rslt)
        apuesta2 = self.logica.dar_apuesta_comp(id_carrera-1, nombre_competidor, nombre_apostador)
        self.assertEqual(apuesta2.get('Valor'), new_valor)
        tearDown(self)
    
    #Eliminar carrera
    def test_eliminarCarrera(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        #print(nombre_carrera)
        self.logica.crear_carrera(nombre_carrera)
        race = self.session.query(Carrera).filter(Carrera.Nombre == nombre_carrera).first()
        #print(consulta1)
        #carrera = self.logica.dar_carrera(nombre_carrera)
        self.assertEqual(race.Nombre, nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        rslt = self.logica.eliminar_carrera(id_carrera-1)
        self.assertIsNone(rslt)
        tearDown(self)
