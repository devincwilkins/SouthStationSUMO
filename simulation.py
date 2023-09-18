import traci
import re
import numpy as np
import pandas as pd
import timeit
import numpy as np
import random

class Simulation:        
    def __init__(self, TrafficGen, sumo_cmd, start_time, end_time, loading_duration, timestep, schedule):
        #self.sum_waiting_time = 0
        self.sum_queue_length = 0
        self.waiting_times = {}
        self.traffic_gen = TrafficGen
        self.step = 0
        self.sumo_cmd = sumo_cmd
        self.max_steps = end_time - start_time
        self.loading_duration = loading_duration
        self.timestep = timestep
        self.sigDict = {} #lane number: signal to enter the interlocking ("Start" signal)
        self.indDict = {}  #inductor: signal
        self.trackDict = {'Start4':'Track1', 'Start2':'Track5', 'Start6':'TrackDB1','Start7':'TrackDB2','Start9':'TrackOC21'} #"StartX" to "TrackY"
        self.loadingTracksDict = {} #in edge: out edge
        self.route_list = []
        self.loadingTracks = []
        self.arrivalTracks = []
        self.activeRoutes = []
        self.occupied = {}  #edge: True/False
        self.occupied_time = {} #edge: time_step
        self.doneloading = {}  #edge: vehicle
        self.first_waiting = {}  #edge: vehicle
        self.conflictDict = {}  #route: list of conflicting routes
        self.inductors = []
        self.interlockingEdges = []
        self.valid_actions = []
        self.outTrackDict = {'CR-Fair':'TrackDB1','CR-Prov':'Track2','CR-Fran':'Track2', \
                'CR-Midd':'TrackOC19','CR-Worc':'Track7','CR-Need':'Track7', \
                    'CR-Gree':'Track2','CR-King':'TrackOC19','Amtrak_':'Track2','Southco':'TrackOC19'} 
        self.limitedPlatformDict = {'CR-Fair':['L10_in','L11_in','L8_in','L9_in','L2_in'],'CR-Prov':['L3_in','L4_in','L5_in','L6_in','L7_in','L2_in'],'CR-Fran':['L3_in','L4_in','L2_in','L5_in','L6_in','L7_in'], \
                'CR-Midd':['L12_in','L13_in','L11_in','L10_in','L9_in','L8_in','L2_in'],'CR-Worc':['L1_in','L4_in','L10_in'],'CR-Need':['L3_in','L4_in','L2_in','L5_in','L6_in','L7_in','L8_in','L9_in'], \
                    'CR-Gree':['L12_in','L13_in','L11_in','L10_in','L8_in','L9_in','L2_in'],'CR-King':['L12_in','L13_in','L11_in','L10_in','L8_in','L9_in',],'Amtrak_':['L8_in','L9_in'],'Southco':['L12_in','L13_in','L11_in','L10_in','L8_in','L9_in']}  #make these veh attributes in generator.py?
        self.trackassignedcount = np.zeros(13)
        self.donothingcount = 0
        self.output_platform = {}
        self.tv_dict = {}
        self.dv_dict = {}
        self.arr_dict = {}
        self.departures_dict = {}
        lineList = ['CR-Fairmount','CR-Providence','CR-Franklin', \
                'CR-Middleborough','CR-Worcester','CR-Needham' \
                    'CR-Greenbush','CR-Kingston','Amtrak']
        df =  pd.read_csv('schedules/' + schedule)
        print('SCHEDULE IS: ' + schedule)
        departures = df[df['Direction'] == 0].sort_values(by=['Minutes'])
        for line in lineList:
            self.departures_dict[line] = departures[departures['Service'] == 'CR-Worcester'].reset_index()

    def run(self, episode):
        """
        Runs an episode of simulation, then starts a training session
        """
        start_time = timeit.default_timer()

        # generate the route file for this simulation and set up sumo
        self.traffic_gen.generate_routefile(seed=episode)
        traci.start(self.sumo_cmd)

        print("\t [INFO] Start simulating the episode")

        # init time
        self.step = 0
        old_total_wait = 0
            
        #init platforms
        for edge in traci.edge.getIDList():
            if '_in'in edge:
                self.loadingTracks.append(edge)
                self.loadingTracksDict[edge] = ""
                self.doneloading[edge] = ""
                self.occupied[edge] = False
                self.occupied_time[edge] = 0
            if edge[0:5] == "Start":
                self.arrivalTracks.append(edge)
                self.first_waiting[edge] = ""
        
        #init signals
        for signal in traci.trafficlight.getIDList():
            if signal[0:3] == "Ent":
                ctrl = traci.trafficlight.getControlledLanes(signal)
                traci.trafficlight.setRedYellowGreenState(signal, "rrrr")
                for item in ctrl:
                    if item[0:5] == "Start":
                        self.sigDict[item[:-2]] = signal
            elif signal[0:3] == "End":
                #set signal to red
                traci.trafficlight.setRedYellowGreenState(signal, "rrrr")
                ctrl = traci.trafficlight.getControlledLanes(signal)
                for item in ctrl:
                    if '_in' in item:
                        self.sigDict[item[:-2]] = signal
            elif signal[0] == 'S':
                #set signal to red
                state_length = len(traci.trafficlight.getRedYellowGreenState(signal))
                traci.trafficlight.setRedYellowGreenState(signal, 'r' * (state_length // 2) + 'G'*(state_length // 2))
                ctrl = traci.trafficlight.getControlledLanes(signal)
                for item in ctrl:
                    if '_out' in item:
                        self.sigDict[item[:-2]] = signal
            else:
                #set signal to green
                state_length = len(traci.trafficlight.getRedYellowGreenState(signal))
                traci.trafficlight.setRedYellowGreenState(signal, 'G'* state_length)


        #init inductors
        self.inductors = traci.lanearea.getIDList()
        for inductor in self.inductors:
            self.indDict[inductor] = self.sigDict[traci.lanearea.getLaneID(inductor)[:-2]]
        
        #init conflicts
        self.route_list = traci.route.getIDList()
        for edge in traci.edge.getIDList():
            if "Start" not in edge and "_in" not in edge and "_out" not in edge:
                self.interlockingEdges.append(edge)
        for ego_route in self.route_list:
            ego_nodes = []
            for ego_edge in traci.route.getEdges(ego_route):
                if 'to' in ego_edge:
                    node_list = ego_edge.split('to')
                    ego_nodes.append(node_list[0])
                    ego_nodes.append(node_list[1])
            conflict_list = []
            for foe_route in self.route_list:
                foe_nodes = []
                for foe_edge in traci.route.getEdges(foe_route):
                    if 'to' in foe_edge:
                        node_list = foe_edge.split('to')
                        foe_nodes.append(node_list[0])
                        foe_nodes.append(node_list[1])
                if bool(set(ego_nodes) & set(foe_nodes)) == True: 
                    conflict_list.append(foe_route)
            self.conflictDict[ego_route] = conflict_list

        sum_reward = 0
        sum_waiting = 0
        while self.step < self.max_steps:

            # get current state of the intersection
            self.initialize_signals()
            self.update_first_waiting()
            self.get_loading()
            self.assign_platform()
            self.dispatch()
            self.greenlight_assigned()

            # calculate reward of previous action: (change in cumulative waiting time between actions)
            # waiting time = seconds waited by a car since the spawned in the environment,
            current_total_wait = self.collect_waiting_times()
            reward = old_total_wait - current_total_wait 
            
            self.simulate(self.timestep) #make a decision every 1 seconds

            # saving variables for later & accumulate reward
            old_total_wait = current_total_wait

            # saving only the meaningful reward to better see if the agent is behaving correctly
            if reward < 0:
                sum_reward += reward
            sum_waiting += current_total_wait

        avg_waiting = current_total_wait #sum_waiting / self.max_steps
        traci.close()
        simulation_time = round(timeit.default_timer() - start_time, 1)

        trackassigneds = self.trackassignedcount
        donothings = self.donothingcount

        output = pd.DataFrame({'Tv':pd.Series(self.tv_dict),'Dv':pd.Series(self.dv_dict),'Arr':pd.Series(self.arr_dict)})

        return simulation_time, avg_waiting, trackassigneds, donothings, output

    def simulate(self, steps_todo):
        """
        Execute steps in sumo while gathering statistics
        """
        # do not do more steps than the maximum allowed number of steps
        if (self.step + steps_todo) >= self.max_steps:
            steps_todo = self.max_steps - self.step
        if self.step >= self.max_steps -1:
            traci.simulation.clearPending()
            print('pending cleared')
            for vehicle in traci.vehicle.getIDList():
                traci.vehicle.remove(vehicle)
        while steps_todo > 0:
            traci.simulationStep()  # simulate 1 step in sumo
            self.step += 1  # update the step counter
            steps_todo -= 1
            queue_length = self.get_queue_length()
            self.sum_queue_length += queue_length

    def initialize_signals(self):
        """
        Retrieve the name of each signal and initialize to red
        """
        signalList = traci.trafficlight.getIDList()
        for signal in signalList:
            if 'Ent' in signal:
                state_length = len(traci.trafficlight.getRedYellowGreenState(signal))
                traci.trafficlight.setRedYellowGreenState(signal,'r' * state_length)
            elif 'S' in signal:
                #set signal to red
                state_length = len(traci.trafficlight.getRedYellowGreenState(signal))
                traci.trafficlight.setRedYellowGreenState(signal, 'r' * (state_length // 2) + 'G'*(state_length // 2))

    def greenlight_assigned(self):
        """
        Let any assigned vehicles into the interlocking
        """
        awaiting_release = []
        self.get_activeRoutes() 
        for loop in self.inductors:
            awaiting_release = traci.lanearea.getLastStepVehicleIDs(loop)
            if awaiting_release and traci.vehicle.getParameter(awaiting_release[0], "greenlit") == "False" :
                print("Check 1")
                if traci.vehicle.getParameter(awaiting_release[0], "assigned") == "True" or (traci.vehicle.getParameter(awaiting_release[0], "dispatched") == "True" ):
                    # print(self.activeRoutes)
                    print("Check 2")
                    if not bool(set(self.conflictDict[traci.vehicle.getRouteID(awaiting_release[0])]) & set (self.activeRoutes)): #doesnt share elem with self.activeRoutes
                        # self.activeRoutes = []
                        print("Check 3")
                        if traci.vehicle.getRouteID(awaiting_release[0])[0] == 'T':
                            print("Check 4")
                            state_length = len(traci.trafficlight.getRedYellowGreenState(self.indDict[loop]))
                            traci.trafficlight.setRedYellowGreenState(self.indDict[loop], state_length * 'G')
                            traci.trafficlight.setPhaseDuration(self.indDict[loop], 90)
                            if traci.vehicle.getParameter(awaiting_release[0],"origin") != "YARD":
                                self.tv_dict[traci.vehicle.getParameter(awaiting_release[0],"name")] = traci.simulation.getTime()
                            self.activeRoutes.append(traci.vehicle.getRouteID(awaiting_release[0]))
                            traci.vehicle.setParameter(awaiting_release[0], "greenlit", "True")
                        if traci.vehicle.getRouteID(awaiting_release[0])[0] == 'L' and int(traci.vehicle.getParameter(awaiting_release[0], "dep_time")) <= traci.simulation.getTime():
                            state_length = len(traci.trafficlight.getRedYellowGreenState(self.indDict[loop]))
                            traci.trafficlight.setRedYellowGreenState(self.indDict[loop], state_length * 'G')
                            if traci.vehicle.getParameter(awaiting_release[0],"next") != "YARD":
                                self.dv_dict[traci.vehicle.getParameter(awaiting_release[0],"name")] = traci.simulation.getTime()
                            self.activeRoutes.append(traci.vehicle.getRouteID(awaiting_release[0]))
                            self.occupied[traci.lanearea.getLaneID(loop)[0:-5] + 'in'] = False 
                            traci.vehicle.setParameter(awaiting_release[0], "greenlit", "True")
                            print("greenlighting " + awaiting_release[0])
                    else:
                        None
                        # self.activeRoutes = []  

    def collect_waiting_times(self):
        """
        Retrieve the waiting time of every train and return the total waiting time
        """
        train_list = traci.vehicle.getIDList() 
        for train_id in train_list:
            wait_time = traci.vehicle.getAccumulatedWaitingTime(train_id)
            self.waiting_times[train_id] = wait_time
        total_waiting_time = sum(self.waiting_times.values())
        return total_waiting_time

    def update_first_waiting(self):
        """
        Retrieve the first vehicle in list of vehicles waiting on the arrival tracks
        """
        for edge in self.first_waiting:
            if traci.edge.getLastStepVehicleIDs(edge):
                train_list = traci.edge.getLastStepVehicleIDs(edge)
                self.first_waiting[edge] = train_list[-1]
            else:
                self.first_waiting[edge] = ""

    def get_loading(self):
        """
        Retrieve any vehicles ready to be sent back out
        """
        for track in self.loadingTracks:
            if traci.edge.getLastStepVehicleIDs(track):#if there's a vehicle on the edge
                train = traci.edge.getLastStepVehicleIDs(track)[0] #retrieve that vehicle
                if traci.vehicle.getStopState(train) == 1 and traci.vehicle.getParameter(train, "loading") == "False" and traci.vehicle.getParameter(train, "doneloading") == "False":
                    traci.vehicle.setParameter(train, "loading", "True")
                    traci.vehicle.setParameter(train, "greenlit", "False")
                    if traci.vehicle.getParameter(train,"next") != "YARD":
                        traci.vehicle.setColor(train, (255,251,0,255))
                    if traci.vehicle.getParameter(train,"origin") != "YARD":
                        self.arr_dict[traci.vehicle.getParameter(train,"name")] = traci.simulation.getTime()
                        print(traci.vehicle.getParameter(train,"name") + " getting arrival data point")
                    self.transform_trip(train)
                elif traci.vehicle.getStopState(train) == 0 and traci.vehicle.getParameter(train, "loading") == "True":
                    traci.vehicle.setParameter(train, "loading", "False")
                    traci.vehicle.setParameter(train, "doneloading", "True")
                    self.doneloading[track] = train
    
    def get_activeRoutes(self):
        self.activeRoutes = []
        for link in self.interlockingEdges:
            for veh in traci.edge.getLastStepVehicleIDs(link):
                if traci.vehicle.getRouteID(veh) not in self.activeRoutes: 
                    self.activeRoutes.append(traci.vehicle.getRouteID(veh))

    def assign_platform(self):
        #when a train is ready for assignment (has entered the system)
        for edge in self.first_waiting:
            if self.first_waiting[edge] != '':
                train = self.first_waiting[edge]
                for platform in self.limitedPlatformDict[train[0:7]]:
                    if self.occupied[platform] == False and traci.vehicle.getParameter(train, "assigned") == "False": 
                        route = str(self.trackDict[edge.split('to')[0]]) + 'to' + str(platform.split('_')[0]) #"Start4" needs to be "Track1"
                        final_edge = traci.route.getEdges(route)[-2] 
                        traci.vehicle.setRouteID(train, route) 
                        traci.vehicle.setStop(train, final_edge, pos= traci.lane.getLength(final_edge + '_0') - 50, laneIndex=0, duration= self.loading_duration)
                        # print('I choose to send vehicle '+ str(self.first_waiting[edge]) + " to platform "+ str(final_edge))
                        assigned_platform = int(re.search("\d+", final_edge)[0])
                        self.output_platform[self.first_waiting[edge]] = assigned_platform
                        self.trackassignedcount[assigned_platform - 1] += 1
                        self.occupied[final_edge] = True
                        self.occupied_time[final_edge] = self.step
                        traci.vehicle.setParameter(train, "assigned", "True")

    def dispatch(self):
        #When a train has finished loading and is ready to leave the system
        for edge in self.doneloading:
            if self.doneloading[edge] != '':
                train = self.doneloading[edge]
                while traci.vehicle.getParameter(train, "dispatched") == "False":
                    #check if there's a scheduled departure
                    #assign to that departure

                    route = str(edge.split('_')[0]) + 'to' + str(self.outTrackDict[train[0:7]])
                    # print('I choose to send vehicle '+ str(train) + " from platform "+ str(edge))
                    traci.vehicle.setRouteID(train, route) 
                    traci.vehicle.setParameter(train, "dispatched", "True")
                    self.doneloading[edge] = ""

    def get_queue_length(self):
        """
        Retrieve the number of trains with speed = 0 in every incoming lane
        """
        queue_length = 0
        for track in self.arrivalTracks:
            queue_length += traci.edge.getLastStepHaltingNumber(track)
        return queue_length

    def transform_trip(self,train):
        """
        change arrived vehicle into departure vehicle, trigger when loading begins for vehicleA
        """
        nextstate = traci.vehicle.getParameter(train, "next")
        if nextstate != "":
            prefix = train.split('_')[0] + '_'
            traci.vehicle.setParameter(train, "name", prefix + nextstate)
            # print("my new dep time is " + traci.vehicle.getParameter(train, "dep_time") )
        edge = traci.vehicle.getRoadID(train)
        if nextstate == "YARD":
            route = str(edge.split('_')[0]) + 'toTrackOC19'
            traci.vehicle.setRouteID(train, route)
            traci.vehicle.setColor(train, (143,219,255,255))
        #step 1: obtain "Departureslist"
        # if len(self.departures_dict['CR-Worcester']) != 0:
        #     if self.departures_dict['CR-Worcester']['Minutes'].iloc[0] < traci.simulation.getTime():
        #         print("fix late train case: " + str(self.departures_dict['CR-Worcester']['Minutes'].iloc[0]))
        #         traci.vehicle.setParameter(train, "name", "CR-Worcester_" + traci.vehicle.getParameter(train, "next"))
        #         # traci.vehicle.setParameter(train, "name", "CR-Worcester_" + str(self.departures_dict['CR-Worcester']['id'].iloc[0]))
        #         self.departures_dict['CR-Worcester'].drop(index=self.departures_dict['CR-Worcester'].index[0], axis=0, inplace=True)
        #     elif self.departures_dict['CR-Worcester']['Minutes'].iloc[0] - traci.simulation.getTime() < 15:
        #         print("upcoming departure case: " + str(self.departures_dict['CR-Worcester']['Minutes'].iloc[0]))
        #         # traci.vehicle.setRouteID()


            




