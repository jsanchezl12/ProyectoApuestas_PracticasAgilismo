import unittest
from faker import Faker
import random

from src.logica.LogicaEPorra import Logica_EPorra, Carrera, Competidor
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

    self.session.commit()
    self.session.close()



class Semana5_TestCase(unittest.TestCase):
    pos_carr = 0
    pos_comp = 0

    def test_crearCarrera(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        #print(nombre_carrera)
        self.logica.crear_carrera(nombre_carrera)
        race = self.session.query(Carrera).filter(Carrera.Nombre == nombre_carrera).first()
        #print(consulta1)
        #carrera = self.logica.dar_carrera(nombre_carrera)
        self.assertEqual(race.Nombre, nombre_carrera)
        tearDown(self)

    def test_getlistacarreras(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        carreras = self.logica.dar_carreras()
        self.assertIsInstance(carreras, list)
        self.assertGreater(len(carreras),0)
        tearDown(self)

    def test_obtenercarrera(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        carreras = self.logica.dar_carreras()
        race = self.session.query(Carrera).filter(Carrera.Nombre == nombre_carrera).first()
        self.assertIsNotNone(race)
        tearDown(self)
    
    def test_eliminarCarrera_noExistente(self):
        setUp(self)
        id_carrera = self.data_factory.pyint(1501, 1990)
        rslt = self.logica.eliminar_carrera(id_carrera)
        self.assertEqual(rslt, 'No existe la carrera')
        tearDown(self)
    
    def test_eliminarCarrera_existente(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        
        rslt = self.logica.eliminar_carrera(self.pos_carr)
        #print(rslt)
        self.assertIsNone(rslt)
        tearDown(self)
    
    #TEST HU002

    def test_crearCompetidor(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_competidor = self.data_factory.name()
        proba = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(self.pos_carr,nombre_competidor, proba)
        self.assertTrue(self.logica.competidor_existe_nombre(id_carrera,nombre_competidor))
        tearDown(self)

    def test_editarCompetidor(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_competidor = self.data_factory.name()
        proba = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(self.pos_carr,nombre_competidor, proba)
        id_competidor = self.logica.dar_id_competidor(self.pos_carr, nombre_competidor)
        nombre_competidor2 = self.data_factory.name()
        proba2 = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.editar_competidor(self.pos_carr,self.pos_comp,nombre_competidor2, proba2)
        self.assertTrue(self.logica.competidor_existe_nombre(id_carrera,nombre_competidor2))
        tearDown(self)

    def test_editarCompetidor_conPorcentajeAlto(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_competidor = self.data_factory.name()
        prob = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(self.pos_carr,nombre_competidor, prob)
        id_competidor = self.logica.dar_id_competidor(self.pos_carr, nombre_competidor)
        prob_alto = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=1.0, max_value=2.0)
        rslt = self.logica.editar_competidor(self.pos_carr,self.pos_comp,nombre_competidor, prob_alto)
        self.assertEqual(rslt, 'La probabilidad es mayor que la restante')
        tearDown(self)

    def test_editarCompetidor_conPorcentajeBajo(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_competidor = self.data_factory.name()
        prob = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(self.pos_carr,nombre_competidor, prob)
        id_competidor = self.logica.dar_id_competidor(self.pos_carr, nombre_competidor)
        prob = -0.1
        rslt = self.logica.editar_competidor(self.pos_carr,self.pos_comp,nombre_competidor, prob)
        self.assertEqual(rslt, 'La probabilidad debe ser mayor a 0')
        tearDown(self)
    
    def test_editarCompetidor_conPorcentaje(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_competidor = self.data_factory.name()
        prob = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(self.pos_carr,nombre_competidor, prob)
        id_competidor = self.logica.dar_id_competidor(self.pos_carr, nombre_competidor)
        prob = 0.5
        rslt = self.logica.editar_competidor(self.pos_carr,self.pos_comp,nombre_competidor, prob)
        competidor = self.logica.dar_competidor(self.pos_carr, self.pos_comp)
        self.assertEqual(competidor['Probabilidad'], prob)
        self.assertIsNone(rslt)
        tearDown(self)

    def test_editarCompetidor_noExistente(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_competidor = self.data_factory.name()
        prob = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(self.pos_carr,nombre_competidor, prob)
        id_competidor_ficty = self.data_factory.pyint(1501, 1990)
        prob2 = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        rslt = self.logica.editar_competidor(self.pos_carr,id_competidor_ficty,nombre_competidor, prob2)
        self.assertEqual(rslt, 'No existe el competidor')
        tearDown(self)
    
    def test_eliminarCompetidor(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        nombre_competidor = self.data_factory.name()
        prob = self.data_factory.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0.01, max_value=0.99)
        self.logica.aniadir_competidor(self.pos_carr,nombre_competidor, prob)
        id_competidor = self.logica.dar_id_competidor(self.pos_carr, nombre_competidor)
        rslt = self.logica.eliminar_competidor(self.pos_carr,self.pos_comp)
        self.assertIsNone(rslt)
        tearDown(self)

    def test_eliminarCompetidor_noExistente(self):
        setUp(self)
        nombre_carrera = self.data_factory.name()
        self.logica.crear_carrera(nombre_carrera)
        id_carrera = self.logica.dar_carreraid_nom(nombre_carrera)
        id_competidor_ficty = self.data_factory.pyint(1501, 1990)
        rslt = self.logica.eliminar_competidor(self.pos_carr,id_competidor_ficty)
        self.assertEqual(rslt, 'No existe el competidor')
        tearDown(self)
