from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import Humano, Construccion, Muro
import math
from agent import GRID_INICIAL_X, GRID_FINAL_X, GRID_INICIAL_Y, GRID_FINAL_Y

class miModelo(Model):
    def __init__(self,N_humanos):
        self.running = True
        self.schedule = RandomActivation(self)        
        self.grid = MultiGrid(GRID_FINAL_X,GRID_FINAL_Y,False)   

        pintarMuros(self);  #Dibuja todos los muros
        
        for i in range(0,N_humanos): #Crea a los humanos y los coloca en una posicion aleatoria
            pos_x = self.random.randint(GRID_INICIAL_X + 1,GRID_FINAL_X - 2) #Posicion x del humano
            pos_y = self.random.randint(GRID_INICIAL_Y + 1 ,GRID_FINAL_Y - 2) #Posicion y del humano
            a = Humano(i,self,(pos_x,pos_y)) #Creacion del humano
            self.schedule.add(a)
            self.grid.place_agent(a, a.pos) #Coloca  en la posicion creada


            
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
    pintarMuro(modelo, GRID_INICIAL_X, GRID_FINAL_X, GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .3) ,  GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .3) ) #Torniquetes .3 de distancia
    pintarMuro(modelo, GRID_INICIAL_X, GRID_FINAL_X, GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .7) ,  GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .7) ) #Tren .7 de distancia

def pintarMuro(modelo, inicial_x, final_x, inicial_y, final_y):
    if inicial_y == final_y: #horizontal
        for i in range(inicial_x,final_x):
            a = Muro(i,modelo,(i,inicial_y))
            modelo.schedule.add(a)
            modelo.grid.place_agent(a, a.pos)
            
    elif inicial_x == final_x: #vertical
        for i in range(inicial_y,final_y):
            a = Muro(i,modelo,(inicial_x,i))
            modelo.schedule.add(a)
            modelo.grid.place_agent(a, a.pos)
    else:
        print("Algo Salio Mal")
    

    

   