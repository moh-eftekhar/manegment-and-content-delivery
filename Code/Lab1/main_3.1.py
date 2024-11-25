from Base import BaseMultiple3
from Util import multiExecutor3, draw

#multi-server / Random

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
        tempResult = multiExecutor3(BaseMultiple3(SERVICE,item,SIM_TIME,BUFFER_SIZE),"first")
        result.append(tempResult)
        losses.append(tempResult["Loss_Prob"]*100)
        utilizations.append(tempResult["Avg_Users"])
        delays.append(tempResult["Avg_Delay"]*1000)
        loads.append(tempResult["Load"])
        print(item," : ",result[-1])

    
    draw("Main3.1_AL","BufferSize - Loss Prob",iterates,"BufferSize", losses, "Loss_Prob")
    draw("Main3.1_AU","BufferSize - Utilization",iterates,"BufferSize", utilizations, "Utilization")
    draw("Main3.1_AD","BufferSize - Delay",iterates,"BufferSize", delays, "Delay")
    draw("Main3.1_Arr-Load","Arrival - Load",iterates,"Arrival", loads, "Load")