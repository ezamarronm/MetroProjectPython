from model import miModelo
from mesa.batchrunner import BatchRunner 
from server import N_HUMANOS_INICIALES
from model import prueba
import matplotlib.pyplot as plt

fixed_params ={}
variable_params = {"N_humanos":N_HUMANOS_INICIALES}

batchRun = BatchRunner(miModelo,
                       fixed_parameters=fixed_params,
                       variable_parameters= variable_params,
                       iterations=1,
                       max_steps=5000,
                       model_reporters={"numTicks":prueba})

batchRun.run_all()

batch_data = batchRun.get_model_vars_dataframe()

print(batch_data)

plt.scatter(batch_data.N,batch_data.numTicks)
plt.show()