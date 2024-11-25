from Base import BaseMultiple4
from Util import multiExecutor4, draw

#multi-server / Round Robin

if __name__ == "__main__":
    # ------------------ Constants ------------------
    SERVICE = 10
    SIM_TIME = 1000
    BUFFER_SIZE = 10
    # ------------------ Constants ------------------
    iterates = range(1,11)
    result = []
    losses = []
    utilizations = []
    delays = []
    loads = []

    tempResult = None
    for item in iterates:
        tempResult = multiExecutor4(BaseMultiple4(item,SERVICE,SIM_TIME,BUFFER_SIZE))
        result.append(tempResult)
        losses.append(tempResult["Loss_Prob"])
        utilizations.append(tempResult["Avg_Users"])
        delays.append(tempResult["Avg_Delay"])
        loads.append(tempResult["Load"])
        print(item," : ",result[-1])

    
    draw("Main4_AL","Arrival - Loss Prob",iterates,"Arrival", losses, "Loss_Prob")
    draw("Main4_AU","Arrival - Utilization",iterates,"Arrival", utilizations, "Utilization")
    draw("Main4_AD","Arrival - Delay",iterates,"Arrival", delays, "Delay")
    draw("Main4_A-Load","Arrival - Load",iterates,"Arrival", loads, "Load")