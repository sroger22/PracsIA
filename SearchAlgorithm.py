# This file contains all the required routines to make an A* search algorithm.
#
__authors__='MariaXaviAnna'
__group__='DL00'
# _________________________________________________________________________________________
# Intel.ligencia Artificial 
# Grau en Enginyeria Informatica
# Curs 2015-2016
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

from SubwayMap import *
from math import fabs,sqrt



class Node:
    # __init__ Constructor of Node Class.
    def __init__(self, station, father):
        """
        __init__: 	Constructor of the Node class
        :param
                - station: STATION information of the Station of this Node
                - father: NODE (see Node definition) of his father
        """
        
        self.station = station      # STATION information of the Station of this Node
        self.g = 0                  # REAL cost - depending on the type of preference -
                                    # to get from the origin to this Node
        self.h = 0                  # REAL heuristic value to get from the origin to this Node
        self.f = 0                  # REAL evaluate function
        self.parentsID = []         # TUPLE OF NODES (from the origin to its father)
        self.father = father        # NODE pointer to his father
        self.time = 0               # REAL time required to get from the origin to this Node
                                    # [optional] Only useful for GUI
        self.num_stopStation = 0    # INTEGER number of stops stations made from the origin to this Node
                                    # [optional] Only useful for GUI
        self.walk = 0               # REAL distance made from the origin to this Node
                                    # [optional] Only useful for GUI
        self.transfers = 0          # INTEGER number of transfers made from the origin to this Node
                                    # [optional] Only useful for GUI


    def setEvaluation(self):
        """
        setEvaluation: 	Calculates the Evaluation Function
        :returns
                - f: REAL evaluate function
        """

        self.f = self.g + self.h


    def setHeuristic(self, typePreference, node_destination,city):
        """"
        setHeuristic: 	Calculates the heuristic depending on the preference selected
        :params
                - typePreference: INTEGER Value to indicate the preference selected: 
                                0 - Null Heuristic
                                1 - minimum Time
                                2 - minimum Distance 
                                3 - minimum Transfers
                                4 - minimum Stops
                - node_destination: PATH of the destination station
                - city: CITYINFO with the information of the city (see CityInfo class definition)
        """
        
        if typePreference == 0:
            print "Null Heusrisitc"
        elif typePreference == 1:
            #Minim time
            distance = minimDistance(self.station, node_destination.station)
            velocity = city.max_velocity 
            self.h = distance/velocity
            
        elif typePreference == 2:
            #Minim distance
            self.h = minimDistance(self.station, node_destination.station)
            
        elif typePreference == 3:
            #Minim transfer
            if self.station.line == node_destination.station.line:
                self.h = 0
            else:
                self.h = city.min_transfer
            
        elif typePreference == 4:
            #Minim stop
            if self.station.destinationDic.has_key(node_destination.station.id):
                if minimDistance(self.station, node_destination.station) == 0:
                    self.h = 0
                else:
                    self.h = 1
            else:
                self.h = 2

    def setRealCost(self,  costTable):
        """
        setRealCost: 	Calculates the real cost depending on the preference selected
        :params
                 - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
                             cost can be in terms of any preference.
        """
        if self.father != None:
            self.g = costTable[self.father.station.id][self.station.id] + self.father.g


    def __repr__(self):
        return str(self.station.id)




def Expand(fatherNode, stationList, typePreference, node_destination, costTable,city):
    """
        Expand: It expands a node and returns the list of connected stations (childrenList)
        :params
                - fatherNode: NODE of the current node that should be expanded
                - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)
                - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Null Heuristic
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
                - node_destination: NODE (see Node definition) of the destination
                - costTable: DICTIONARY. Relates each station with their adjacency an their real cost. NOTE that this
                             cost can be in terms of any preference.
                - city: CITYINFO with the information of the city (see CityInfo class definition)
        :returns
                - childrenList:  LIST of the set of child Nodes for this current node (fatherNode)

    """
    child = []
    for station in fatherNode.station.destinationDic:
        node = Node(stationList[station - 1], fatherNode)
        node.setRealCost(costTable[typePreference])
        node.setHeuristic(typePreference, node_destination, city)
        node.setEvaluation()

        #parentsID
        node.parentsID = list(fatherNode.parentsID)
        node.parentsID.append(fatherNode.station.id)

        #time
        node.time = costTable[1][fatherNode.station.id ][station] + fatherNode.time
        #walk
        node.walk = costTable[2][fatherNode.station.id ][station] + fatherNode.walk
        #Transfers
        node.transfers = costTable[3][fatherNode.station.id ][station] + fatherNode.transfers
        #Stops
        node.num_stopStation = costTable[4][fatherNode.station.id][station] + fatherNode.num_stopStation

        child.append(node)

    return child


def RemoveCycles(childrenList):
    """
        RemoveCycles: It removes from childrenList the set of childrens that include some cycles in their path.
        :params
                - childrenList: LIST of the set of child Nodes for a certain Node
        :returns
                - listWithoutCycles:  LIST of the set of child Nodes for a certain Node which not includes cycles
    """
    listWithoutCycles = []
    for i in childrenList:
        print "ID:", i.station.id,"Parents:", i.parentsID
        if not i.station.id in i.parentsID:
            listWithoutCycles.append(i)
        else:
            print "Cycle removed"
    return listWithoutCycles



def RemoveRedundantPaths():
    """
        RemoveRedundantPaths:   It removes the Redundant Paths. They are not optimal solution!
                                If a node is visited and have a lower g in this moment, TCP is updated.
                                In case of having a higher value, we should remove this child.
                                If a node is not yet visited, we should include to the TCP.
        :params

        :returns

    """







def setCostTable( typePreference, stationList,city):
    """
    setCostTable :      Real cost of a travel.
    :param
            - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)
            - city: CITYINFO with the information of the city (see CityInfo class definition)
    :return:
            - costTable: DICTIONARY. Relates each station with their adjacency an their g, depending on the
                                 type of Preference Selected.
    """
    costTable = {}

    #Adjacency
    if typePreference == 0:
        for i in city.adjacency.keys():
            for j in city.adjacency[i].keys():

                if costTable.has_key(i):
                    costTable[i][j] = 1
                else:
                    costTable[i] = {}
                    costTable[i][j] = 1
                    
    #Minimum time             
    elif typePreference == 1:
        for i in city.adjacency.keys():
            for j in city.adjacency[i].keys():
                if costTable.has_key(i):
                    costTable[i][j] = stationList[i - 1].destinationDic[j]
                else:
                    costTable[i] = {}
                    costTable[i][j] = stationList[i - 1].destinationDic[j]                
    #Minimum distance           
    elif typePreference == 2:
        for i in city.adjacency.keys():
            for j in city.adjacency[i].keys():
                distance = minimDistance(stationList[i-1], stationList[j-1])
                if costTable.has_key(i):
                    costTable[i][j] = distance
                else:
                    costTable[i] = {}
                    costTable[i][j] = distance
    #Minimum transfer           
    elif typePreference == 3:
        for i in city.adjacency.keys():
            for j in city.adjacency[i].keys():
                if minimDistance(stationList[i-1], stationList[j-1]) == 0:
                    
                    if costTable.has_key(i):
                        costTable[i][j] = stationList[i-1].destinationDic[j]
                    else:
                        costTable[i] = {}
                        costTable[i][j] = stationList[i-1].destinationDic[j]
                else:
                    if costTable.has_key(i):
                        costTable[i][j] = 0
                    else:
                        costTable[i] = {}
                        costTable[i][j] = 0
    #Minim stops               
    elif typePreference == 4:
        for i in city.adjacency.keys():
            for j in city.adjacency[i].keys():
                if minimDistance(stationList[i-1], stationList[j-1]) == 0:
                    
                    if costTable.has_key(i):
                        costTable[i][j] = 0
                    else:
                        costTable[i] = {}
                        costTable[i][j] = 0
                else:
                    if costTable.has_key(i):
                        costTable[i][j] = 1
                    else:
                        costTable[i] = {}
                        costTable[i][j] = 1

    return costTable




def coord2station(coord, stationList):
    """
    coord2station :      From coordinates, it searches the closest station.
    :param
            - coord:  LIST of two REAL values, which refer to the coordinates of a point in the city.
            - stationList: LIST of the stations of a city. (- id, destinationDic, name, line, x, y -)

    :return:
            - possible_origins: List of the Indexes of the stationList structure, which corresponds to the closest
            station
    """
    x,y = coord
    node = Station(0,0,0,x,y)
    stations = [stationList[0].id - 1]
    min = minimDistance(node, stationList[0])
    stationList = iter(stationList)
    next(stationList)

    for i in stationList:
        distance = minimDistance(node, i)
        if min > distance:
            min = distance
            stations = []
            stations.append(i.id - 1)
        else:
            if min == distance:
                stations.append(i.id - 1)

    return stations[0]


def AstarAlgorithm(stationList, coord_origin, coord_destination, typePreference,city,flag_redundants):
    """
     AstarAlgorithm: main function. It is the connection between the GUI and the AStar search code.
     INPUTS:
            - stationList: LIST of the stations of a city. (- id, name, destinationDic, line, x, y -)
            - coord_origin: TUPLE of two values referring to the origin coordinates
            - coord_destination: TUPLE of two values referring to the destination coordinates
            - typePreference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
                                4 - minimum Stops
            - city: CITYINFO with the information of the city (see CityInfo class definition)
    OUTPUTS:
            - time: REAL total required time to make the route
            - distance: REAL total distance made in the route
            - transfers: INTEGER total transfers made in the route
            - stopStations: INTEGER total stops made in the route
            - num_expanded_nodes: INTEGER total expanded nodes to get the optimal path
            - depth: INTEGER depth of the solution
            - visitedNodes: LIST of INTEGERS, IDs of the stations corresponding to the visited nodes
            - idsOptimalPath: LIST of INTEGERS, IDs of the stations corresponding to the optimal path
            (from origin to destination)
            - min_distance_origin: REAL the distance of the origin_coordinates to the closest station
            - min_distance_destination: REAL the distance of the destination_coordinates to the closest station
            - flag_redundants: [0/1]. Flag to indicate if the algorithm has to remove the redundant paths (1) or not (0)


            EXAMPLE:
            return optimalPath.time, optimalPath.walk, optimalPath.transfers,optimalPath.num_stopStation,
            len(expandedList), len(idsOptimalPath), visitedNodes, idsOptimalPath, min_distance_origin,
            min_distance_destination
    """
    typePreference = int(typePreference)

    costAdjacencyTable = setCostTable(0, stationList, city)
    costTimeTable = setCostTable(1, stationList, city)
    costDistanceTable = setCostTable(2, stationList, city)
    costTransferTable = setCostTable(3, stationList, city)
    costStopsTable = setCostTable(4, stationList, city)

    costTable = [costAdjacencyTable,costTimeTable,costDistanceTable,costTransferTable,costStopsTable]
    station_origin = stationList[coord2station(coord_origin, stationList)]
    station_destination = stationList[coord2station(coord_destination, stationList)]
    node_start = Node(station_origin, None)
    node_end = Node(station_destination, None)
    llista = [[node_start]]
    visited_nodes = [node_start]
    print llista
    while True:
        cap = llista.pop(0)
        if cap[-1].station == station_destination:
            break
        capNode = cap[-1]
        print "Cap:", capNode
        E = Expand(capNode, stationList, typePreference, node_end, costTable, city)
        E = RemoveCycles(E)
        for i in E:
            llista.append(cap + [i])
            visited_nodes.append(i)
        llista = Insercio_ordenada_f(llista)
        print "Llista:", llista
    if cap != None:
        print "Encontrado!"
        print cap
        definitiu = []
        print costTable[3]
        for i in cap:
            definitiu.append(i.station.id)
        return cap[-1].time,cap[-1].walk,cap[-1].transfers,cap[-1].num_stopStation,len(visited_nodes),len(definitiu),visited_nodes,definitiu,0,0
    else:
        return "No"

def minimDistance(station, destination):
    x = fabs(destination.x - station.x)
    y = fabs(destination.y - station.y)
            
    return sqrt(x*x + y*y)

def Insercio_ordenada_f(llista):
    llista = sorted(llista, key=lambda station: station[-1].f)
    return llista
