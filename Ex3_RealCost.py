# With this exercise we will work on calculating the Real Cost of a Path.
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


    origin=Node(stationList[4],None)                # Charpennes L2
    destination=Node(stationList[5],origin)         # college Bellecombe L2
    origin2=Node(stationList[5], None)              # college Bellecombe L2
    destination2=Node(stationList[6],origin2)       # Thiers Lafayette L2
    destination3=Node(stationList[6],destination)   # Thiers Lafayette L2

    #------------------------------------------------------------------#

    #HEURISTIC 1 : TIME
    print "\n"
    timeCostTable=setCostTable( 1, stationList,city)
    print_connections(timeCostTable)

    destination.setRealCost(  timeCostTable)
    print " REAL COST (TIME) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +  str(destination.g)
    destination2.setRealCost(timeCostTable)
    print " REAL COST (TIME) from " + destination2.father.station.name + " L" + str(destination2.father.station.line) + " to " + destination2.station.name + " L" + str(destination2.station.line) + "  : \t\t" +  str(destination2.g)
    destination3.setRealCost(timeCostTable)
    print " REAL COST (TIME) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination3.station.name + " L" + str(destination3.station.line) + "  : \t\t" +  str(destination3.g)

    print "\n"

    #HEURISTIC 2 : DISTANCE
    distanceTable=setCostTable( 2,  stationList,city)
    print_connections(distanceTable)
    destination.setRealCost(  distanceTable)
    print " REAL COST (DISTANCE) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +  str(destination.g)
    destination2.setRealCost(distanceTable)
    print " REAL COST (DISTANCE) from " + destination2.father.station.name + " L" + str(destination2.father.station.line) + " to " + destination2.station.name + " L" + str(destination2.station.line) + "  : \t\t" +  str(destination2.g)
    destination3.setRealCost(distanceTable)
    print " REAL COST (DISTANCE) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination3.station.name + " L" + str(destination3.station.line) + "  : \t\t" +  str(destination3.g)

    print "\n"

    #HEURISTIC 3 : TRANSFERS
    print "\n"
    transfersCostTable=setCostTable( 3, stationList,city)
    print_connections(transfersCostTable)
    destination.setRealCost( transfersCostTable)
    print " REAL COST (#TRANSFERS) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +  str(destination.g)
    destination2.setRealCost(transfersCostTable)
    print " REAL COST (#TRANSFERS) from " + destination2.father.station.name + " L" + str(destination2.father.station.line) + " to " + destination2.station.name + " L" + str(destination2.station.line) + "  : \t\t" +  str(destination2.g)
    destination3.setRealCost(transfersCostTable)
    print " REAL COST (#TRANSFERS) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination3.station.name + " L" + str(destination3.station.line) + "  : \t\t" +  str(destination3.g)

    print "\n"

    #HEURISTIC 4 : STOP STATIONS
    print"\n"
    stopStationsCostTable=setCostTable( 4,  stationList,city)
    print_connections(stopStationsCostTable)
    destination.setRealCost(  stopStationsCostTable)
    print " REAL COST (#STATIONS) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) + "  : \t\t" +  str(destination.g)
    destination2.setRealCost(stopStationsCostTable)
    print " REAL COST (#STATIONS) from " + destination2.father.station.name + " L" + str(destination2.father.station.line) + " to " + destination2.station.name + " L" + str(destination2.station.line) + "  : \t\t" +  str(destination2.g)
    destination3.setRealCost(stopStationsCostTable)
    print " REAL COST (#STATIONS) from " + origin.station.name + " L" + str(origin.station.line) + " to " + destination3.station.name + " L" + str(destination3.station.line) + "  : \t\t" +  str(destination3.g)










if __name__ == '__main__':
    main()
