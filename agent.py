
from mesa import Agent
import math
GRID_INICIAL_X = 0
GRID_INICIAL_Y = 0
GRID_FINAL_X = 30
GRID_FINAL_Y = 30
YMURO_TORNIQUETES = GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .3)
YMURO_TREN = GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .8)
class Construccion(Agent):
    def __init__(self,unique_id, model, pos, transitable):
        super().__init__(unique_id, model)
        self.pos = pos
        self.transitable = transitable
    def get_position(self):
        return self.pos

class Muro(Construccion):
    def __init__(self,unique_id, model, pos,transitable):
        super().__init__(unique_id, model, pos, transitable)
    # def step(self):
class TorniqueteEntrada(Construccion):
    def __init__(self,unique_id, model, pos, transitable):
        super().__init__(unique_id, model, pos, transitable)
class TorniqueteSalida(Construccion):
    def __init__(self,unique_id, model, pos, transitable):
        super().__init__(unique_id, model, pos, transitable)
class Puerta(Construccion):
    def __init__(self,unique_id, model, pos, transitable):
        super().__init__(unique_id, model, pos, transitable)

class Humano(Agent):
    def __init__(self, model, pos):
        super().__init__(self,model)
        self.pos = pos
        self.direccion = self.set_direction()

    def get_position(self):
        return self.pos
    
    def set_direction(self):
        if self.pos[1] < YMURO_TREN:
            return False #False caminan hacia arriba
        elif self.pos[1] >= YMURO_TREN:
            return True #True caminan hacia abajo
        else:
            print("Algo salio mal al caminar")
    # 
    # HACIA TORNIQUETES
    # 
    def elegirTorniquete(self,modelo, posHumano, direccion):
        distancias = []
        if direccion:
            torniquetes = modelo.getTorniquetesEntrada()
        else:
            torniquetes = modelo.getTorniquetesSalida()
        for torniquete in torniquetes:
            distancias.append( math.pow( posHumano[0] - torniquete[0], 2) + math.pow(posHumano[1] - torniquete[1], 2) )

        return torniquetes[ distancias.index(min(distancias)) ] 
        

    def obtenerDestinosPosibles(self,torniqueteDestino, direccion):
        destinosPosibles = []
        vecindad = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False, radius = 1)
        for vecino in vecindad:
            humanosCerca = self.model.grid.get_neighbors(vecino,moore=True, include_center=True,radius=0)
            vecinos = [x for x in humanosCerca if type(x) is Humano and x!=self]

            if len(vecinos) < 3:
                destinosPosibles.append(vecino)
                obstaculosCerca = self.model.grid.get_neighbors(vecino,moore=True, include_center=True,radius=0)
                if direccion:
                    obstaculos = [x for x in humanosCerca if type(x) is not Humano and x!=self if type(x) is not TorniqueteEntrada] 
                else: 
                    obstaculos = [x for x in humanosCerca if type(x) is not Humano and x!=self if type(x) is not TorniqueteSalida] 
                if len(obstaculos) > 0:
                    destinosPosibles.remove(vecino)
        if torniqueteDestino in destinosPosibles:
            ObjetosEnTorniquete = self.model.grid.get_neighbors(torniqueteDestino,moore=True, include_center=True,radius=0)
            HumanosEnTorniquete = [x for x in ObjetosEnTorniquete if type(x) is Humano and x!=self]
            if len(HumanosEnTorniquete) > 0:
                return [self.pos]
            else:
                return [torniqueteDestino]
        if destinosPosibles == []:
            destinosPosibles.append(self.pos)
        return destinosPosibles
    def obtenerDestino(self, destinosPosibles, torniqueteDestino):
        distancias = [] 
        for destinoSiguiente in destinosPosibles:
             distancias.append( math.pow( destinoSiguiente[0] - torniqueteDestino[0], 2) + math.pow(destinoSiguiente[1] - torniqueteDestino[1], 2) )
        return destinosPosibles[ distancias.index(min(distancias)) ]
    # 
    # HACIA LAS PUERTAS
    # 
    def elegirPuerta(self,modelo, posHumano):
        distancias = []
        puertas = modelo.getPuertas()
        for puerta in puertas:
            distancias.append( math.pow( posHumano[0] - puerta[0], 2) + math.pow(posHumano[1] - puerta[1], 2) )
        return puertas[ distancias.index(min(distancias)) ] 

    def obtenerDestinosPosiblesPuertas(self,puertaDestino):
            destinosPosibles = []
            vecindad = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False, radius = 1)
            for vecino in vecindad:
                humanosCerca = self.model.grid.get_neighbors(vecino,moore=True, include_center=True,radius=0)
                vecinos = [x for x in humanosCerca if type(x) is Humano and x!=self]

                if len(vecinos) < 3:
                    destinosPosibles.append(vecino)
                    obstaculosCerca = self.model.grid.get_neighbors(vecino,moore=True, include_center=True,radius=0)
                    obstaculos = [x for x in humanosCerca if type(x) is not Humano and x!=self if type(x) is not Puerta] 
                    if len(obstaculos) > 0:
                        destinosPosibles.remove(vecino)
            if puertaDestino in destinosPosibles:
                ObjetosEnPuerta = self.model.grid.get_neighbors(puertaDestino,moore=True, include_center=True,radius=0)
                HumanosEnPuerta = [x for x in ObjetosEnPuerta if type(x) is Humano and x!=self]
                if len(HumanosEnPuerta) > 1:
                    return [self.pos]
                else:
                    return [puertaDestino]
            if destinosPosibles == []:
                destinosPosibles.append(self.pos)
            return destinosPosibles
    # 
    # DENTRO DE LAS PUERTAS
    # 
    def elegirUInterior(self,modelo, posHumano):
        distancias = []
        uInteriores = modelo.getUInteriores()
        for uInterior in uInteriores:
            distancias.append( math.pow( posHumano[0] - uInterior[0], 2) + math.pow(posHumano[1] - uInterior[1], 2) )
        #print(min(distancias))
        #print(distancias.index(min(distancias)))
        return uInteriores[ distancias.index(min(distancias)) ] 


    #
    # EN CADA TICK
    #
    def step(self):
        if self.pos[0] == GRID_INICIAL_X or self.pos[0] == GRID_FINAL_X -1  or self.pos[1] == GRID_INICIAL_Y or self.pos[1] == GRID_FINAL_Y -1:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            print("Humano eliminado")
        else:
            if self.pos[1] > YMURO_TORNIQUETES and self.direccion == True: #Si esta afuera de los torniquetes
                torniqueteDestino = self.elegirTorniquete(self.model, self.pos, self.direccion)
                destinosPosibles = self.obtenerDestinosPosibles(torniqueteDestino, self.direccion)
                destino = self.obtenerDestino(destinosPosibles,torniqueteDestino)

            elif self.pos[1] <= YMURO_TORNIQUETES and self.pos[1] > YMURO_TREN and self.direccion == True: #Si estan dentro de la estacion y van a la puerta
                PuertaDestino = self.elegirPuerta(self.model, self.pos)
                destinosPosibles = self.obtenerDestinosPosiblesPuertas(PuertaDestino)
                destino = self.obtenerDestino(destinosPosibles,PuertaDestino)

            elif self.pos[1] <= YMURO_TREN and self.direccion == True: #Si estan en la puerta y van a entrar al metro
                centroDestino = self.elegirUInterior(self.model, self.pos)
                destinosPosibles = self.obtenerDestinosPosiblesPuertas(centroDestino)
                destino = self.obtenerDestino(destinosPosibles,centroDestino)
            elif self.pos[1] < YMURO_TREN and self.direccion == False:
                PuertaDestino = self.elegirPuerta(self.model, self.pos)
                destinosPosibles = self.obtenerDestinosPosiblesPuertas(PuertaDestino)
                destino = self.obtenerDestino(destinosPosibles,PuertaDestino)
            elif self.pos[1] < YMURO_TORNIQUETES and self.pos[1] >= YMURO_TREN and self.direccion == False: #Si estan dentro de la estacion y van a los torniquetes
                torniqueteDestino = self.elegirTorniquete(self.model, self.pos, self.direccion)
                destinosPosibles = self.obtenerDestinosPosibles(torniqueteDestino,self.direccion)
                destino = self.obtenerDestino(destinosPosibles,torniqueteDestino)
            elif self.pos[1] >= YMURO_TORNIQUETES and self.direccion == False:
                destino = (self.pos[0] , self.pos[1] +1)
            else:
                destino = (0,0)
            self.model.grid.move_agent(self,destino)
            #print("Me movi a ", destino)
        
            # print("Soy un humano")    