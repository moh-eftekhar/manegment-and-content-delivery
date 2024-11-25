from Base import BaseMultiple
from Util import draw, multiExecutor

#multi-server / finite queue / different arrival rates
#constant buffer size
#2a

if __name__ == "__main__":
    # ------------------ Constants ------------------
    SERVICE = 10
    SIM_TIME = 400000
    BUFFER_SIZE = float("inf")
    # ------------------ Constants ------------------
    # iterates = [i/10 for i in range(1, 50)] #arrival rates
    iterates = range(1,10) #buffer sizes
    result = []
    losses = []
    utilizations = []
    delays = []
    loads = []

    tempResult = None
    for item in iterates:
        tempResult = multiExecutor(BaseMultiple(SERVICE,item,SIM_TIME,BUFFER_SIZE))
        result.append(tempResult)
        print(tempResult["Loss_Prob"])
        losses.append(tempResult["Loss_Prob"]*100)
        utilizations.append(tempResult["Avg_Users"])
        delays.append(tempResult["Avg_Delay"]*1000)
        loads.append(tempResult["Load"])
        print(item," : ",result[-1])

    
    draw("Main2.2_AL","Arrival rate - Loss Prob",iterates,"Arrival", losses, "Loss_Prob(%)")
    draw("Main2.2_AU","Arrival rate - Utilization",iterates,"Arrival", utilizations, "Utilization")
    draw("Main2.2_AD","Arrival rate - Delay",iterates,"Arrival", delays, "Delay(ms)")
    draw("Main2.2_Arrival-Load: ","Arrival - Load",iterates,"Buffer", loads, "Load")