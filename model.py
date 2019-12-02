from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import Humano, Construccion, Muro, Torniquete, Puerta
import math
from agent import GRID_INICIAL_X, GRID_FINAL_X, GRID_INICIAL_Y, GRID_FINAL_Y, YMURO_TORNIQUETES,YMURO_TREN
XTORNIQUETE_IZQ = math.floor(GRID_FINAL_X * .3)
XTORNIQUETE_CTR = math.floor(GRID_FINAL_X * .5)
XTORNIQUETE_DER = math.floor(GRID_FINAL_X * .7)

XPUERTA1 = math.floor(GRID_FINAL_X * .2)
XPUERTA2 = math.floor(GRID_FINAL_X * .4)
XPUERTA3 = math.floor(GRID_FINAL_X * .6)
XPUERTA4 = math.floor(GRID_FINAL_X * .8)

class miModelo(Model):
    def __init__(self,N_humanos):
        self.running = True
        self.schedule = RandomActivation(self)        
        self.grid = MultiGrid(GRID_FINAL_X,GRID_FINAL_Y,False)   

        pintarTorniquetes(self) #Dibuja los torniquetes
        pintarPuertas(self) #Dibuja todas las puertas
        pintarMuros(self);  #Dibuja todos los muros
        pintarHumanos(self,N_humanos)
           
    def step(self):
        self.schedule.step()
        if self.schedule.get_agent_count()<2:
            self.running = False
        print("---- End of tick ----")

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
            a = Muro(i,modelo,(i,inicial_y), False)
            vecinos = modelo.grid.get_neighbors(a.pos,moore=True, include_center=True,radius=0)
            vecinos = [x for x in vecinos if type(x) is Torniquete or Puerta]
            if vecinos==[]:
                modelo.grid.place_agent(a, a.pos)
                modelo.schedule.add(a)        
            
    elif inicial_x == final_x: #vertical
        for i in range(inicial_y,final_y):
            a = Muro(i,modelo,(inicial_x,i),False)
            modelo.schedule.add(a)
            modelo.grid.place_agent(a, a.pos)
    else:
        print("Algo Salio Mal")

def pintarTorniquetes(modelo):
    pintarTorniquete(1,modelo,XTORNIQUETE_DER,YMURO_TORNIQUETES)
    pintarTorniquete(1,modelo,XTORNIQUETE_DER+1,YMURO_TORNIQUETES)
    pintarTorniquete(1,modelo,XTORNIQUETE_CTR,YMURO_TORNIQUETES)
    pintarTorniquete(1,modelo,XTORNIQUETE_CTR+1,YMURO_TORNIQUETES)
    pintarTorniquete(1,modelo,XTORNIQUETE_CTR-1,YMURO_TORNIQUETES)
    pintarTorniquete(1,modelo,XTORNIQUETE_IZQ,YMURO_TORNIQUETES)
    pintarTorniquete(1,modelo,XTORNIQUETE_IZQ-1,YMURO_TORNIQUETES)

def pintarTorniquete(i,modelo, pos_x,pos_y):
    a = Torniquete(i,modelo,(pos_x,pos_y),True)
    modelo.schedule.add(a)
    modelo.grid.place_agent(a, a.pos)

def pintarPuertas(modelo):
    for i in range(-1,2):
        pintarPuerta(1,modelo,XPUERTA1 + i ,YMURO_TREN)
        pintarPuerta(1,modelo,XPUERTA2 + i ,YMURO_TREN)
        pintarPuerta(1,modelo,XPUERTA3 + i ,YMURO_TREN)
        pintarPuerta(1,modelo,XPUERTA4 + i ,YMURO_TREN)
        
    # pintarPuerta(1,modelo,XPUERTA,YMURO_TREN)
    # pintarPuerta(1,modelo,XPUERTA1,YMURO_TREN)
    # pintarPuerta(1,modelo,XPUERTA1,YMURO_TREN)
    # pintarPuerta(1,modelo,XPUERTA1,YMURO_TREN)
    # pintarPuerta(1,modelo,XPUERTA1,YMURO_TREN)


def pintarPuerta(i,modelo, pos_x,pos_y):
    a = Puerta(i,modelo,(pos_x,pos_y),True)
    modelo.schedule.add(a)
    modelo.grid.place_agent(a, a.pos)

def pintarHumanos(modelo,N_humanos):
    contador = 0
    while contador < N_humanos:
        pos_x = modelo.random.randint(GRID_INICIAL_X + 1,GRID_FINAL_X - 2) #Posicion x del humano
        pos_y = modelo.random.randint(GRID_INICIAL_Y + 1 ,GRID_FINAL_Y - 2) #Posicion y del humano
        if pos_y != YMURO_TORNIQUETES and pos_y !=  YMURO_TREN:
            contador+=1
            a = Humano(contador,modelo,(pos_x,pos_y)) #Creacion del humano
            modelo.schedule.add(a)
            modelo.grid.place_agent(a, a.pos) #Coloca  en la posicion creada    
    

    

    

   