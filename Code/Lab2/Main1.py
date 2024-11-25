import simpy
import matplotlib.pyplot as plt
from Util import simulator
from Base import Base

if __name__ == '__main__':
    losses = []
    simtime_list = range(1,100000, 1000)#[1,50, 100,1000,50000, 100000, 150000, 200000, 250000, 300000]

    edge_nodes = 1
    A_edge_serv_time = 2
    B_edge_serv_time = 2
    edge_bufferSize = 100
    cloud_serv_time = 1
    A_cloud_serv_time = 1
    B_cloud_serv_time = 5
    cloud_bufferSize = 100
    B_cloud_serv_partialprocess = 10
    B_cloud_serv_fullprocess = 15
    propagation_delay = 5
    arrival_rate = 0.9
    edgePackets = []
    cloudPackets = []

    base1 = Base(edge_nodes, edge_bufferSize, cloud_bufferSize, cloud_serv_time, A_edge_serv_time,
                    A_cloud_serv_time, B_edge_serv_time, B_cloud_serv_partialprocess,
                    B_cloud_serv_fullprocess, propagation_delay, arrival_rate)
    runner = simulator(base1.packet_arrivals, base1.measurements, base1.edge_node, base1.cloud_server, edge_nodes)
    for simtime in simtime_list:
        runner.run(until=simtime)
        losses.append( 100*  base1.measurements.drop/ ( base1.measurements.N_arr_A+ base1.measurements.N_arr_B))
        edgePackets.append(base1.measurements.N_arr_A)
        cloudPackets.append(base1.measurements.N_arr_B)


    plt.plot(simtime_list, losses, color='g') #,marker = 'o', ms = 5, mec = 'g'
    # plt.text(2000, max(losses), 'Transient', color='red', va='bottom', ha='center')
    plt.xlabel('Sim Time (Seconds)')
    plt.ylabel('Loss Prob (%)')
    plt.title('Loss Probability During Time')
    plt.show()