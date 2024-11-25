from Base import Base
from Util import execute, draw

#different arrival rates

if __name__ == "__main__":
    # ------------------ Contants ------------------
    SERVICE = 10
    SIM_TIME = 10000
    BUFFER_SIZE = 50
    # ------------------ Contants ------------------
    # iterates = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7,5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12 , 12.5, 13, 13.5, 14, 14.5, 15]
    iterates = [i/10 for i in range(1, 50)]
    result = []
    losses = []
    utilizations = []
    delays = []
    loads = []
    
    tempResult = None
    for i in iterates:
        tempResult = execute(Base(SERVICE,i,SIM_TIME,BUFFER_SIZE))
        result.append(tempResult)
        losses.append(tempResult["Loss_Prob"])
        utilizations.append(tempResult["Avg_Users"])
        delays.append(tempResult["Avg_Delay"]*1000)
        loads.append(tempResult["Load"])
        print(i," : ",result[-1])

    draw("Main1_AL: ","Arrival Rate- Loss Prob (%)",iterates,"Arr_Rate", losses, "Loss_Prob(%)")
    draw("Main1_AU: ","Arrival Rate - Utilization",iterates,"Arr_Rate", utilizations, "Utilization(%)")
    draw("Main1_AD: ","Arrival Rate - Delay",iterates,"Arr_Rate", delays, "Delay (ms)")
    draw("Main1_Arr-Load: ","Arrival Rate - Load",iterates,"Arrival", loads, "Load")