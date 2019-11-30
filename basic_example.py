from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation

class miAgente(Agent): #Definimos la clase
    # Constructor
    def __init__(self,unique_id,model,capital):
        super().__init__(unique_id, model)
        self.capital = capital
    # Metodo step (nada mas imprime algo)
    def step(self):
        print("Mi capital es %s" % self.capital)

class miModelo(Model):
    def __init__(self,N_agentes):
        self.schedule = RandomActivation(self)
        for i in range(0,N_agentes):
            a = miAgente(i,self,self.random.randrange(5,15))
            self.schedule.add(a)
    def step(self):
        self.schedule.step()
        print("---- End of tick ----")

modelo1 = miModelo(10)
modelo1.step()
modelo1.step()