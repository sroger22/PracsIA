# Aquest fitxer conte tot el que es necessari per a la cerca A*:
#   - Definicio de la classe Node, corresponent a la definicio dels nodes de l'arbre
#	- Definicio de la cerca A*
#	- Definicio de les heuristiques a utilitzar.
#   - Eliminar Camins Redundants
#   - Eliminar Cicles
# 
# Autors: 
# Grup: 
# _________________________________________________________________________________________
# Intel.ligencia Artificial 
# Grau en Enginyeria Informatica
# Curs 2014 - 2015
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

from MapaMetro import *
from math import *


#calcula distancia euclidiana entre dos puntos origen - destino
def calcularDistancia (originX, originY, destination_X, destination_Y):
    
    difference_x = destination_X-originX
    difference_x = difference_x*difference_x
    difference_y = destination_Y-originY
    difference_y = difference_y*difference_y
	
    return sqrt(difference_x+difference_y)

def expand(CurrentHead, connections, timeTransfers, timeStations, stationList, expandedNodesList, destX, destY, typePreference):

    ExpandedList = []


    for i in connections[CurrentHead[5][0]].keys():
        if stationList[i-1].id not in expandedNodesList:
            
            #print "Estacion adyacente a " + CurrentHead[4].name + " : " + stationList[i-1].name + " con ID: " + str(stationList[i-1].id)+ "\n\n"
            ##TODO: BUSCAR PARA RELLENAR UN NUEVO NODO DE OPTIMAL PATH, DE MOMENTO SOLO TENEMOS ID DE LA ESTACION, CONSEGUIR TODO LO DEMAS
            newNode = [CurrentHead[0]+calcularDistancia(CurrentHead[4].x, CurrentHead[4].y, stationList[i-1].x, stationList[i-1].y), CurrentHead[1]+1, CurrentHead[2] + (timeStations[i][CurrentHead[5][0]]), CurrentHead[3], stationList[i-1], CurrentStationstationList[i-1].id, heuristica(stationList[i-1].x, stationList[i-1].y, destX, destY, typePreference)]
            ExpandedList.insert(0, newNode)
            expandedNodesList.append(stationList[i-1].id)
    
    return ExpandedList, expandedNodesList

#calculo de la heuristica dependiendo de la heuristica seleccionada
def heuristica(origenX, origenY, destX, destY, typePreference):
	
	#si la heuristica seleccionada es min paradas o min transbordos no hay que tener en cuenta la distancia
    if typePreference is 1 or typePreference is 3:	
        return 0

    distance = calcularDistancia(origenX, origenY, destX, destY)
	
    if typePreference is 2: 
	    distance = distance/90
		
    return distance

def OrderList (OptimalPath, typePreference):
    distances = {}
    if typePreference == 0:
    #que tenga en cuenta la heuristica de distancia hasta el objetivo para ordenar la lista
        for i in range(len(OptimalPath)):
            distances[OptimalPath[i][0]+OptimalPath[i][6]] = OptimalPath[i][5][0]
        distances = sorted(distances)
        print "\n\nLista ANTES DE SER ORDENADA\n---------------------------\n"
        print OptimalPath
        for sortedDist in distances:
            pos = 0
            while sortedDist !=  (OptimalPath[pos][0]+OptimalPath[pos][6]):
                pos=pos+1
            OptimalPath.insert(len(OptimalPath), OptimalPath.pop(pos))
        print "\n\nLista DESPUES DE SER ORDENADA\n---------------------------\n"
        print OptimalPath
    
    return OptimalPath

def BuscarEstacion(stationList, coord_origin, coord_destination):
    oritgen = 0
    destino = 0
    distMinOrigen = 999999
    distMinDestino = 999999

    for coord in stationList:
        resX= coord.x - coord_origin[0]
        resX *= resX
        resY = coord.y - coord_origin[1]
        resY *= resY
        distOrigen = sqrt(resX + resY)
        
        if distOrigen < distMinOrigen:
            distMinOrigen = distOrigen
            origen_id = coord.id
        resX = coord.x - coord_destination[0]
        resX *= resX
        resY = coord.y - coord_destination[1]
        resY *= resY
        distDestino = sqrt(resX+resY)
        if distDestino < distMinDestino:
            distMinDestino = distDestino
            destino_id = coord.id
            
    return origen_id, destino_id, distMinOrigen, distMinDestino

def GetInfoEstacion (stationList, id):
    i=0
    while(stationList[i].id != id):
        i+=1
    return stationList[i]


def RemoveCycles(childrenList):
        pass

def RemoveRedundantPaths(childrenList, nodeList, partialCostTable):
        pass

def AstarAlgorithm(stationList, connections, coord_origin, coord_destination, typePreference, timeTransfers,
                   timeStations):
    """
     AstarAlgorithm: main function. It is the connection between the GUI and the AStar search code.
     INPUTS:
            - stationList: LIST of the stations of a city. (- id, name, destinationDic, line, x, y -)
            - connections: DICTIONARY set of possible connections between the stations (REAL connections)
            - coord_origin: TUPLE of two values referring to the origin coordinates
            - coord_destination: TUPLE of two values referring to the destination coordinates
            - typePreference: INTEGER Value to indicate the preference selected: 0 - minimum Distance | 1- minimum Stops | 2- minimum Time | 3 - minimum transfers
            - timeTransfers: DICTIONARY time of transfers between two different lines in a certain station
            - timeStations: DICTIONARY  time that takes the train to go from a station to the other (in the same line)
    OUTPUTS:
            - time: REAL total required time to make the route
            - distance: REAL total distance made in the route
            - transfers: INTEGER total transfers made in the route
            - stopStations: INTEGER total stops made in the route
            - num_expanded_nodes: INTEGER total expanded nodes to get the optimal path
            - depth: INTEGER depth of the solution
            - visitedNodes: LIST of INTEGERS, ID's of the visited nodes
            - min_distance_origin: REAL the distance of the origin_coordinates to the closest station
            - min_distance_destination: REAL the distance of the destination_coordinates to the closest station

            optimalPath.time, optimalPath.walk, optimalPath.transfers, optimalPath.num_stopStation, len(
        expandedList), len(optimalPath.parentsID), visitedNodes, idsOptimalPath, min_distance_origin, min_distance_destination
    """


    origen_id, destino_id, distMinOrigen, distMinDestino = BuscarEstacion(stationList, coord_origin, coord_destination)


    estacionOrigen = GetInfoEstacion(stationList, origen_id) #con el id cojemos la informacion
    estacionDestino = GetInfoEstacion(stationList, destino_id)
    
    print "ESTACIO ORIGEN : " + estacionOrigen.name + " ID: " + str(estacionOrigen.id) + "\n\n"
    print "ESTACIO DESTI : " + estacionDestino.name + "ID: " + str(estacionDestino.id) + "\n\n"

    optimalPath = [[0, 0, 0 , 0 , estacionOrigen, [estacionOrigen.id], 0]]
    expandedNodesList = [estacionOrigen.id]
    
    while (optimalPath[0][5][0] != estacionDestino.id):
        
        pathHead = optimalPath.pop(0)
        expandedPath, expandedNodesList = expand(pathHead, connections, timeTransfers, timeStations, stationList, expandedNodesList, coord_destination[0], coord_destination[1], typePreference)
        for i in range(len(expandedPath)):
            optimalPath.insert(0, expandedPath[i])
        optimalPath = OrderList(optimalPath, typePreference)
        
    print optimalPath
    print "\n\n"
	


    return optimalPath[0][2], optimalPath[0][0], optimalPath[0][3], optimalPath[0][1], len(expandedNodesList), len(optimalPath[0]), expandedNodesList, 0, distMinOrigen, distMinDestino


if __name__ == "__main__":
    main()
