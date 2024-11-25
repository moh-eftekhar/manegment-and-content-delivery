import simpy
import random
import matplotlib.pyplot as plt


class Base:
    def __init__(self, num_edge_nodes, edge_buffer_size, cloud_buffer_size, cloud_server_time, A_edge_service_time,
                  A_cloud_service_time, B_edge_sevice_time, B_cloud_service_partialprocess, B_cloud_service_fullprocess,
                  propagation_delay, arrival_rate):
        self.num_edge_nodes = num_edge_nodes
        self.edge_buffer_size = edge_buffer_size
        self.cloud_buffer_size = cloud_buffer_size
        self.cloud_server_time = cloud_server_time
        self.A_edge_service_time = A_edge_service_time
        self.A_cloud_service_time = A_cloud_service_time
        self.B_edge_sevice_time = B_edge_sevice_time
        self.B_cloud_service_partialprocess = B_cloud_service_partialprocess
        self.B_cloud_service_fullprocess = B_cloud_service_fullprocess
        self.propagation_delay = propagation_delay
        self.arrival_rate = arrival_rate


    class Measure:
        def __init__(self, N_arr_a, N_arr_b, drop):
            self.N_arr_A = N_arr_a
            self.N_arr_B = N_arr_b
            self.drop = drop

    measurements = Measure(0, 0,  0)


    def packet_arrivals(self,env, micro_data_center, cloud_data_center, data,fraction = 0.1):
        packet_type_options = ['A', 'B']
        packet_id = 1

        while True:
            packet_type = random.choices(packet_type_options, weights=(1 - fraction, fraction))[0]

            # Updating arrival data
            if packet_type == "A":
                data.N_arr_A = data.N_arr_A + 1
            else:
                data.N_arr_B = data.N_arr_B + 1



            if len(micro_data_center.items) < self.edge_buffer_size:
                if packet_type == "A":
                    micro_data_center.put((packet_id, packet_type, self.A_edge_service_time))
                elif packet_type == "B":
                    micro_data_center.put((packet_id, packet_type, self.B_edge_sevice_time))


            else:
                if len(cloud_data_center.items) < self.cloud_buffer_size:
                    if packet_type == "A":
                        cloud_data_center.put(
                            (packet_id, packet_type, self.A_cloud_service_time + self.propagation_delay))

                    elif packet_type == "B":
                        cloud_data_center.put(
                            (packet_id, packet_type, self.B_cloud_service_fullprocess + self.propagation_delay))

                else:
                    data.drop = data.drop + 1


            yield env.timeout(random.expovariate(self.arrival_rate))
            packet_id += 1


    def edge_node(self,env, micro_data_center, cloud_data_center, node_id):
        while True:
            packet_id, packet_type, packet_processing_time = yield micro_data_center.get()

            yield env.timeout(packet_processing_time)
            print(f"Edge Node {node_id} processed packet {packet_id} of type {packet_type} at time {env.now}")

            if packet_type == 'B':
                yield cloud_data_center.put((packet_id, packet_type, self.B_cloud_service_partialprocess + self.propagation_delay))


    def cloud_server(self,env, cloud_data_center):
        while True:
            packet_id, packet_type, packet_processing_time = yield cloud_data_center.get()

            yield env.timeout(packet_processing_time)
            print(
                f"Cloud Server processed {packet_type} packet {packet_id} (including propagation delay) at time {env.now}")


class Base21:
    def __init__(self, num_edge_nodes, edge_buffer_size, cloud_buffer_size, cloud_server_time, A_edge_service_time,
                  A_cloud_service_time, B_edge_sevice_time, B_cloud_service_partialprocess, B_cloud_service_fullprocess,
                  propagation_delay, arrival_rate):
        self.num_edge_nodes = num_edge_nodes
        self.edge_buffer_size = edge_buffer_size
        self.cloud_buffer_size = cloud_buffer_size
        self.cloud_server_time = cloud_server_time
        self.A_edge_service_time = A_edge_service_time
        self.A_cloud_service_time = A_cloud_service_time
        self.B_edge_sevice_time = B_edge_sevice_time
        self.B_cloud_service_partialprocess = B_cloud_service_partialprocess
        self.B_cloud_service_fullprocess = B_cloud_service_fullprocess
        self.propagation_delay = propagation_delay
        self.arrival_rate = arrival_rate
        self.f = 0.5


    class Measure:
        def __init__(self, N_arr_a, N_arr_b, drop):
            self.N_arr_A = N_arr_a
            self.N_arr_B = N_arr_b
            self.drop = drop

    measurements = Measure(0, 0, 0)


    def packet_arrivals(self,env, micro_data_center, cloud_data_center, data, edge_buffer, cloud_buffer):
        packet_type_options = ['A', 'B']
        packet_id = 1

        while True:
            packet_type = random.choices(packet_type_options, weights=(1 - self.f, self.f))[0]

            # Updating arrival data
            if packet_type == "A":
                data.N_arr_A = data.N_arr_A + 1
            else:
                data.N_arr_B = data.N_arr_B + 1



            if len(micro_data_center.items) < edge_buffer:
                if packet_type == "A":
                    micro_data_center.put((packet_id, packet_type, self.A_edge_service_time))
                elif packet_type == "B":
                    micro_data_center.put((packet_id, packet_type, self.B_edge_sevice_time))


            else:
                if len(cloud_data_center.items) < cloud_buffer:
                    if packet_type == "A":
                        cloud_data_center.put(
                            (packet_id, packet_type, self.A_cloud_service_time + self.propagation_delay))

                    elif packet_type == "B":
                        cloud_data_center.put(
                            (packet_id, packet_type, self.B_cloud_service_fullprocess + self.propagation_delay))

                else:
                    data.drop = data.drop + 1


            yield env.timeout(random.expovariate(self.arrival_rate))
            packet_id += 1


    def edge_node(self,env, micro_data_center, cloud_data_center, node_id):
        while True:
            packet_id, packet_type, packet_processing_time = yield micro_data_center.get()

            yield env.timeout(packet_processing_time)
            print(f"Edge Node {node_id} processed packet {packet_id} of type {packet_type} at time {env.now}")

            if packet_type == 'B':
                yield cloud_data_center.put((packet_id, packet_type, self.B_cloud_service_partialprocess + self.propagation_delay))


    def cloud_server(self,env, cloud_data_center):
        while True:
            packet_id, packet_type, packet_processing_time = yield cloud_data_center.get()

            yield env.timeout(packet_processing_time)
            print(
                f"Cloud Server processed {packet_type} packet {packet_id} (including propagation delay) at time {env.now}")
