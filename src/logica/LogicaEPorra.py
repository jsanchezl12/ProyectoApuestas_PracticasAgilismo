from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.ganancia import Ganancia
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
# from src.modelo.carr_gan import Carr_Gan
# from src.modelo.grupo_apuesta import Grupo_Apuesta
from sqlalchemy import inspect
from src.modelo.declarative_base import Session, engine, Base

import copy


class Logica_EPorra():
    carreras = []
    competidores = []
    apuestas = []
    apostadores = []
    ganancias = []
    
    def __init__(self):

        Base.metadata.create_all(engine)
        #Abrir la session de la BD
        session = Session()
        self.carreras = session.query(Carrera).all()
        self.competidores = session.query(Competidor).all()
        self.apuestas = session.query(Apuesta).all()
        self.apostadores = session.query(Apostador).all()
        self.ganancias = session.query(Ganancia).all()
        session.close()
        
    # -->Descripcion Eporra
    # -->Listado de Carreras

    def updateData(self):
        session = Session()
        self.carreras = session.query(Carrera).all()
        self.competidores = session.query(Competidor).all()
        self.apuestas = session.query(Apuesta).all()
        self.apostadores = session.query(Apostador).all()
        self.ganancias = session.query(Ganancia).all()
        session.close()

    def dar_carreras(self):
        session = Session()
        carreras = session.query(Carrera).all()
        lst_carreras = []
        # for carrera in carreras:
        #     lst_carreras.append({column: str(getattr(carrera, column)) for column in carrera.__table__.c.keys()})
        for ca in session.query(Carrera).all():
            lst_carreras.append(ca.__dict__)          
        session.close()
        return lst_carreras.copy()
    
    def dar_idCarreraPos(self, pos):
        try:
            carrera = self.carreras[pos]
            _id = None
            if carrera != None:
                _id = carrera.id
            return _id
        except IndexError:
            return None

    def dar_carrera(self, _id):
        session = Session()
        id_carrera = self.dar_idCarreraPos(_id)
        ca = session.query(Carrera).get(id_carrera)
        session.close()
        if ca != None:
            return ca.__dict__
        else:
            return None
    
    def dar_carreraById(self, id_carrera):
        session = Session()
        ca = session.query(Carrera).get(id_carrera)
        session.close()
        if ca != None:
            return ca.__dict__
        else:
            return None
    
    def dar_carreraid_nom(self, nombre):
        session = Session()
        car = session.query(Carrera).filter(Carrera.Nombre == nombre).first()
        if car != None:
            return car.id
    
    def carrera_existe_nombre(self, nombre):
        session = Session()
        car = session.query(Carrera).filter(Carrera.Nombre == nombre).first()
        if car != None:
            return True
        else:
            return False
    
    def carrera_existe_id(self, id):
        session = Session()
        car = session.query(Carrera).filter(Carrera.id == id).first()
        if car != None:
            return True
        else:
            return False
    
    def competidor_existe_nombre(self, idcarrera, nom_competidor):
        session = Session()
        competidores = session.query(Carrera).filter(Carrera.id == idcarrera).first().Competidores
        for competidor in competidores:
            if competidor.Nombre == nom_competidor:
                return True
        return False
    def competidor_existe_nombre_prob(self, idcarrera, nom_competidor, prob):
        session = Session()
        competidores = session.query(Carrera).filter(Carrera.id == idcarrera).first().Competidores
        for competidor in competidores:
            if competidor.Nombre == nom_competidor and competidor.Probabilidad == prob:
                return True
        return False
    
    def competidor_tiene_apuestas(self, idcarrera, idcompetidor):
        session = Session()
        apuestas = session.query(Apuesta).filter(Apuesta.Carrera == idcarrera).all()
        competidor_name = session.query(Competidor).filter(Competidor.id == idcompetidor).first().Nombre
        for apuesta in apuestas:
            if apuesta.Competidor == competidor_name:
                return True
        return False
    def competidor_existe_id(self, idcarrera, id):
        session = Session()
        competidores = session.query(Carrera).filter(Carrera.id == idcarrera).first().Competidores
        for competidor in competidores:
            if competidor.id == id:
                return True
        return False

    def crear_carrera(self, nombre):
        existe = self.carrera_existe_nombre(nombre)
        if not existe:
            session = Session()
            car = Carrera(Nombre=nombre, Abierta=True)
            session.add(car)
            session.commit()
            session.close()
            self.updateData()
        else:
            print('Ya existe la carrera')
            return 'Ya existe la carrera'
        #self.carreras.append({'Nombre':nombre, 'Competidores':[], 'Abierta':True})
        

    def editar_carrera(self, _id, nombre):
        session = Session()
        id = self.dar_idCarreraPos(_id)
        existe = self.carrera_existe_id(id)
        if existe:
            car = session.query(Carrera).filter(Carrera.id == id).first()
            car.Nombre = nombre
            session.commit()
            session.close()
            self.updateData()
            # self.carreras = session.query(Carrera).all()
        else:
            print('No existe la carrera')
            return 'No existe la carrera'
        
            

    def terminar_carrera(self, _id, ganador):
        session = Session()
        id = self.dar_idCarreraPos(_id)
        existe = self.carrera_existe_id(id)
        if existe:
            carreraStatus = self.dar_carreraById(id)['Abierta']
            if carreraStatus:
                existe_Ganador = self.competidor_existe_nombre(id, ganador)
                if existe_Ganador:
                    car = session.query(Carrera).filter(Carrera.id == id).first()
                    car.Abierta = False
                    car.Ganador = ganador
                    session.commit()
                    session.close()
                    self.updateData()
                    #self.carreras = session.query(Carrera).all()
                else:
                    print('No existe el competidor')
                    return 'No existe el competidor'
            else:
                print('La carrera ya esta cerrada')
                return 'La carrera ya esta cerrada'
        else:
            print('No existe la carrera')
            return 'No existe la carrera'

    def eliminar_carrera(self, _id):
        session = Session()
        id = self.dar_idCarreraPos(_id)
        existe = self.carrera_existe_id(id)
        if existe:
            carreraStatus = self.dar_carreraById(id)['Abierta']
            if carreraStatus:
                car = session.query(Carrera).filter(Carrera.id == id).first()
                session.delete(car)
                session.commit()
                session.close()
                self.updateData()
                #self.carreras = session.query(Carrera).all()
            else:
                print('La carrera esta cerrada')
                return 'La carrera esta cerrada'
        else:
            print('No existe la carrera')
            return 'No existe la carrera'

    def calcular_prob_carrera(self,id_carrera):
        session = Session()
        competidores = session.query(Competidor).filter(Competidor.carrera == id_carrera).all()
        sumaProb = 0
        for competidor in competidores:
            sumaProb += competidor.Probabilidad
        return sumaProb

    def calcular_prob_carrera_comp(self,id_carrera, id_competidor, prob):
        session = Session()
        competidores = session.query(Competidor).filter(Competidor.carrera == id_carrera).all()
        sumaProb = 0
        for competidor in competidores:
            if competidor.id == id_competidor:
                sumaProb += prob
            else:
                sumaProb += competidor.Probabilidad
        return sumaProb
    # -->Crear Carrera

    # -->Crear Competidor
    def dar_id_competidor_2(self,id_carrera, comp):
        session = Session()
        competidor = session.query(Competidor).filter(Competidor.Nombre == comp and Competidor.carrera == id_carrera).first()
        if competidor != None:
            return competidor.id

    def dar_id_competidor(self,_id, comp):
        session = Session()
        id_carrera = self.dar_idCarreraPos(_id)
        competidor = session.query(Competidor).filter(Competidor.Nombre == comp and Competidor.carrera == id_carrera).first()
        if competidor != None:
            return competidor.id
    def dar_competidores_carrera(self, _id):
        session = Session()
        id = self.dar_idCarreraPos(_id)
        existe = self.carrera_existe_id(id)
        if existe:
            car = session.query(Carrera).filter(Carrera.id == id).first()
            lst_competidores = []
            for comp in car.Competidores:
                lst_competidores.append(comp.__dict__)          
            return lst_competidores.copy()
        else:
            print('No existe la carrera')
            return 'No existe la carrera'
    
    def dar_idCompetidorPos(self, _id, _idcomp):
        try:
            carrera = self.carreras[_id]
            if carrera != None:
                session = Session()
                competidores = session.query(Competidor).filter(Competidor.carrera == carrera.id).all()
                comp = competidores[_idcomp]
                if comp != None:
                    return comp.id
                else:
                    return None
        except IndexError:
            return None
    

    def dar_competidor(self, _id, _idcomp):
        session = Session()
        id_carrera = self.dar_idCarreraPos(_id)
        id_competidor = self.dar_idCompetidorPos( _id, _idcomp)
        existe = self.carrera_existe_id(id_carrera)
        if existe:
            existe_comp = self.competidor_existe_id(id_carrera, id_competidor)
            if existe_comp:
                session = Session()
                competidor = session.query(Competidor).filter(Competidor.id == id_competidor and Competidor.carrera == id_carrera).first()
                if competidor != None:
                    return competidor.__dict__
                #return copy.copy(competidor)
            else:
                print('No existe el competidor')
                return 'No existe el competidor'
        else:
            print('No existe la carrera')
            return 'No existe la carrera'

    def aniadir_competidor(self, _id, nombre, probabilidad):
        id = self.dar_idCarreraPos(_id)
        existe = self.carrera_existe_id(id)
        if existe:
            carreraStatus = self.dar_carreraById(id)['Abierta']
            if carreraStatus:
                existe_comp = self.competidor_existe_nombre(id, nombre)
                if not existe_comp:
                    prob_carrera = self.calcular_prob_carrera(id)
                    if prob_carrera + probabilidad <= 1:
                        session = Session()
                        competidor = Competidor(Nombre=nombre, Probabilidad=probabilidad, carrera=id)
                        session.add(competidor)
                        session.commit()
                        session.close()
                        self.updateData()
                    else:
                        print('La probabilidad es mayor que la restante')
                        return 'La probabilidad es mayor que la restante'
                else:
                    print('Ya existe el competidor')
                    return 'Ya existe el competidor'
            else:
                print('La carrera esta cerrada')
                return 'La carrera esta cerrada'
        else:
            print('No existe la carrera')
            return 'No existe la carrera'

    def editar_competidor(self, _id, _idcomp, nombre, probabilidad):
        id_carrera = self.dar_idCarreraPos(_id)
        id_competidor = self.dar_idCompetidorPos( _id, _idcomp)
        if probabilidad > 0:
            existe = self.carrera_existe_id(id_carrera)
            if existe:
                existe_comp = self.competidor_existe_id(id_carrera, id_competidor)
                if existe_comp:
                    carreraStatus = self.dar_carreraById(id_carrera)['Abierta']
                    if carreraStatus:
                        #existe_comp = self.competidor_existe_nombre(id_carrera, nombre)
                        existe_comp_prob = self.competidor_existe_nombre_prob(id_carrera, nombre, probabilidad)
                        if not existe_comp_prob:
                            if not self.competidor_tiene_apuestas(id_carrera, id_competidor):
                                prob_carrera = self.calcular_prob_carrera_comp(id_carrera, id_competidor, probabilidad)
                                if prob_carrera <= 1:
                                    session = Session()
                                    competidor = session.query(Competidor).filter(Competidor.id == id_competidor and Competidor.carrera == id_carrera).first()
                                    competidor.Nombre = nombre
                                    competidor.Probabilidad = probabilidad
                                    session.commit()
                                    session.close()
                                    self.updateData()
                                else:
                                    print('La probabilidad es mayor que la restante')
                                    return 'La probabilidad es mayor que la restante'
                            else:
                                print('El competidor tiene apuestas asociadas')
                                return 'El competidor tiene apuestas asociadas'
                        else:
                            print('Ya existe un competidor con ese nombre')
                            return 'Ya existe un competidor con ese nombre'
                    else:
                        print('La carrera esta cerrada')
                        return 'La carrera esta cerrada'
                else:
                    print('No existe el competidor')
                    return 'No existe el competidor'
            else:
                print('No existe la carrera')
                return 'No existe la carrera'
        else:
            print('La probabilidad debe ser mayor a 0')
            return 'La probabilidad debe ser mayor a 0'
    
    def eliminar_competidor(self, _id, _idcomp):
        id_carrera = self.dar_idCarreraPos(_id)
        id_competidor = self.dar_idCompetidorPos( _id, _idcomp)
        existe = self.carrera_existe_id(id_carrera)
        if existe:
            existe_comp = self.competidor_existe_id(id_carrera, id_competidor)
            if existe_comp:
                carreraStatus = self.dar_carreraById(id_carrera)['Abierta']
                if carreraStatus:
                    session = Session()
                    competidor = session.query(Competidor).filter(Competidor.id == id_competidor and Competidor.carrera == id_carrera).first()
                    session.delete(competidor)
                    session.commit()
                    session.close()
                    self.updateData()
                else:
                    print('La carrera esta cerrada')
                    return 'La carrera esta cerrada'
            else:
                print('No existe el competidor')
                return 'No existe el competidor'
        else:
            print('No existe la carrera')
            return 'No existe la carrera'

    def existeApostador_nom(self, nom):
        session = Session()
        apostador = session.query(Apostador).filter(Apostador.Nombre == nom).first()
        if apostador != None:
            return True
        else:
            return False

    def existeApostador_id(self, _idApost):
        session = Session()
        apostador = session.query(Apostador).filter(Apostador.id == _idApost).first()
        if apostador != None:
            return True
        else:
            return False
    
    def get_apostadorid(self, nom):
        session = Session()
        apostador = session.query(Apostador).filter(Apostador.Nombre == nom).first()
        if apostador != None:
            return apostador.id
        else:
            return None

    def get_apostador_nom(self, id_):
        session = Session()
        apostador = session.query(Apostador).filter(Apostador.id == id_).first()
        if apostador != None:
            return apostador.Nombre
        else:
            return None

    def dar_idApostPos(self, pos):
        try:
            apostador = self.apostadores[pos]
            if apostador != None:
                return apostador.id
            else:
                return None
        except IndexError:
            return None
    def get_apostador_2(self, id):
        session = Session()
        apostador = session.query(Apostador).filter(Apostador.id == id).first()
        if apostador != None:
            return apostador.__dict__
        else:
            return None

    def get_apostador(self, _idapost):
        id = self.dar_idApostPos(_idapost)
        session = Session()
        apostador = session.query(Apostador).filter(Apostador.id == id).first()
        if apostador != None:
            return apostador.__dict__
        else:
            return None


    def aniadir_apostador(self, nombre_apost):
        if nombre_apost != '' and nombre_apost != None:
            if not self.existeApostador_nom(nombre_apost):
                session = Session()
                apostador = Apostador(Nombre=nombre_apost)
                session.add(apostador)
                session.commit()
                session.close()
                self.updateData()
            else:
                print('Ya existe el apostador')
                return 'Ya existe el apostador'
        else:
            print('El nombre no puede estar vacio')
            return 'El nombre no puede estar vacio'
        
    def apostador_tiene_apuestas(self, _idApost):
        id = self.dar_idApostPos(_idApost)
        session = Session()
        apostador = session.query(Apostador).filter(Apostador.id == id).first()
        if apostador != None:
            if apostador.apuestas != None:
                return True
            else:
                return False
        else:
            return False

    def editar_apostador(self, _id_, nombre_apost):
        id_apostador = self.dar_idApostPos(_id_)
        if id_apostador != None:
            if not self.existeApostador_nom(nombre_apost):
                if not self.apostador_tiene_apuestas(id_apostador):
                    session = Session()
                    apostador = session.query(Apostador).filter(Apostador.id == id_apostador).first()
                    apostador.Nombre = nombre_apost
                    session.commit()
                    session.close()
                    self.updateData()
                else:
                    print('El apostador tiene apuestas asociadas')
                    return 'El apostador tiene apuestas asociadas'
            else:
                print('Ya existe el apostador')
                return 'Ya existe el apostador'
        else:
            print('No existe el apostador')
            return 'No existe el apostador'

    def eliminar_apostador(self, _idApost):
        id_apostador = self.dar_idApostPos(_idApost)
        existe = self.existeApostador_id(id_apostador)
        if existe:
            if not self.apostador_tiene_apuestas(id_apostador):
                session = Session()
                apostador = session.query(Apostador).filter(Apostador.id == id_apostador).first()
                session.delete(apostador)
                session.commit()
                session.close()
                self.updateData()
            else:
                print('El apostador tiene apuestas asociadas')
                return 'El apostador tiene apuestas asociadas'
        else:
            print('No existe el apostador')
            return 'No existe el apostador'


    def dar_apostadores(self):
        session = Session()
        lst_apostadores = []
        for ap in session.query(Apostador).all():
            lst_apostadores.append(ap.__dict__)          
        return lst_apostadores.copy()
    
    # def dar_idApuestaPos(self, pos):
    #     try:
    #         apuesta = self.apuestas[pos]
    #         if apuesta != None:
    #             return apuesta.id
    #         else:
    #             return None
    #     except IndexError:
    #         return None

    def dar_idApuestaPos(self, _id, _idApu):
        try:
            carrera = self.carreras[_id]
            if carrera != None:
                session = Session()
                apuestas = session.query(Apuesta).filter(Apuesta.Carrera == carrera.id).all()
                apuesta = apuestas[_idApu]
                if apuesta != None:
                    return apuesta.id
                else:
                    return None
        except IndexError:
            return None

    def dar_apuesta_comp(self, _id, nombre_competidor, nombre_apostador):
        id_carrera = self.dar_idCarreraPos(_id)
        session = Session()
        for apuesta in session.query(Apuesta).all():
            #print(apuesta.Competidor + '-' + str(apuesta.Apostador) + '-' + str(apuesta.Carrera)) 
            if apuesta.Competidor == nombre_competidor and apuesta.Apostador == nombre_apostador and apuesta.Carrera == id_carrera:
                return apuesta.__dict__
        return None
    
    def dar_apuesta(self, _id, _idApu):
        id_carrera = self.dar_idCarreraPos(_id)
        id_apuesta = self.dar_idApuestaPos(_id, _idApu)
        session = Session()
        race = session.query(Carrera).get(id_carrera)
        apu = session.query(Apuesta).get(id_apuesta)

        for apuesta in session.query(Apuesta).all():
            if apuesta.id == apu.id and apuesta.Carrera == race.id:
                return apuesta.__dict__
        return ''

    def dar_ganancias(self, _id):
        id_carrera = self.dar_idCarreraPos(_id)
        # session = Session()
        # ganancias = session.query(Ganancia).filter(Ganancia.Carrera == id_carrera).all()
        # return ganancias.__dict__
        session = Session()
        lst_ganancias = []
        for ga in session.query(Ganancia).filter(Ganancia.Carrera == id_carrera).all():
            lst_ganancias.append(ga.__dict__)          
        return lst_ganancias.copy()

    def crear_apuesta(self,nombre_apostador,  _id, valor, nombre_competidor):
        id_carrera = self.dar_idCarreraPos(_id)
        if valor > 0:
            if nombre_apostador != '' and nombre_apostador != None:
                if self.dar_carreraById(id_carrera) != None:
                    if self.competidor_existe_nombre(id_carrera, nombre_competidor):
                        if self.existeApostador_nom(nombre_apostador):
                            session = Session()
                            apuest = Apuesta(Competidor=nombre_competidor, Valor=valor, Apostador=nombre_apostador, Carrera=id_carrera)
                            session.add(apuest)
                            session.commit()
                            session.close()
                            self.updateData()
                        else:    
                            print('No existe el apostador')
                            return 'No existe el apostador'
                    else:
                        print('No existe el competidor')
                        return 'No existe el competidor'
                else:
                    print('No existe la carrera')
                    return 'No existe la carrera'
            else:
                print('El nombre de apostador no puede estar vacio')
                return 'El nombre de apostador no puede estar vacio'
        else:
            print('El valor de la apuesta no puede ser menor o igual a 0')
            return 'El valor de la apuesta no puede ser menor o igual a 0'

    def editar_apuesta(self, _id, _idApu, valor):
        
        
        if valor > 0:
            session = Session()
            apus_dic = self.dar_apuesta(_id, _idApu)
            apuesta = session.query(Apuesta).get(apus_dic['id'])
            if apuesta != None:
                apuesta.Valor = valor
                session.commit()
                session.close()
                self.updateData()
            else:
                print('No existe la apuesta')
                return 'No existe la apuesta'
        else:
            print('El valor de la apuesta no puede ser menor o igual a 0')
            return 'El valor de la apuesta no puede ser menor o igual a 0'        

    def eliminar_apuesta(self, _id, _idApu):
        session = Session()
        apus_dic = self.dar_apuesta(_id, _idApu)
        apuesta = session.query(Apuesta).get(apus_dic['id'])
        if apuesta != None:
            session.delete(apuesta)
            session.commit()
            session.close()
            self.updateData()
        else:
            print('No existe la apuesta')
            return 'No existe la apuesta'

    def dar_apuestas_carrera(self, _id):
        id_carrera = self.dar_idCarreraPos(_id)
        session = Session()
        lst_apuestas = []
        for apuesta in session.query(Apuesta).filter(Apuesta.Carrera == id_carrera).all():
            lst_apuestas.append(apuesta.__dict__)
        return lst_apuestas.copy()

    def dar_reporte_ganancias(self, _id, _idcomp):
        id_carrera = self.dar_idCarreraPos(_id)
        id_competidor = self.dar_idCompetidorPos( _id, _idcomp)
        competidor_ganador = self.dar_competidor( _id, _idcomp)
        apostadores_ganadores = []
        session = Session()
        ganancias = 0
        for apuesta in session.query(Apuesta).filter(Apuesta.Carrera == id_carrera).all():
            ganancias += apuesta.Valor
            if apuesta.Competidor == competidor_ganador['Nombre']:
                apostadores_ganadores.append(apuesta.Apostador)
        
        ganacia_por_apostador = ganancias / (len(apostadores_ganadores)+1)
        if ganacia_por_apostador != 0:
            for apuesta in session.query(Apuesta).filter(Apuesta.Carrera == id_carrera).all():
                if apuesta.Competidor == competidor_ganador['Nombre']:
                    session = Session()
                    ganacia = Ganancia(Ganancia_Valor=ganacia_por_apostador, Apostador=apuesta.Apostador, Carrera=id_carrera)
                    session.add(ganacia)
                    session.commit()
                    session.close()
                else:
                    session = Session()
                    ganacia = Ganancia(Ganancia_Valor=0, Apostador=apuesta.Apostador, Carrera=id_carrera)
                    session.add(ganacia)
                    session.commit()
                    session.close()

            session = Session()
            carrera = session.query(Carrera).get(id_carrera)
            carrera.Ganancia = ganacia_por_apostador
            carrera.Abierta = False
            session.commit()
            session.close()
            self.updateData()
            lst_ganancias = []
            for ganancia in self.dar_ganancias(_id):
                #print(ganancia)
                base_tupla = ()
                base_tupla = (ganancia['Apostador'], ganancia['Ganancia_Valor'])
                lst_ganancias.append(base_tupla)
            return lst_ganancias, ganacia_por_apostador
        else:
            return [],0







