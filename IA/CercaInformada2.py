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


def Cap(lista):
    cap1 = lista[0]
    return cap1

def BuscarEstacion(stationList, coord_origin, coord_destination):
    oritgen = 0
    destino = 0
    distMinOrgien = 999999
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

def Expandir():
    pass
    
def RemoveCycles(childrenList):
    pass
    #for pathRem in childrenList:
        
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

    i = 0
    while (stationList[i].x is not coord_origin[0]) and (stationList[i].y is not coord_origin[1]) and (i < len(stationList)):
        i+=1
    estacionOrigen = stationList[i]
    print estacionOrigen.name
    i = 0
    while (stationList[i].x is not coord_destination[0]) and (stationList[i].y is not coord_destination[1]) and (i < len(stationList)):
        i+=1
    estacionDestino = stationList[i]
    print estacionDestino.name

    print timeTransfers
    
    origen_id, destino_id, distMinOrigen, distMinDestino = BuscarEstancion(stationList, coord_origin, coord_destination)
    infoStationOrigen = GetInfoEstacion(stationList, origen_id) #con el id cojemos la informacion
    infoStationDestino = GetInfoEstacion(stationList, desti_id)
    
    lista = []
    lista.append([estacionOrigen])
    while (lista[0][0] != estacionDestino):
        cap = lista[0]
        expa
      




        
if __name__ == "__main__":
    main()
    
