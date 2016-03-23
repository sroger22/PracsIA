# With this exercise we will work on finding a station of the path given certain coordinates
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

    coord=[67,79]
    coord1=[140,20]
    coord2=[100,199]
    #------------------------------------------------------------------#


    node=coord2station(coord,stationList)
    node1=coord2station(coord1,stationList)
    node2=coord2station(coord2,stationList)

    print "\nFrom coord: " + str(coord) + " possible nodes: "
    for i in node:
        print stationList[i].name + " L"+ str(stationList[i].line) + " with ID: " + str([stationList[i].id])




    print "\nFrom coord: " + str(coord1) + " possible nodes:  "
    for i in node1:
        print stationList[i].name + " L"+ str(stationList[i].line) + " with ID: " + str([stationList[i].id])


    print "\nFrom coord: " + str(coord2) + " possible nodes: "
    for i in node2:
        print stationList[i].name + " L"+ str(stationList[i].line) + " with ID: " + str([stationList[i].id])



if __name__ == '__main__':
    main()