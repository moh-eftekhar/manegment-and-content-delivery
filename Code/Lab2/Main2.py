import simpy
import matplotlib.pyplot as plt
from Util import simulator, Simulator2
from Base import Base, Base21
import numpy as np

if __name__ == '__main__':
    simtime = 100
    losses1 = []
    losses2 = []
    losses3 = []
    average_queuing_delays = []

    simtime_list = [1,50, 100, 200, 400, 800, 1600, 3200, 6400, 8000,10000]

    # Parameters
    edge_nodes = 1
    edge_bufferSize = 50
    cloud_bufferSize = 100

    # service times
    cloud_serv_time = 20
    A_edge_serv_time = 10
    A_cloud_serv_time = 5
    B_edge_serv_time = 5
    B_cloud_serv_partialprocess = 10
    B_cloud_serv_fullprocess = 15
    propagation_delay = 5

    arrival_rate = 1

    base21 = Base21(edge_nodes, edge_bufferSize, cloud_bufferSize, cloud_serv_time, A_edge_serv_time,
                    A_cloud_serv_time, B_edge_serv_time, B_cloud_serv_partialprocess, B_cloud_serv_fullprocess,
                    propagation_delay, arrival_rate)
    sim21 = Simulator2(base21.packet_arrivals, base21.measurements, base21.edge_node, base21.cloud_server,
                          base21.num_edge_nodes, base21.edge_buffer_size, base21.cloud_buffer_size,
                            base21.edge_buffer_size, base21.A_cloud_service_time, base21.A_edge_service_time,
                            base21.B_edge_sevice_time, base21.B_cloud_service_partialprocess,
                            base21.B_cloud_service_fullprocess, base21.propagation_delay, base21.arrival_rate)
    
    buffer_size_local = list(range(1, 100000 + 1, 10000))
    for buffer_local in buffer_size_local:
        sim21.RoadRunner(1, buffer_local).run(until=simtime)
        losses1.append( 100*  base21.measurements.drop/ ( base21.measurements.N_arr_A+ base21.measurements.N_arr_B))

    plt.plot(buffer_size_local, losses1)
    #plt.axvline(x=2000, color='red', linestyle='--')
    #plt.text(2000, max(losses), 'Transition Period', color='red', va='bottom', ha='center')
    plt.xlabel('Different local buffer sizes')
    plt.ylabel('Loss Probability at Cloud (%)')
    plt.title('Loss Probability over Different local buffer sizes')
    plt.show()