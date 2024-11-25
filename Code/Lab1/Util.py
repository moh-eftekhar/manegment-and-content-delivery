from queue import PriorityQueue
import matplotlib.pyplot as plt
import random

def execute(Entry):
    Entry.users = 0
    Entry.result= {}
    Entry.data = Entry.Measure(0,0,0,0,0,0)
    Entry.MM1 = []
    Entry.time = 0
    
    Entry.FES = None
    Entry.FES = PriorityQueue()

    Entry.FES.put((0, "arrival"))

    while Entry.time < Entry.sim_time: # Simulation time
        (Entry.time, Entry.event_type) = Entry.FES.get() # get next event from FES - it can be arrival or departure

        if Entry.event_type == "arrival":
            Entry.Arrival(Entry.time, Entry.MM1) # call the Arrival function

        elif Entry.event_type == "departure":
            Entry.Departure(Entry.time, Entry.MM1) # call the Departure function

    return {
        "N_User_Queue": Entry.users,
        "No.Arr": Entry.data.arr,
        "No.Dep": Entry.data.dep,
        "Dropped": Entry.data.drop,
        "Loss_Prob": Entry.data.drop / Entry.data.arr,
        "Buff_Size": Entry.max_buffer_size if Entry.max_buffer_size != float("inf") else "infinite",
        "Load": Entry.load,
        "Arr_Rate": Entry.data.arr / Entry.time,
        "Dep_Rate": Entry.data.dep / Entry.time,
        "Avg_Users": Entry.data.ut / Entry.time,
        "Avg_Delay": Entry.data.delay / Entry.data.dep,
        "Act_Q": len(Entry.MM1)
    }


def multiExecutor(Entry):
        Entry.data = Entry.Measure()
        Entry.result = {}
        Entry.MM1 = []
        Entry.time = 0
        Entry.FES = PriorityQueue()
        Entry.Server1 = Entry.Server()
        Entry.Server2 = Entry.Server()
        Entry.FES.put((0, "arrival"))

        while Entry.time < Entry.sim_time:
            (Entry.time, Entry.event_type, *server) = Entry.FES.get()

            if Entry.event_type == "arrival":
                if Entry.Server1.users <= Entry.Server2.users: # choose the server with the least users
                    Entry.Arrival(Entry.time, Entry.MM1, Entry.Server1) # call the Arrival function for server 1
                else:
                    Entry.Arrival(Entry.time, Entry.MM1, Entry.Server2) # call the Arrival function for server 2

            elif Entry.event_type == "departure":
                Entry.Departure(Entry.time, Entry.MM1, server[0]) # call the Departure function

        Entry.users = Entry.Server1.users + Entry.Server2.users # total number of users in the system
        return {
            "N_User_Queue": Entry.users,
            "No.Arr": Entry.data.arr,
            "No.Dep": Entry.data.dep,
            "Dropped": Entry.data.drop,
            "Loss_Prob": Entry.data.drop / Entry.data.arr,
            "Buff_Size": Entry.max_buffer_size if Entry.max_buffer_size != float("inf") else "infinite",
            "Load": Entry.load,
            "Arr_Rate": Entry.data.arr / Entry.time,
            "Dep_Rate": Entry.data.dep / Entry.time,
            "Avg_Users": Entry.data.ut / Entry.time,
            "Avg_Delay": Entry.data.delay / Entry.data.dep,
            "Act_Q": len(Entry.MM1)
        }


def multiExecutor3(Entry, type="first"):
        Entry.data = Entry.Measure()
        Entry.result = {}
        Entry.MM1 = []
        Entry.time = 0
        Entry.FES = PriorityQueue()
        Entry.Server1 = Entry.Server(Entry.service * 0.5)
        Entry.Server2 = Entry.Server(Entry.service)
        Entry.Server3 = Entry.Server(Entry.service * 1.5)
        Entry.Server4 = Entry.Server(Entry.service * 2)
        Entry.FES.put((0, "arrival")) # put the first arrival to FES to initialize the simulation

        if type == "second" or "third": # Round Robin or Fastest Server
            Entry.last_assigned_server = -1 # last assigned server - first time it's non of them
            Entry.servers = [Entry.Server1, Entry.Server2, Entry.Server3, Entry.Server4] # list of servers

        if type == "first":
            print("first")
            while Entry.time < Entry.sim_time:
                (Entry.time, Entry.event_type, *server_obj) = Entry.FES.get() # get next event from FES - it can be arrival or departure

                Entry.servers = [Entry.Server1, Entry.Server2, Entry.Server3, Entry.Server4]
                if Entry.event_type == "arrival":
                    selected_server = random.choice(Entry.servers) # Random
                    Entry.Arrival(Entry.time, Entry.MM1, selected_server)
                elif Entry.event_type == "departure":
                    Entry.Departure(Entry.time, Entry.MM1, server_obj[0])
            Entry.users = Entry.Server1.users + Entry.Server2.users + Entry.Server3.users + Entry.Server4.users
                    
        elif type == "second":
            print("second")
            while Entry.time < Entry.sim_time:
                (Entry.time, Entry.event_type, *server_obj) = Entry.FES.get()

                if Entry.event_type == "arrival":
                    Entry.last_assigned_server = (Entry.last_assigned_server + 1) % len(Entry.servers) # Round Robin / ensures that it stays within the range of available servers by wrapping around if necessary.
                    selected_server = Entry.servers[Entry.last_assigned_server] # assign to the next server 
                    Entry.Arrival(Entry.time, Entry.MM1, selected_server)
                elif Entry.event_type == "departure":
                    Entry.Departure(Entry.time, Entry.MM1, server_obj[0])
            Entry.users = Entry.Server1.users + Entry.Server2.users + Entry.Server3.users + Entry.Server4.users

        elif type == "third":
            while Entry.time < Entry.sim_time:
                (Entry.time, Entry.event_type, *server_obj) = Entry.FES.get()

                if Entry.event_type == "arrival":
                    #This ensures that non-idle servers are never selected as the server with the minimum service time. gpt
                    selected_server = min(Entry.servers, key=lambda s: s.service_time if s.idle else float('inf')) #choose the fastest server - if it's idle set it to infinity otherwise set it to the service time - infinity is always bigger than any number

                    if not selected_server.idle:
                        Entry.last_assigned_server = (Entry.last_assigned_server + 1) % len(Entry.servers) # assign to the next server
                        selected_server = Entry.servers[Entry.last_assigned_server]
                    Entry.Arrival(Entry.time, Entry.MM1, selected_server)

                elif Entry.event_type == "departure":
                    Entry.Departure(Entry.time, Entry.MM1, server_obj[0])

        return {
            "N_User_Queue": Entry.users,
            "No.Arr": Entry.data.arr,
            "No.Dep": Entry.data.dep,
            "Dropped": Entry.data.drop,
            "Loss_Prob": Entry.data.drop / Entry.data.arr,
            "Buff_Size": Entry.max_buffer_size if Entry.max_buffer_size != float("inf") else "infinite",
            "Load": Entry.load,
            "Arr_Rate": Entry.data.arr / Entry.time,
            "Dep_Rate": Entry.data.dep / Entry.time,
            "Avg_Users": Entry.data.ut / Entry.time,
            "Avg_Delay": Entry.data.delay / Entry.data.dep,
            "Act_Q": len(Entry.MM1)
        }


def multiExecutor4(Entry):
        Entry.users = 0
        Entry.result= {}
        Entry.data = Entry.Measure(0,0,0,0,0,0)
        Entry.MM1 = []
        Entry.time = 0
        Entry.FES = None
        Entry.FES = PriorityQueue()
        Entry.FES.put((0, "arrival"))
        while Entry.time < Entry.sim_time:
            (Entry.time, Entry.event_type) = Entry.FES.get()

            if Entry.event_type == "arrival":
                Entry.Arrival(Entry.time, Entry.MM1)

            elif Entry.event_type == "departure":
                Entry.Departure(Entry.time, Entry.MM1)
        
        return {
            "N_User_Queue": Entry.users,
            "No.Arr": Entry.data.arr,
            "No.Dep": Entry.data.dep,
            "Dropped": Entry.data.drop,
            "Loss_Prob": Entry.data.drop / Entry.data.arr,
            "Buff_Size": Entry.max_buffer_size if Entry.max_buffer_size != float("inf") else "infinite",
            "Load": Entry.load,
            "Arr_Rate": Entry.data.arr / Entry.time,
            "Dep_Rate": Entry.data.dep / Entry.time,
            "Avg_Users": Entry.data.ut / Entry.time,
            "Avg_Delay": Entry.data.delay / Entry.data.dep,
            "Act_Q": len(Entry.MM1)
        }

def draw(saveTitle,title, x, x_label, y, y_label):
    plt.figure().clear()
    plt.title(title)
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # plt.show()
    plt.savefig(saveTitle + ".png")
    plt.clf()