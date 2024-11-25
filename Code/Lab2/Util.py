import simpy
import matplotlib.pyplot as plt
import numpy as np

def simulator(packet_arrivals, measurements, edge_node, cloud_server, num_edge_nodes) :
  env = simpy.Environment()
  micro_data_center = simpy.Store(env)
  cloud_data_center = simpy.Store(env)

  fraction = 0.5  # Fraction of packets of type B
  env.process(packet_arrivals(env, micro_data_center, cloud_data_center, measurements))
  for node_id in range(num_edge_nodes):
      env.process(edge_node(env, micro_data_center, cloud_data_center, node_id + 1))
  env.process(cloud_server(env, cloud_data_center))
  return env


class Simulator2:
    def __init__(self, packet_arrivals, measurements, edge_node, cloud_server, num_edge_nodes,
                    buffer_size_local, cloud_buffer_size, edge_buffer_size, A_cloud_service_time, A_edge_service_time,
                    B_edge_sevice_time, B_cloud_service_partialprocess, B_cloud_service_fullprocess,
                    propagation_delay, arrival_rate):
        self.packet_arrivals = packet_arrivals
        self.measurements = measurements
        self.edge_node = edge_node
        self.cloud_server = cloud_server
        self.num_edge_nodes = num_edge_nodes
        self.buffer_size_local = buffer_size_local
        self.cloud_buffer_size = cloud_buffer_size
        self.edge_buffer_size = edge_buffer_size
        self.A_cloud_service_time = A_cloud_service_time
        self.A_edge_service_time = A_edge_service_time
        self.B_edge_sevice_time = B_edge_sevice_time
        self.B_cloud_service_partialprocess = B_cloud_service_partialprocess
        self.B_cloud_service_fullprocess = B_cloud_service_fullprocess
        self.propagation_delay = propagation_delay
        self.arrival_rate = arrival_rate
        self.fraction = 0.5  # Fraction of packets of type B
    def RoadRunner(self,type,changingVar):
        if type == 1:
            env = simpy.Environment()
            micro_data_center = simpy.Store(env)
            cloud_data_center = simpy.Store(env)
            env.process(self.packet_arrivals(env, micro_data_center, cloud_data_center, self.measurements, changingVar, self.cloud_buffer_size))
            for node_id in range(self.num_edge_nodes):
                env.process(self.edge_node(env, micro_data_center, cloud_data_center, node_id + 1))
            env.process(self.cloud_server(env, cloud_data_center))
            return env
        elif type == 2:
                env = simpy.Environment()
                micro_data_center = simpy.Store(env)
                cloud_data_center = simpy.Store(env)
                env.process(self.packet_arrivals(env, micro_data_center, cloud_data_center, self.measurements, self.edge_buffer_size, changingVar))
                for node_id in range(self.num_edge_nodes):
                    env.process(self.edge_node(env, micro_data_center, cloud_data_center, node_id + 1))
                env.process(self.cloud_server(env, cloud_data_center))
                return env
        else:
                env = simpy.Environment()
                micro_data_center = simpy.Store(env)
                cloud_data_center = simpy.Store(env)
                env.process(
                    self.packet_arrivals(env, micro_data_center, cloud_data_center, self.measurements, self.edge_buffer_size, self.cloud_buffer_size,changingVar))
                for node_id in range(self.num_edge_nodes):
                    env.process(self.edge_node(env, micro_data_center, cloud_data_center, node_id + 1, self.measurements))
                env.process(self.cloud_server(env, cloud_data_center))
                return env
    


def draw(saveTitle,title, x, x_label, y, y_label):
  plt.plot(x, y)
  #plt.axvline(x=2000, color='red', linestyle='--')
  #plt.text(2000, max(losses), 'Transition Period', color='red', va='bottom', ha='center')
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.title(title)
  plt.show()