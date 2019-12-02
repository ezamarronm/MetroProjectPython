
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
    def __init__(self,unique_id, model, pos):
        super().__init__(unique_id, model)
        self.direccion = True
        self.pos = pos
        self.direccion = None

    def get_position(self):
        return self.pos
    
    def step(self):
        if self.pos[0] == GRID_INICIAL_X or self.pos[0] == GRID_FINAL_X -2  or self.pos[1] == GRID_INICIAL_Y or self.pos[1] == GRID_FINAL_Y -2:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
        else:
            destino = (self.pos[0]+1,self.pos[1])
            self.model.grid.move_agent(self,destino)
            # print("Soy un humano")    