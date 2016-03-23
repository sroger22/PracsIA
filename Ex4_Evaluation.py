# With this exercise we will work on the evaluation function of the algorithm.
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

    origin=Node(stationList[1],None)            # Charpennes L1
    child=Node(stationList[4], origin)          # Charpennes L2
    destination=Node(stationList[13],None)      # Dauphine lacassagne L4

    #------------------------------------------------------------------#


    #HEURISTIC 1 : TIME
    timeCostTable=setCostTable(1,stationList, city)
    child.setHeuristic(1,destination,city)
    child.setRealCost( timeCostTable)
    child.setEvaluation()
    print " Evaluation Function (TIME) from " + child.station.name + " L" + str(child.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) +  ": \t\t" +  str(child.f)
    print "                               g : " + str(child.g)
    print "                               h : " + str(child.h) + "\n"

    #HEURISTIC 2 : DISTANCE
    distCostTable=setCostTable( 2,  stationList,city)
    child.setHeuristic(2,destination,city)
    child.setRealCost( distCostTable)
    child.setEvaluation()
    print " Evaluation Function (DISTANCE) from " + child.station.name + " L" + str(child.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) +  ": \t\t" +  str(child.f)
    print "                               g : "  + str(child.g)
    print "                               h : " + str(child.h) + "\n"

    #HEURISTIC 3 : TRANSFERS
    transCostTable=setCostTable( 3,  stationList,city)
    child.setHeuristic(3,destination,city)
    child.setRealCost( transCostTable)
    child.setEvaluation()
    print " Evaluation Function (#TRANSFERS) from " + child.station.name + " L" + str(child.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) +  ": \t\t" +  str(child.f)
    print "                               g : " + str(child.g)
    print "                               h : " + str(child.h) + "\n"

    #HEURISTIC 4 : STOP STATIONS
    stopCostTable=setCostTable(4, stationList,city)
    child.setHeuristic(4,destination,city)
    child.setRealCost(  stopCostTable)
    child.setEvaluation()
    print " Evaluation Function (#STATIONS) from " + child.station.name + " L" + str(child.station.line) + " to " + destination.station.name + " L" + str(destination.station.line) +  ": \t\t" +  str(child.f)
    print "                               g : " + str(child.g)
    print "                               h : " + str(child.h) + "\n"



if __name__ == '__main__':
    main()