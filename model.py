from mesa import Model #importamos paquete mesa 
from mesa.time import RandomActivation 
from mesa.space import MultiGrid
from agent import Humano, Construccion, Muro, TorniqueteEntrada, TorniqueteSalida, Puerta
import math #importa funciones básicas de matemáticas
import time #importa función sleep
from random import randrange # importa paquete para elegir números aleatorios
from agent import GRID_INICIAL_X, GRID_FINAL_X, GRID_INICIAL_Y, GRID_FINAL_Y, YMURO_TORNIQUETES,YMURO_TREN, TIMERABRIR,TIMERCERRAR
#importa las constantes del archivo agentes
XTORNIQUETE_IZQ = math.floor(GRID_FINAL_X * .3) #posición en X de los tres torniquetes
XTORNIQUETE_CTR = math.floor(GRID_FINAL_X * .5)
XTORNIQUETE_DER = math.floor(GRID_FINAL_X * .7)

XPUERTA1 = math.floor(GRID_FINAL_X * .2) #Posición en X de las cuatro puertas
XPUERTA2 = math.floor(GRID_FINAL_X * .4)
XPUERTA3 = math.floor(GRID_FINAL_X * .6)
XPUERTA4 = math.floor(GRID_FINAL_X * .8)

X_U_INTERIOR1 = math.floor(GRID_FINAL_X * .1) #Posición en X a donde se dirigen los agentes al interior del vagón
H_ENTRANDO_ARRIBA = 10 #La cantidad de humanos que van apareciendo y se dirigen a los torniquetes
MIN_H_LLEGANDO_VAGON = 30 #Cabtidad mínima de humanos que llegan dentro del vagón
MAX_H_LLEGANDO_VAGON = 50 #CAntidad máxima de humanos que llegan dentro del vagón


class miModelo(Model): #definimos la clase miModelo
    def __init__(self,N_humanos): #constructor, metemos el argumento Número Humanos iniciales
        self.running = True #permite la ejecución continua 
        self.schedule = RandomActivation(self) # elige el tipo de schedule      
        self.grid = MultiGrid(GRID_FINAL_X,GRID_FINAL_Y,False) #tipo y tamaño de grid  
        self.posTorniquetesEntrada = [] #guarda las posiciones de los torniquites de entrada
        self.posTorniquetesSalida = [] #guarda las posiciones de los torniquites de salida
        self.posPuertas = [] #guarda las posiciones de las puertas
        self.puertas = [] #guarda los objetos puerta
        self.posUInteriores = calcularUInteriores() #te calcula todas las posiciones interios del vagón a donde se dirigen los usuarios
        self.contador = 1 # contador de ticks para abrir y cerrar puertas
        self.humanosEntraronTorniquetes = 0 #contador para humanos que entran a torniquetes
        self.humanosSalieronTorniquetes = 0 #contador para humanos que entran a torniquetes
        self.humanosEntraronVagon = 0 #contador para humanos que entran a torniquetes
        self.humanosSalieronVagon = 0 #contador para humanos que entran a torniquetes
        #self.timer = TIMERABIERTO
        pintarTorniquetes(self) #Dibuja los torniquetes
        pintarPuertas(self) #Dibuja todas las puertas
        pintarMuros(self);  #Dibuja todos los muros
        pintarHumanos(self,N_humanos, False)
    def step(self):
        print("Start tick")
        self.schedule.step()
        pintarNuevosHumanos(self,1)
        # N_humanos = self.random.randint(1,12)
        if self.schedule.get_agent_count()<2:
            self.running = False
        self.contador +=1
        humanosAEntrar = []
        humanosASalir = []
        if self.contador == TIMERABRIR and self.puertas[0].cerrada:
            humanosAEntrar = self.obtenerHumanosEnRango(GRID_INICIAL_X,GRID_FINAL_X, YMURO_TREN,YMURO_TORNIQUETES)
            print("HUMANOS A ENTRAR ", len(humanosAEntrar))
            time.sleep(5)
            for puerta in self.puertas:
                puerta.cerrada =  False
                self.contador = 0
            pintarHumanos(self, self.random.randint(MIN_H_LLEGANDO_VAGON,MAX_H_LLEGANDO_VAGON), True) #Humanos aleatorio que aparecen en el vagon
        elif self.contador == TIMERCERRAR and not self.puertas[0].cerrada:
            
            for puerta in self.puertas:
                puerta.cerrada =  True
                self.contador = 0
        elif self.contador == TIMERCERRAR -1 and not self.puertas[0].cerrada:
            humanosEntraron = self.obtenerHumanosEnRango(GRID_INICIAL_X,GRID_FINAL_X, GRID_INICIAL_Y+1,YMURO_TREN)
            humanosNoEntraron = self.obtenerHumanosEnRango(GRID_INICIAL_X,GRID_FINAL_X, YMURO_TREN,YMURO_TORNIQUETES)
            print("HUMANOS QUE ENTRARON ", len(humanosEntraron))
            print("HUMANOS QUE NO ENTRARON", len(humanosNoEntraron))
            time.sleep(5)
        # if self.contador == self.timer:
        #     for puerta in self.puertas:
        #         puerta.cerrada =  not puerta.cerrada
        #     if self.timer == 10:
        #         self.timer = 9
        #     elif self.timer == 9:
        #         self.timer = 10
        #     pintarHumanos(self, self.random.randint(30,50), True)
        #     self.contador = 0
        print("Los humanos que han entrado por los torniquetes son ", self.humanosEntraronTorniquetes)
        print("Los humanos que han salido por los torniquetes son ", self.humanosSalieronTorniquetes)
        print("Los Humanos que han entrado al vagon son ", self.humanosEntraronVagon)
        print("Los Humanos que han salido del vagon son ", self.humanosSalieronVagon)
        print("---- End of tick ----")
    def getTorniquetesEntrada(self):
        #return [(),(),()]
        return self.posTorniquetesEntrada
    def getPuertas(self):
        #return [(),(),()]
        return self.posPuertas
    def getUInteriores(self):
        return self.posUInteriores
    def getTorniquetesSalida(self):
        return self.posTorniquetesSalida
    def obtenerHumanosEnRango(self,xinicial,xfinal, yinicial,yfinal):
        totalHumanos = []
        for x in range(xinicial,xfinal + 1):
            for y in range(yinicial,yfinal):
                pos = (x,y)
                humanos = self.grid.get_neighbors( pos,moore=True, include_center=True,radius=0)
                humanos = [x for x in humanos if type(x) is Humano and x.direccion == True]
                if len(humanos) > 0:
                    totalHumanos = totalHumanos + humanos
        return totalHumanos

def pintarMuros(modelo):
    pintarMuro(modelo, GRID_INICIAL_X, GRID_FINAL_X, GRID_FINAL_Y - 1, GRID_FINAL_Y - 1) #Superior
    pintarMuro(modelo, GRID_INICIAL_X, GRID_FINAL_X, GRID_INICIAL_Y,  GRID_INICIAL_Y) #Inferior
    pintarMuro(modelo, GRID_INICIAL_X, GRID_INICIAL_X, GRID_INICIAL_Y+1, GRID_FINAL_Y-1) #Izquierda
    pintarMuro(modelo, GRID_FINAL_X -1, GRID_FINAL_X -1, GRID_INICIAL_Y, GRID_FINAL_Y-1) #Derecha
    pintarMuro(modelo, GRID_INICIAL_X, GRID_FINAL_X, YMURO_TORNIQUETES ,  YMURO_TORNIQUETES ) #Torniquetes .3 de distancia
    pintarMuro(modelo, GRID_INICIAL_X, GRID_FINAL_X, YMURO_TREN ,  YMURO_TREN ) #Tren .7 de distancia
    
def pintarMuro(modelo, inicial_x, final_x, inicial_y, final_y):
    if inicial_y == final_y: #horizontal
        for i in range(inicial_x,final_x):
            a = Muro(modelo,(i,inicial_y), False)
            vecinos = modelo.grid.get_neighbors(a.pos,moore=True, include_center=True,radius=0)
            vecinos = [x for x in vecinos if type(x) is TorniqueteEntrada or TorniqueteSalida or Puerta]
            if vecinos==[]:
                modelo.grid.place_agent(a, a.pos)
                modelo.schedule.add(a)        
            
    elif inicial_x == final_x: #vertical
        for i in range(inicial_y,final_y):
            a = Muro(modelo,(inicial_x,i),False)
            modelo.schedule.add(a)
            modelo.grid.place_agent(a, a.pos)
    else:
        print("Algo Salio Mal")

def pintarTorniquetes(modelo):
    pintarTorniquete(modelo,XTORNIQUETE_DER,YMURO_TORNIQUETES,False)
    pintarTorniquete(modelo,XTORNIQUETE_DER+1,YMURO_TORNIQUETES, False)
    pintarTorniquete(modelo,XTORNIQUETE_CTR,YMURO_TORNIQUETES, True)
    pintarTorniquete(modelo,XTORNIQUETE_CTR+1,YMURO_TORNIQUETES, True)
    pintarTorniquete(modelo,XTORNIQUETE_CTR-1,YMURO_TORNIQUETES, True)
    pintarTorniquete(modelo,XTORNIQUETE_IZQ,YMURO_TORNIQUETES, False)
    pintarTorniquete(modelo,XTORNIQUETE_IZQ-1,YMURO_TORNIQUETES, False)

def pintarTorniquete(modelo, pos_x,pos_y,EoS): #EoS es Entrada (True), Salida (False)
    if EoS:
        a = TorniqueteEntrada(modelo,(pos_x,pos_y),True) #True/Transitable False/NoTransitable
    else:
        a = TorniqueteSalida(modelo,(pos_x,pos_y),True)
    modelo.schedule.add(a)
    modelo.grid.place_agent(a, a.pos)
    if EoS:
        modelo.posTorniquetesEntrada.append(a.pos)
    else:
        modelo.posTorniquetesSalida.append(a.pos)

def pintarPuertas(modelo):
    for i in range(-1,2):
        pintarPuerta(modelo,XPUERTA1 + i ,YMURO_TREN)
        pintarPuerta(modelo,XPUERTA2 + i ,YMURO_TREN)
        pintarPuerta(modelo,XPUERTA3 + i ,YMURO_TREN)
        pintarPuerta(modelo,XPUERTA4 + i ,YMURO_TREN)


def pintarPuerta(modelo, pos_x,pos_y):
    a = Puerta(modelo,(pos_x,pos_y),True)
    modelo.schedule.add(a)
    modelo.grid.place_agent(a, a.pos)
    modelo.posPuertas.append(a.pos)
    modelo.puertas.append(a)

def pintarHumanos(modelo,N_humanos,step):
    contador = 0
    while contador < N_humanos:
        if step == False:
            pos_x = modelo.random.randint(GRID_INICIAL_X + 1,GRID_FINAL_X - 2) #Posicion x del humano
            pos_y = modelo.random.randint(YMURO_TREN + 1 ,GRID_FINAL_Y - 2) #Posicion y del humano
        else:
            pos_x = modelo.random.randint(GRID_INICIAL_X + 1,GRID_FINAL_X - 2) #Posicion x del humano
            pos_y = modelo.random.randint(GRID_INICIAL_Y + 1 ,YMURO_TREN - 1) #Posicion y del humano

        if pos_y != YMURO_TORNIQUETES and pos_y !=  YMURO_TREN:
            contador+=1
            a = Humano(modelo,(pos_x,pos_y)) #Creacion del humano
            modelo.schedule.add(a)
            modelo.grid.place_agent(a, a.pos) #Coloca  en la posicion creada
    #humanoPrueba = Humano(modelo,(40,40))
    #modelo.schedule.add(humanoPrueba)
    #modelo.grid.place_agent(humanoPrueba, humanoPrueba.pos) #Coloca  en la posicion creada
    #for i in range(0,4):
    #    humanoPrueba2 = Humano(modelo,(41,40))
    #    modelo.schedule.add(humanoPrueba2)
    #    modelo.grid.place_agent(humanoPrueba2, humanoPrueba2.pos) #Coloca  en la posicion creada
    

def pintarNuevosHumanos(modelo,N_humanos):
    #contador = 0
    #lista = [GRID_FINAL_X, GRID_INICIAL_X]
    
    #while contador < N_humanos:
    if modelo.random.randint(0,1):
        if modelo.random.randint(0,1):
            pos_x = GRID_FINAL_X -2 #Posicion x del humano
            pos_y = GRID_FINAL_Y -2 #GRID_FINAL_Y #Posicion y del humano
            #contador+=1
        else:
            pos_x = GRID_INICIAL_X +1 #Posicion x del humano
            pos_y = GRID_FINAL_Y -2 #GRID_FINAL_Y #Posicion y del humano
        for i in range (0,H_ENTRANDO_ARRIBA):  #PINTAR HUMANOS ENTRANDO AL METRO DESDE ARRIBA
            a = Humano(modelo,(pos_x,pos_y)) #Creacion del humano
            modelo.schedule.add(a)
            modelo.grid.place_agent(a, a.pos) #Coloca  en la posicion creada
        # a = Humano(modelo,(pos_x,pos_y)) #Creacion del humano
        # modelo.schedule.add(a)
        # modelo.grid.place_agent(a, a.pos) #Coloca  en la posicion creada
def calcularUInteriores():
    i = .1
    lista = []
    while GRID_FINAL_X * i < GRID_FINAL_X:
        lista.append( ( round (GRID_FINAL_X * i)  , ( math.floor(YMURO_TREN*.5)  )) )
        i = i + .2
    return lista


def prueba(modelo):
    return 50
