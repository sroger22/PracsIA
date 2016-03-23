# AStar development
#   - Node deffinition
#   - A* search
#   - Heurisitcs deffinition
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

from LinkedList import *
from MapaMetro import *
from copy import *
import math


time = 0
distance = 0
connections = 0
stopStations = 0
expanded_nodes = 0
llista_nodes = [4,2,5,7]
path = [9,3,4,2]
min_distance_origin = 0
min_distance_destination = 0
num_depth = 0

def originStation(stationList, coord_origin):
    distanceOrigin = 1000

    for station in stationList:
        minimO = math.sqrt((station.x-coord_origin[0])**2 + (station.y-coord_origin[1])**2)
       
        if minimO < distanceOrigin:
            distanceOrigin= minimO
            station_origen = station

    temps = distanceOrigin/4

    return station_origen, temps


def destinationStation(stationList, coord_destination):
    distanceDestination = 1000
        
    for station in stationList:
        minimD = math.sqrt((station.x-coord_destination[0])**2 + (station.y-coord_destination[1])**2)

        if minimD < distanceDestination:
            distanceDestination = minimD
            station_destino = station

    temps = distanceDestination / 4

    return station_destino, temps

# RemoveRedundantPaths: It remove the Redundant Paths. They are not optimal
#solution!
# If a node is visited and have a lower cost in this moment, TCP is updated.
#In case of having a higher value, we should remove this child. 
# If a node is not yet visited, we should include to the TCP.
def RemoveRedundantPaths(childrenList, nodeList,partialCostTable):
        pass

# RemoveCycles: It removes from childrenList the set of Childrens that include
#some cycles in their path. 
# It returns a list of childs that not include cycles in their paths.           
def RemoveCycles(childrenList):
        temp=childrenList.getHead()
        recorrer=temp.getNext()
        while(recorrer!=None):
            if(temp.getData()==recorrer.getData()):
                return True
            recorrer=recorrer.getNext()
        return False

def pitagoras(id1,id2,stationList):
        origin_x = stationList[id1-1].x
        origin_y = stationList[id1-1].y
        destination_x = stationList[id2-1].x
        destination_y = stationList[id2-1].y
        
        h=math.sqrt(((origin_x-destination_x)**2)+((origin_y-destination_y)**2))
        return h

def costeAcumuladoDistancia(lista,stationList):
        aux=lista.getHead()
        recorrido=aux.getNext()
        acumulado=0
        while(recorrido!=None):
                acumulado = acumulado + pitagoras(aux.getData().id,recorrido.getData().id,stationList)        
                aux=aux.getNext()
                recorrido=recorrido.getNext()
        return acumulado

def costeAcumuladoTiempo(lista,stationList,timeConnections, timeStations):
        aux=lista.getHead()
        aux2=aux.getNext()
        acumulado=0
        while(aux2!=None):
                if(aux.getData().name == aux2.getData().name):
                        acumulado = acumulado + timeConnections[aux.getData().id].get(aux2.getData().id)
                elif(aux.getData().name != aux2.getData().name):
                        acumulado = acumulado + timeStations[aux.getData().id].get(aux2.getData().id)
                aux=aux.getNext()
                aux2=aux2.getNext()
        return acumulado
    
def costeAcumuladoParadas(lista,stationList,connections):
        aux=lista.getHead()
        aux2=aux.getNext()
        acumulado=0
        while(aux2!=None):
                if(aux.getData().name != aux2.getData().name):
                    acumulado = acumulado + 1       
                aux=aux.getNext()
                aux2=aux2.getNext()
        return acumulado

def costeAcumuladoTransbords(lista,stationList,connections):
        aux=lista.getHead()
        aux2=aux.getNext()
        acumulado=0
        while(aux2!=None):
                if(aux.getData().name == aux2.getData().name):
                    acumulado = acumulado + 1       
                aux=aux.getNext()
                aux2=aux2.getNext()
        return acumulado

def ponerCoste(lista,destino,stationList,typePreference,timeConnections, timeStation, connections):
        #Minima distancia
        if(typePreference == "0"):
            h = pitagoras((lista.getFirst().id),destino.id,stationList)
            g = costeAcumuladoDistancia(lista,stationList)
        #Minimes parades
        elif(typePreference == "1"):
            if(lista.getFirst().id != destino.id):
                h = 1
            else:
                h = 0
            g = costeAcumuladoParadas(lista,stationList,connections)
        #Minim temps
        elif(typePreference == "2"):
            h = pitagoras((lista.getFirst().id),destino.id,stationList) / 90
            g = costeAcumuladoTiempo(lista,stationList,timeConnections, timeStation)
        #Minims transbords
        elif(typePreference == "3"):
            if(lista.getFirst().line != destino.line):
                h = 1
            else:
                h = 0
            g = costeAcumuladoTransbords(lista,stationList,connections)
            
        lista.setCost(float(h)+float(g))
        return lista

def expandirNodo(typePreference,estrella,stationList,connections,cami,destino,timeConnections, timeStation):
        aux=cami.getFirst().id

        #print(typePreference)
        
        for i in stationList:
                temp=cami.__copy__()
                for j in connections[aux].keys():
                        if(j == i.id):
                                #print(i.id)
                                temp.prepend(i)
                                if(RemoveCycles(temp) is False):
                                    temp = ponerCoste(temp,destino,stationList,typePreference,timeConnections, timeStation,connections)
                                    estrella.prepend(temp)
        estrella.extract(cami)
        return estrella

def ordenarLista(estrella):
        temp=LinkedList()
        while(estrella.getIsEmpty() is False):
                recElement=estrella.getHead()
                rec=recElement.getData()
                costemin=rec.getCost()
                nodomin=rec
                while(recElement!=None):
                        rec=recElement.getData()
                        if(rec.getCost()<=costemin):
                                costemin=rec.getCost()
                                nodomin=rec
                        recElement=recElement.getNext()
                temp.append(nodomin)
                estrella.extract(nodomin)
        estrella=LinkedList()
        estrella=temp.__copy__()
        return estrella

# AstarAlgirthm: main function. It is the connection between the GUI and the AStar search code.
#       INPUTS:
#           - stationList: list of the stations of a city. (- id, name, line, x, y -)
#           - connections: Dictionary set of possible connections between the stations. 
#           - coord_origin: list of two values referring to the origin coordinates
#           - coord_destination: list of two values referring to the destination coordinates 
#           - typePreference: Value to indicate the preference selected: 0 - minimum Distance | 1- minimum Stops | 2- minimum Time | 3 - minimum Connections
#           - timeConnections: Dictionary including the time of connections between two different lines in a certain station 
#           - timeStation: Dictionary including the time of connections between two different stations.
#       OUTPUTS:
#           - time: required time to make the route
#           - distance: total distance made in the route
#           - connections: total connections between different lines in the route
#           - stopStations: total stops made in the route
#           - expandedNodes: total expanded nodes to get the optimal path
#           - expandedList:  list of the expanded nodes to get the optimal path
#           - idCamins: List of the Station IDs of the optimal Path
#           - min_distance_origin: the distance of the origin_coordinates to the closest station 
#           - min_distance_destination: the distance of the destination_coordinates to the closest station
#                       - num_depth
def AstarAlgorithm(stationList, connections,coord_origin,coord_destination,typePreference, timeConnections, timeStation):

        temps = 0
        expandits = 0
        depth = 0
        expanded_list = []
        id_list = []

        origin_node, min_distance_origin = originStation(stationList,coord_origin)
        destination_node, min_distance_destination = destinationStation(stationList, coord_destination)
        temps = min_distance_origin + min_distance_destination

        #Iniciem algoritme estrella
        estrella = LinkedList() #Fem la LinkedList general (guardara totes les LinkedLists per cada cami possible
        NodeArrel=LinkedList()                  #Fem una LinkedList
        NodeArrel.prepend(origin_node)          #Li pasem el node origen
        estrella.prepend(NodeArrel)             #Li passem aquesta LinkedList a la LinkedList general (estrella)
        cami=estrella.getFirst().getFirst()     #Cami = [id,name,line,x,y] del node Origen
        while(cami.id != destination_node.id or estrella.isEmpty): 
                cami=estrella.getFirst()        #Cami = LinkedList del node amb cost mes petit
                expandits = expandits + 1
                expanded_list.append(cami.getFirst().id)
                estrella = expandirNodo(        #Expandim el node amb cost mes petit i actualitzem 'Estrella' desde dins
                        typePreference,                 #Tipus Preferencia (0-Distance|1-Stops|2-Time|3-Connections)
                        estrella,                       #LinkedList general con todas las LinkedList
                        stationList,                    #Lista con les estaciones ([id,name,line,x,y])
                        connections,                    #Diccionari amb les conexions entre estacions
                        cami,                           #LinkedList del cami amb cost mes petit
                        destination_node,               #Node desti ([id,name,line,x,y])
                        timeConnections,
                        timeStation)
                estrella = ordenarLista(estrella) #Ordenem 'Estrella' de cost mes petit a mes gran
                cami = estrella.getFirst().getFirst() #Cami = [id,name,line,x,y] del node amb cost mes petit

        #Borrem els nodes de transbords innecesaris
        antigua = estrella.getFirst()
        aux = antigua

        aux2 = antigua.getHead()
        aux3 = aux2.getNext()
        while aux3 != None:
            if(aux2.getData().name == aux3.getData().name
               and aux2.getData().line != aux3.getData().line):
                aux4 = aux3.getNext()
                if(aux4 != None):
                    if(aux3.getData().name == aux4.getData().name
                        and aux3.getData().line != aux4.getData().line):
                        aux.extract(aux3.getData())
            aux2 = aux2.getNext()
            aux3 = aux3.getNext()

        estrella.extract(antigua)
        estrella.prepend(aux)

        #Borrem les ids repetides a la llista de nodes expandits
        for i in expanded_list:
            while (expanded_list.count(i) > 1):
                expanded_list.remove(i)
        expanded_list.sort()
        
        #Calculem distancia recorregut        
        aux = estrella.getFirst().getHead()
        aux2 = aux.getNext()
        distancia = 0
        while aux2 != None:
                distancia = distancia + pitagoras(aux.getData().id,aux2.getData().id,stationList)
                aux = aux.getNext()
                aux2 = aux2.getNext()

        #Calculem temps recorregut
        aux = estrella.getFirst().getHead()
        aux2 = aux.getNext()
        while aux2 != None:
                #print(timeStation[aux.getData().id].values())
                #print(timeStation[aux.getData().id].get(aux2.getData().id))
                if(aux.getData().line == aux2.getData().line):
                        #print(timeStation[aux.getData().id].get(aux2.getData().id))
                        temps = temps + timeStation[aux.getData().id].get(aux2.getData().id)
                elif(aux.getData().line != aux2.getData().line and aux.getData().name == aux2.getData().name):
                        #print(timeConnections[aux.getData().id].get(aux2.getData().id))
                        temps = temps + timeConnections[aux.getData().id].get(aux2.getData().id)
                aux = aux.getNext()
                aux2 = aux2.getNext()

        #Calculem transbords recorregut
        aux = estrella.getFirst().getHead()
        aux2 = aux.getNext()
        transbords = 0
        while aux2 != None:
            if(aux.getData().name == aux2.getData().name
               and aux.getData().line != aux2.getData().line):
                transbords = transbords + 1
            aux = aux.getNext()
            aux2 = aux2.getNext()

        #Calculem parades recorregut
        aux = estrella.getFirst().getHead()
        aux2 = aux.getNext()
        parades = 1
        while aux2 != None:
            if(aux.getData().name != aux2.getData().name):
                parades = parades + 1
            aux = aux.getNext()
            aux2 = aux2.getNext()

        #Calculem idCamins
        aux = estrella.getFirst().getHead()
        while aux!=None:
            id_list.append(aux.getData().id)
            aux = aux.getNext()
        id_list.reverse()
        #Calculem depth
        depth = parades + transbords

        """
        aux = estrella.getFirst().getHead()
        while aux != None:
                print(aux.getData().name)
                aux = aux.getNext()
        """
                
        return temps,distancia,transbords,parades,expandits,expanded_list,id_list,min_distance_origin*4,min_distance_destination*4,depth
