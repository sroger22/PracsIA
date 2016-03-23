# With this exercise we will work on the definition of the heuristics.
#
__authors__='MariaXaviAnna'
__group__='DL00'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2015 - 2016
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

from SearchAlgorithm import *
from SubwayMap import *

def main():

    #------------------------------------------------------------------#
    #read file
    filename='Stations_Session1.txt'
    stationList=readStationInformation(filename)
    #read adjacency matrix
    filename='Connections_Session1.txt'
    adjacency=readCostTable(filename)

    #Real TIME cost table
    filename = 'PartialLyon_Session1_Time.txt'
    timeStations = readCostTable(filename)
    setNextStations(stationList, timeStations)

    # CITY information
    # velocity
    filename = "PartialLyon_Session1_InfoVelocity.txt"
    infoVelocity = readInformation(filename)
    # Transfers times
    filename = "PartialLyon_Session1_InfoTransfers.txt"
    infoTransfers = readInformation(filename)
    city=CityInfo(len(infoVelocity),infoVelocity,infoTransfers,adjacency)

    #------------------------------------------------------------------#

    origin=Node(stationList[5],None)                    # Charpennes L2
    destination=Node(stationList[13],None)               # Dauphine Lacassagne L4

    #------------------------------------------------------------------#


    #HEURISTIC 1 : TIME
    origin.setHeuristic( 1, destination,city)
    print " HEURISTIC (TIME) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +   str(origin.h)


    #HEURISTIC 2 : DISTANCE
    origin.setHeuristic( 2, destination,city)
    print " HEURISTIC (DISTANCE) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +  str(origin.h)

    #HEURISTIC 3 : TRANSFERS
    origin.setHeuristic( 3, destination,city)
    print " HEURISTIC (#TRANSFERS) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +   str(origin.h)


    #HEURISTIC 4 : STOP STATIONS
    origin.setHeuristic( 4, destination,city)
    print " HEURISTIC (#STATIONS) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +   str(origin.h)




if __name__ == '__main__':
    main()