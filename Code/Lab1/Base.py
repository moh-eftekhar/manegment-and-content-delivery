#!/usr/bin/python3
import random
#ES - Event Scheduler
# ------------------------------------ Single ------------------------------------
class Base:
    def __init__(self, service, arrival, sim_time, max_buffer_size = float('inf')):
        self.service = 1/service
        self.arrival = 1/arrival
        self.load= self.service / self.arrival
        self.max_buffer_size = max_buffer_size
        self.type1 = 1 #!! type of what?
        self.sim_time = sim_time #!! simulation time
        self.arrivals=0 #!! number of arrivals
        self.users=0 #!! number of users
        self.data = None #!! what is this
        self.BusyServer=False #!! is the server busy?
        self.MM1= None #!! type of queue
        self.FES = None #!! this future event scheduler and Arr and Dep are events
        self.result = None #!! what is this
        random.seed(42) #!! what is this - seed for random number generator

    class Measure: #!! this is where we store the data
        def __init__(self,Narr,Ndep,NAveraegUser,OldTimeEvent,AverageDelay,Drop):
            self.arr = Narr #!! number of arrivals
            self.dep = Ndep #!! number of departures
            self.ut = NAveraegUser #!! average number of users
            self.oldT = OldTimeEvent #!! what is this? old time
            self.delay = AverageDelay #!! average delay
            self.drop = Drop #!! number of drops

    class Client: #!! what is this what is use of this
        def __init__(self,type,arrival_time):
            self.type = type #!! what is this what are the types? arrival or departure?
            self.arrival_time = arrival_time #!! arrival time of a client which is a packet ?

    class Server(object):
        def __init__(self):
            self.idle = True

    def Arrival(self,time, queue):
        # cumulate statistics
        self.data.arr += 1 #!! increment number of arrivals
        self.data.ut += self.users*(time - self.data.oldT) #!! utilization = number of users * time
        self.data.oldT = time #!! what is this? the time when this one entered the system -> later it will be used to calculate the utilization

        # sample the time until the next event
        inter_arrival = random.expovariate(lambd=1/self.arrival) #!! inter arrival time is exponential with lambda = 1/arrival rate (lambda is the rate of the exponential distribution) - this is the time until the next arrival event occurs
        #schedule the next arrival
        self.FES.put((time + inter_arrival, "arrival")) #!! put the next arrival event in the future event scheduler
        self.users += 1
        client = self.Client(self.type1,time) #!! create a client with type 1 and arrival time = time

        #check the buffer size before putting the packet in the queue
        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            #if the buffer is full we increment the number of drops
            self.data.drop += 1
            self.users -= 1

        # start service if the server is idle and the queue is not empty (there is a packet to serve)
        #avoid duplication on service
        if self.users==1:
            service_time = random.expovariate(1/self.service) # sample the service time
            self.FES.put((time + service_time, "departure")) # schedule the departure - when the packet is served and leaves the system

    def Departure(self,time, queue):
        # cumulate statistics
        self.data.dep += 1
        self.data.ut += self.users*(time-self.data.oldT)
        self.data.oldT = time
        client = queue.pop(0) #!! pop the first packet from the queue why? because it is the first one that entered the system and it is the first one that will leave the system - FIFO
        self.data.delay += (time-client.arrival_time) #!! calculate the delay of the packet in the system
        self.users -= 1

        if self.users >0:
            #if there are more packets to serve - schedule the departure of the next one - when this one leaves the system
            service_time = random.expovariate(1/self.service)
            self.FES.put((time + service_time, "departure"))


# ------------------------------------ Mutli ------------------------------------


class BaseMultiple:
    def __init__(self, service, arrival, sim_time, max_buffer_size = float('inf')):
        self.busyServer=False
        self.service = 1/service
        self.arrival = 1/arrival
        self.load= self.service / self.arrival
        self.max_buffer_size = max_buffer_size
        self.type1 = 1
        self.sim_time = sim_time
        self.arrivals=0
        self.users=0
        self.data = None
        self.BusyServer=False
        self.MM1= None
        self.FES = None
        self.result = None
        random.seed(42)

    class Measure:
        def __init__(self):
            #added
            self.arr = 0
            self.dep = 0
            self.ut = 0
            self.oldT = 0
            self.delay = 0
            self.drop = 0

    class Client:
        def __init__(self,type,arrival_time):
            self.type = type
            self.arrival_time = arrival_time

    class Server(object):
        def __init__(self):
            self.idle = True
            #added
            self.users = 0 #!! number of users in the system - initially 0 - when a packet arrives it becomes 1 and so on

    def Arrival(self,time, queue,server):
        #added
        server.users += 1 # increment the number of users in which server and queue?
        self.data.ut += server.users * (time - self.data.oldT)
        self.data.arr += 1
        self.data.oldT = time

        inter_arrival = random.expovariate(lambd=1/self.arrival)
        self.FES.put((time + inter_arrival, "arrival"))
        client = self.Client(self.type1,time)

        #updated
        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            self.data.drop += 1
            server.users -= 1

        if server.idle: #!! active server when an arrival occurs
            server.idle = False
            service_time = random.expovariate(1/ self.service)
            self.FES.put((time + service_time, "departure", server))

    def Departure(self,time, queue, server):
        self.data.dep += 1
        self.data.ut += server.users * (time - self.data.oldT)
        self.data.oldT = time

        client = queue.pop(0)

        self.data.delay += (time - client.arrival_time)
        server.users -= 1

        if server.users > 0:
            service_time = random.expovariate(1 / self.service)
            self.FES.put((time + service_time, "departure", server))

        else: #!! deactive server when the last packet leaves the system and there are no more packets to serve
            server.idle = True

# ------------------------------------ Mutli 3 ------------------------------------

class BaseMultiple3:
    def __init__(self, service, arrival, sim_time, max_buffer_size = float('inf'),type = "first"):
        # self.busyServer=False
        self.service = 1/service
        self.arrival = 1/arrival
        self.load= self.service / self.arrival
        self.max_buffer_size = max_buffer_size
        self.type1 = 1
        self.sim_time = sim_time
        self.arrivals=0
        self.users=0
        self.data = None
        self.BusyServer=False
        self.MM1= None
        self.FES = None
        self.result = None
        random.seed(42)

    class Measure:
        def __init__(self):
            #added
            self.arr = 0
            self.dep = 0
            self.ut = 0
            self.oldT = 0
            self.delay = 0
            self.drop = 0

    class Client:
        def __init__(self,type,arrival_time):
            self.type = type
            self.arrival_time = arrival_time

    class Server:
        def __init__(self, service_time):
            self.idle = True
            self.users = 0
            self.service_time = service_time

    def Arrival(self,time, queue,server):
        #added
        server.users += 1 # increment the number of users in which server and queue?
        self.data.ut += server.users * (time - self.data.oldT)
        self.data.arr += 1
        self.data.oldT = time

        inter_arrival = random.expovariate(lambd=1/self.arrival)
        self.FES.put((time + inter_arrival, "arrival"))
        client = self.Client(self.type1,time)

        #updated
        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            self.data.drop += 1
            server.users -= 1

        if server.idle:
            server.idle = False

            service_time = random.expovariate(1 / self.service)
            self.FES.put((time + service_time, "departure", server))

    def Departure(self,time, queue, server):
        self.data.dep += 1
        self.data.ut += server.users * (time - self.data.oldT)
        self.data.oldT = time

        if len(queue) > 0:
            client = queue.pop(0)

            self.data.delay += (time - client.arrival_time)
            server.users -= 1

            if server.users > 0:
                if type == "third": #!! what is this? what is the type?
                    service_time = random.expovariate(1 / server.service_time) #!! what is this ? service time is different for each packet
                else:
                    service_time = random.expovariate(1 / self.service) #!! what is this ? service time is the same for each packet
                self.FES.put((time + service_time, "departure", server))
            else:
                server.idle = True
        else:
            server.idle = True


# ------------------------------------ Mutli 4 ------------------------------------
class BaseMultiple4:
    def __init__(self, service, arrival, sim_time, max_buffer_size = float('inf')):
        self.service = 1/service
        self.arrival = 1/arrival
        self.load= self.service / self.arrival
        self.max_buffer_size = max_buffer_size
        self.type1 = 1 #!! type of what?
        self.sim_time = sim_time #!! simulation time
        self.arrivals=0 #!! number of arrivals
        self.users=0 #!! number of users
        self.data = None #!! what is this
        self.BusyServer=False #!! is the server busy?
        self.MM1= None #!! type of queue
        self.FES = None #!! this future event scheduler and Arr and Dep are events
        self.result = None #!! what is this
        random.seed(42) #!! what is this - seed for random number generator

    class Measure: #!! this is where we store the data
        def __init__(self,Narr,Ndep,NAveraegUser,OldTimeEvent,AverageDelay,Drop):
            self.arr = Narr #!! number of arrivals
            self.dep = Ndep #!! number of departures
            self.ut = NAveraegUser #!! average number of users
            self.oldT = OldTimeEvent #!! what is this? old time
            self.delay = AverageDelay #!! average delay
            self.drop = Drop #!! number of drops

    class Client: #!! what is this what is use of this
        def __init__(self,type,arrival_time):
            self.type = type #!! what is this what are the types? arrival or departure?
            self.arrival_time = arrival_time #!! arrival time of a client which is a packet ?

    class Server(object):
        def __init__(self):
            self.idle = True

    def Arrival(self,time, queue):
        # cumulate statistics
        self.data.arr += 1 #!! increment number of arrivals
        self.data.ut += self.users*(time - self.data.oldT) #!! utilization = number of users * time
        self.data.oldT = time #!! what is this? the time when this one entered the system -> later it will be used to calculate the utilization

        # sample the time until the next event
        inter_arrival = random.expovariate(lambd=1/self.arrival) #!! inter arrival time is exponential with lambda = 1/arrival rate (lambda is the rate of the exponential distribution) - this is the time until the next arrival event occurs
        #schedule the next arrival
        self.FES.put((time + inter_arrival, "arrival")) #!! put the next arrival event in the future event scheduler
        self.users += 1
        client = self.Client(self.type1,time) #!! create a client with type 1 and arrival time = time

        #check the buffer size before putting the packet in the queue
        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            #if the buffer is full we increment the number of drops
            self.data.drop += 1
            self.users -= 1

        # start service if the server is idle and the queue is not empty (there is a packet to serve)
        #avoid duplication on service
        if self.users==1:
            service_time = random.uniform(1.0,self.service)# sample the service time
            self.FES.put((time + service_time, "departure")) # schedule the departure - when the packet is served and leaves the system

    def Departure(self,time, queue):
        # cumulate statistics
        self.data.dep += 1
        self.data.ut += self.users*(time-self.data.oldT)
        self.data.oldT = time
        client = queue.pop(0) #!! pop the first packet from the queue why? because it is the first one that entered the system and it is the first one that will leave the system - FIFO
        self.data.delay += (time-client.arrival_time) #!! calculate the delay of the packet in the system
        self.users -= 1

        if self.users >0:
            #if there are more packets to serve - schedule the departure of the next one - when this one leaves the system
            service_time = random.expovariate(1/self.service)
            self.FES.put((time + service_time, "departure"))