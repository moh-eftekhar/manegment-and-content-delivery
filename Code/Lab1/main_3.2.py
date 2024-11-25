from Base import BaseMultiple3
from Util import multiExecutor3, draw

#multi-server / Round Robin

#10 300000 10
#10 500000 20
#20 500000 10
if __name__ == "__main__":
    # ------------------ Constants ------------------
    SERVICE = 15
    SIM_TIME = 100000
    BUFFER_SIZE = 10
    # ------------------ Constants ------------------
    iterates = range(1, 30)
    result = []
    losses = []
    utilizations = []
    delays = []
    loads = []

    tempResult = None
    for item in iterates:
        tempResult = multiExecutor3(BaseMultiple3(SERVICE,item,SIM_TIME,BUFFER_SIZE),"second")
        result.append(tempResult)
        losses.append(tempResult["Loss_Prob"]*100)
        utilizations.append(tempResult["Avg_Users"])
        delays.append(tempResult["Avg_Delay"]*1000)
        loads.append(tempResult["Load"])
        print(item," : ",result[-1])

    
    draw("Main3.2_AL","Arrival - Loss Prob",iterates,"Arrival", losses, "Loss_Prob")
    draw("Main3.2_AU","Arrival - Utilization",iterates,"Arrival", utilizations, "Utilization")
    draw("Main3.2_AD","Arrival - Delay",iterates,"Arrival", delays, "Delay")
    draw("Main3.2_Arr-Load","Arrival - Load",iterates,"Arrival", loads, "Load")