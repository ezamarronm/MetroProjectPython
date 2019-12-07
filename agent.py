
from mesa import Agent
import math
GRID_INICIAL_X = 0
GRID_INICIAL_Y = 0
GRID_FINAL_X = 50
GRID_FINAL_Y = 50
YMURO_TORNIQUETES = GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .3)
YMURO_TREN = GRID_FINAL_Y - math.floor(GRID_FINAL_Y * .7)
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
    #     print("Soy un muro")
class Torniquete(Construccion):
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
    def elegirTorniquete(self,modelo):
        print("Hello")
        torniquetes = modelo.getTorniquetes()
        print(torniquetes)


    def step(self):
        if self.pos[0] == GRID_INICIAL_X or self.pos[0] == GRID_FINAL_X -1  or self.pos[1] == GRID_INICIAL_Y or self.pos[1] == GRID_FINAL_Y -1:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            print("Humano eliminado")
        else:
            if self.pos[1] > YMURO_TORNIQUETES and self.direccion == True:
                destino = (self.pos[0],self.pos[1]-1)
                torniqueteDestino = self.elegirTorniquete(self.model)
                #destino = (self.pos[0],self.pos[1]-1)
            elif self.pos[1] < YMURO_TORNIQUETES and self.pos[1] > YMURO_TREN and self.direccion == True:
                destino = self.pos
            elif self.pos[1] < YMURO_TREN and self.direccion == False:
                destino = (self.pos[0],self.pos[1]+1)
            else:
                destino = (0,0)
            self.model.grid.move_agent(self,destino)
            #print("Me movi a ", destino)
        
            # print("Soy un humano")    