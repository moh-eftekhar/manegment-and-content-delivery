from Base import BaseMultiple
from Util import draw, multiExecutor
import numpy as np

#multi-server / finite queue / different buffer sizes
#Variation on the buffer size
#Constant arrival rate

#2b
if __name__ == "__main__":
    # ------------------ Constants ------------------
    SERVICE = 10
    ARRIVAL_RATE = 20
    SIM_TIME = 100000
    BUFFER_SIZE = range(1, 50)
    # ------------------ Constants ------------------
    result = []
    losses = []
    utilizations = []
    delays = []
    loads = []

    tempResult = None
    for item in BUFFER_SIZE:
        tempResult = multiExecutor(BaseMultiple(SERVICE,ARRIVAL_RATE,SIM_TIME,item))
        result.append(tempResult)
        print(tempResult["Loss_Prob"])
        losses.append(tempResult["Loss_Prob"]*100)
        utilizations.append(tempResult["Avg_Users"])
        delays.append(tempResult["Avg_Delay"]*1000)
        loads.append(tempResult["Load"])
        print(item," : ",result[-1])

    
    draw("Main2.1_AL","BufferSize - Loss Prob",BUFFER_SIZE,"BufferSize", losses, "Loss_Prob (%)")
    draw("Main2.1_AU","BufferSize - Utilization",BUFFER_SIZE,"BufferSize", utilizations, "Utilization")
    draw("Main2.1_AD","BufferSize - Delay",BUFFER_SIZE,"BufferSize", delays, "Delay(ms)")
    draw("Main1_BS-Load: ","BufferSize- Load",BUFFER_SIZE,"Buffer", loads, "Load")