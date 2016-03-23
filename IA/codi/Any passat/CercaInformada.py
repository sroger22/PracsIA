# AStar development
# 	- Node deffinition
#	- A* search
#	- Heurisitcs deffinition
#
# 
# Authors: 
# Group: 
# _________________________________________________________________________________________
# Intel.ligencia Artificial 
# Grau en Enginyeria Informatica
# Curs 2013 - 2014
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

from MapaMetro import *
from math import *

def findStations (stationList, originCoord, destCoord):
        origen = 0
        desti = 0
        dstOrigen = 9999999
        dstDesti = 9999999

        for i in stationList:
                varx = i.x-originCoord[0]
                varx *= varx
                vary = i.y-originCoord[1]
                vary *= vary
                varx += vary 
                if varx < dstOrigen:
                        dstOrigen = varx
                        origen = i.id
                varx = i.x-destCoord[0]
                varx *= varx
                vary = i.y-destCoord[1]
                vary *= vary
                varx += vary
                if varx < dstDesti:
                        dstDesti = varx
                        desti = i.id
        return origen, desti, sqrt(dstOrigen), sqrt(dstDesti)

def buscarEstacio (stationList, id):
        i = 0
        while stationList[i].id != id: i += 1
        return stationList[i]

def calcularDistancia (origenX, origenY, destX, destY):
        varx = destX-origenX
        varx *= varx
        vary = destY-origenY
        vary *= vary
        return sqrt(varx+vary)

def heuristica(origenX, origenY, destX, destY, typePreference):
        if typePreference == 1 or typePreference == 3:
                return 0
        h = calcularDistancia(origenX, origenY, destX, destY)
        if typePreference == 2: h /= 90
        return h

def buscarPos (l, id):
        i = 0
        while i < len(l) and l[i][4] != id: i += 1
        if i == len(l): return -1
        return i

def insertar (l, node, typePreference):
        i = 0;
        while i < len(l) and (l[i][typePreference] + l[i][6]) < (node[typePreference]+node[6]): i += 1
        l.insert(i, node)

# AstarAlgirthm: main function. It is the connection between the GUI and the AStar search code.
# 		INPUTS:
#			- stationList: list of the stations of a city. (- id, name, line, x, y -)
#			- connections: Dictionary set of possible connections between the stations. 
#			- coord_origin: list of two values referring to the origin coordinates
#			- coord_destination: list of two values referring to the destination coordinates 
#			- typePreference: Value to indicate the preference selected: 0 - minimum Distance | 1- minimum Stops | 2- minimum Time | 3 - minimum Connections
#			- timeConnections: Dictionary including the time of connections between two different lines in a certain station 
#			- timeStation: Dictionary including the time of connections between two different stations.
#		OUTPUTS:
#			- time: required time to make the route
#			- distance: total distance made in the route
#			- connections: total connections between different lines in the route
#			- stopStations: total stops made in the route
#			- expandedNodes: total expanded nodes to get the optimal path
#			- expandedList:  list of the expanded nodes to get the optimal path
#			- idCamins: List of the Station IDs of the optimal Path
#			- min_distance_origin: the distance of the origin_coordinates to the closest station 
#			- min_distance_destination: the distance of the destination_coordinates to the closest station
def AstarAlgorithm(stationList, connections,coord_origin,coord_destination,typePreference, timeConnections, timeStation):
        typePreference = int(typePreference)
        origen, desti, min_distance_origin, min_distance_destination = findStations(stationList, coord_origin, coord_destination)
        estacio = buscarEstacio(stationList, origen)
        estacioDesti = buscarEstacio(stationList, desti)
        expandedNodes = 0
        expandedList = []

        expandits = []
        trobats = [[0, 0, 0, 0, origen, -1, heuristica(estacio.x, estacio.y, estacioDesti.x, estacioDesti.y, typePreference)]]

        while trobats[0][4] != desti:
                expandedNodes += 1
                expandedList.append(trobats[0][4])
                expandits.insert(0, trobats.pop(0))
                estacio = buscarEstacio(stationList, expandits[0][4])
                
                if expandits[0][4] in timeConnections.keys():
                        for i in timeConnections[expandits[0][4]].keys():
                                nouNode = [expandits[0][0], expandits[0][1], expandits[0][2]+timeConnections[expandits[0][4]][i], expandits[0][3]+1, i, expandits[0][4], expandits[0][6]]
                                pos = buscarPos(expandits, i)
                                if pos != -1:
                                        if nouNode[typePreference] < expandits[pos][typePreference]:
                                                expandits.pop(pos)
                                                insertar(trobats, nouNode, typePreference)
                                else:
                                        pos = buscarPos(trobats, i)
                                        if pos != -1:
                                                if nouNode[typePreference] < trobats[pos][typePreference]:
                                                        trobats.pop(pos)
                                                        insertar(trobats, nouNode, typePreference)
                                        else: insertar(trobats, nouNode, typePreference)

                if expandits[0][4] in timeStation.keys():
                        for i in timeStation[expandits[0][4]].keys():
                                estacio2 = buscarEstacio(stationList, i)
                                nouNode = [expandits[0][0]+calcularDistancia(estacio.x, estacio.y, estacio2.x, estacio2.y), expandits[0][1]+1, expandits[0][2]+timeStation[expandits[0][4]][i], expandits[0][3], i, expandits[0][4], 0]
                                pos = buscarPos(expandits, i)
                                if pos != -1:
                                        if nouNode[typePreference] < expandits[pos][typePreference]:
                                                nouNode[6] = expandits[pos][6]
                                                expandits.pos(pos)
                                                insertar(trobats, nouNode, typePreference)
                                else:
                                        pos = buscarPos(trobats, i)
                                        if pos != -1:
                                                if nouNode[typePreference] < trobats[pos][typePreference]:
                                                        nouNode[6] = trobats[pos][6]
                                                        trobats.pop(pos)
                                                        insertar(trobats, nouNode, typePreference)
                                        else:
                                                nouNode[6] = heuristica(estacio2.x, estacio2.y, estacioDesti.x, estacioDesti.y, typePreference)
                                                insertar(trobats, nouNode, typePreference)

        cami = [desti]
        pos = buscarPos(expandits, trobats[0][5])
        prof = 0
        while pos != -1:
                prof += 1
                cami.insert(0, expandits[pos][4])
                pos = buscarPos(expandits, expandits[pos][5])

        return trobats[0][2], trobats[0][0], trobats[0][3], trobats[0][1], expandedNodes, expandedList, cami, min_distance_origin, min_distance_destination, prof
