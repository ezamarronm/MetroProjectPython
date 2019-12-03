from mesa.visualization.modules import CanvasGrid # viz of grid
from mesa.visualization.ModularVisualization import ModularServer #server
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from model import miModelo #our model
from agent import Humano, Muro, Torniquete, Puerta
from agent import GRID_FINAL_X, GRID_FINAL_Y
def agent_portrayal(agent): #here we define the design of agents
    if agent is None:
        print("Algo salio mal...")
        return
    #(x, y) = agent.get_position()
    #portrayal["x"] = x
    #portrayal["y"] = y

    # portrayal = {"Shape": "circle",
    #     "Filled": "true",
    #     "Layer": 0,
    #     "Color": "red",
    #     "r": 0.5}
    # return portrayal 
    portrayal = {}
    if type(agent) is Humano:
        portrayal["Layer"] = 1
        portrayal["scale"] = .8
        portrayal["Shape"] = "./resources/human.png"
        #portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "red"
        portrayal["r"] = 0.5
    elif type(agent) is Muro:
        portrayal["Layer"] = 1
        #portrayal["Shape"] = "./resources/wall.png"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "black"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif type(agent) is Torniquete:
        portrayal["Layer"] = 1
        #portrayal["Shape"] = "./resources/wall.png"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "blue"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif type(agent) is Puerta:
        portrayal["Layer"] = 1
        #portrayal["Shape"] = "./resources/wall.png"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "red"
        portrayal["w"] = 1
        portrayal["h"] = 1
    return portrayal
grid = CanvasGrid(agent_portrayal,GRID_FINAL_X,GRID_FINAL_Y,1000,1000)
#chart = ChartModule([{"Label":"Nagentes","Color":"red"}],data_collector_name="datacollector")

server = ModularServer(miModelo,
                       [grid],
                       "Modelo del metro",
                       {"N_humanos":10})  