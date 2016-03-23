# AStar development
#  - Node definition
#  - A* search
#  - Heuristics definition
# 
# Authors: Jozef Franzen                 | 1332057
#          Diego Alberto Medina Mauricio | 1307828
#          Arnau Rojas Sayol             | 1271223
# Group:   DV11.01
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2013 - 2014
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

from MapaMetro import *
from math import sqrt

# The distance between a pair of adjacent stations
maxDistance = 112.0
# The speed higher than the highest we can reach travelling in the actual transport system
maxSpeed = 90.0
# The constant such that any real euclidean distance does not have major influence
maxPower = 1000.0
# Speed how many units of distance a person walks in a unit of time
walkSpeed = 4.0

# HEURISTICS
def heuristics(path, destination, typePreference):
	parametre = 1.0
	if typePreference <= 0:
		actual = 0.0
	if typePreference == 1:
		parametre = maxDistance
		actual = len(path["p"]) + (1 if (path["p"][0].name != destination.name) else 0)
	elif typePreference == 2:
		parametre = maxSpeed
		actual = path["t"] + (1 if (path["p"][0].name != destination.name) else 0)
	elif typePreference == 3:
		parametre = maxPower
		actual = path["c"] + (1 if (path["p"][0].line != destination.line) else 0)
	if typePreference != -1:
		actual += path["d"]/parametre
	return sqrt((path["p"][0].x - destination.x)**2 + (path["p"][0].y - destination.y)**2) / parametre + actual

def StationByXY(coords, stationList):
	nearer = -1
	nearest = []
	manhattan = -1
	for station in stationList:
		manhattan = abs(coords[0] - station.x) + abs(coords[1] - station.y)
		if (manhattan < nearer) or (nearer == -1):
			nearer = manhattan
			nearest = [{"c": 0, "d": nearer, "t": nearer/walkSpeed, "p": [station]}]
		elif manhattan == nearer:
			nearest.append({"c": 0, "d": nearer, "t": nearer/walkSpeed, "p": [station]})
	return nearest

def Expand(pathList, connections, stationList):
	path = pathList[0]
	if (len(connections[path["p"][0].id].keys()) == 1) or not connections.has_key(path["p"][0].id):
		if (connections[path["p"][0].id].keys()[0] in [station.id for station in path["p"]]) or not connections.has_key(path["p"][0].id):
			del pathList[0]
			return Expand(pathList, connections, stationList)
	result = [{"c": path["c"], "d": path["d"], "t": path["t"], "p": [stationList[connection-1]] + path["p"]} for connection in connections[path["p"][0].id].keys()]
	del pathList[0]
	return result

def Evaluate(childrenList, timeStation, timeConnections):
	for path in childrenList:
		if path["p"][0].line <> path["p"][1].line:
			path["c"] += 1
		path["d"] += heuristics(path, path["p"][1], -1)
		if timeStation.has_key(path["p"][0].id):
			if timeStation[path["p"][0].id].has_key(path["p"][1].id):
				path["t"] += timeStation[path["p"][0].id][path["p"][1].id]
		if timeConnections.has_key(path["p"][0].id):
			if timeConnections[path["p"][0].id].has_key(path["p"][1].id):
				path["t"] += timeConnections[path["p"][0].id][path["p"][1].id]

# RemoveRedundantPaths: It removes the Redundant Paths. They are not optimal solution!
# If a node is visited and have a lower cost in this moment, TCP is updated. In case of having a higher value, we should remove this child.
# If a node is not yet visited, we should include to the TCP.
def RemoveRedundantPaths(childrenList, nodeList, partialCostTable, typePreference):
	redundantPaths = []
	evaluatedCost = -1
	for path in childrenList:
		if typePreference == 0:
			evaluatedCost = path["d"]
		elif typePreference == 1:
			evaluatedCost = len(path["p"])
		elif typePreference == 2:
			evaluatedCost = path["t"]
		elif typePreference == 3:
			evaluatedCost = path["c"]
		if not partialCostTable.has_key(path["p"][0].id) or (partialCostTable[path["p"][0].id] > evaluatedCost):
			partialCostTable[path["p"][0].id] = evaluatedCost
		elif partialCostTable[path["p"][0].id] < evaluatedCost:
			redundantPaths.append(path)
	for path in redundantPaths:
		childrenList.remove(path)

# RemoveCycles: It removes from childrenList the set of childrens that include some cycles in their path.
# It returns a list of childs that not include cycles in their paths.
def RemoveCycles(childrenList):
	cycles = []
	for path in childrenList:
		if len(path["p"]) != len(set(path["p"])):
			cycles.append(path)
	for path in cycles:
		childrenList.remove(path)

def Insert_InOrder(childrenList, nodeList, destination, typePreference):
	for path in childrenList:
		pathAStar = heuristics(path, destination, typePreference)
		if len(nodeList) != 0:
			for i, way in enumerate(nodeList):
				wayAStar = heuristics(way, destination, typePreference)
				if pathAStar >= wayAStar:
					if i == len(nodeList)-1:
						nodeList.append(path)
						break
					continue
				else:
					nodeList.insert(i, path)
					break
		else:
			nodeList.append(path)

# AstarAlgorithm: main function. It is the connection between the GUI and the AStar search code.
#
#  INPUTS:
#   - stationList:	list of the stations of a city (- id, name, line, x, y -)
#   - connections:	dictionary set of possible connections between the stations
#   - coord_origin:	list of two values referring to the origin coordinates
#   - coord_destination: list of two values referring to the destination coordinates
#   - typePreference:	value to indicate the preference selected: 0 - minimum Distance | 1 - minimum Stops | 2 - minimum Time | 3 - minimum Connections
#   - timeConnections:	dictionary including the time of connections between two different lines in a certain station
#   - timeStation:	dictionary including the time of connections between two different stations
#
#  OUTPUTS:
#   - time:		required time to make the route
#   - distance:		total distance made in the route
#   - connections:	total connections between different lines in the route
#   - stopStations:	total stops made in the route
#   - expandedNodes:	total expanded nodes to get the optimal path
#   - expandedList:	list of the expanded nodes to get the optimal path
#   - idCamins:		list of the station IDs of the optimal path
#   - min_distance_origin: the distance of the origin_coordinates to the closest station 
#   - min_distance_destination: the distance of the destination_coordinates to the closest station
#   - num_depth:	depth of the solution we have found
def AstarAlgorithm(stationList, connections, coord_origin, coord_destination, typePreference, timeConnections, timeStation):
	typePreference = int(typePreference)
	time = 0
	distance = 0
	num_depth = 0
	stopStations = 0
	expandedNodes = 0
	expandedList = []
	costTable = {}
	idCamins = []

	expandedList = StationByXY(coord_origin, stationList)
	destinations = StationByXY(coord_destination, stationList)

	destination = {"c": 0, "d": destinations[0]["d"], "t": destinations[0]["t"], "s": [destination["p"][0] for destination in destinations]}
	min_distance_origin = expandedList[0]["d"]
	min_distance_destination = destination["d"]

	while (expandedList != []) and (expandedList[0]["p"][0] not in destination["s"]):
		expH = Expand(expandedList, connections, stationList)
		RemoveCycles(expH)
		Evaluate(expH, timeStation, timeConnections)
		RemoveRedundantPaths(expH, expandedList, costTable, typePreference)
		Insert_InOrder(expH, expandedList, destination["s"][0], typePreference)
	if expandedList != []:
		idCamins = [station.id for station in expandedList[0]["p"]]
		idCamins.reverse()
		time = expandedList[0]["t"] + min_distance_destination/walkSpeed
		distance = expandedList[0]["d"] + min_distance_destination
		connections = expandedList[0]["c"]
		stopStations = len(idCamins)
		expandedNodes = 0
		expandList = []
		num_depth = len(idCamins)
		for path in expandedList:
			expandedNodes += len(path["p"])
			expandList.append([station.id for station in path["p"]])
			if len(path["p"]) > num_depth:
				num_depth = len(path["p"])
		return time, distance, connections, stopStations, expandedNodes, expandList, idCamins, min_distance_origin, min_distance_destination, num_depth