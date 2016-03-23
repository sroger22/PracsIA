# This file includes all its needed for define the map of a city.
# 	- Station class deffinition (a metro station)
#	- Reads BD information
#			 - stop information
#			 - connection information
#
# Authors: 
# Group: 
# _________________________________________________________________________________________
# Intel.ligencia Artificial 
# Grau en Enginyeria Informatica
# Curs 2013 - 2014
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

class Station:
	# __init__ Constructor of Station Class.
	def __init__(self,id,name, line,x,y):
		self.id=id 					#station id
		self.destinationDic={}	    #Dictionary where principal keys refers to the set of stations that it is connected.
									#The value of this dictionary refers to the time cost between two stations.
		self.name = name			#station Name
		self.line = line			# line name string
		self.x = x					# coordinate X of the station
		self.y = y					# coordinate Y of the station

# readStationInformation: Given a filename, it reads the information of this file.
# The file should follow the format:
#	id <\t> name <\t> line <\t> x <\t> y <\n>
def readStationInformation(filename):
    fileMetro = open(filename,'r')
    stationList=[]
    for line in fileMetro:
        information = line.split('\t')
        station_read = Station(int(information[0]),information[1],information[2],int(information[3]),int((information[4].replace('\n','')).replace(' ','')))
        stationList.append(station_read)    
    fileMetro.close()
    return stationList

# readCostTable: Given a filename, it reads the information of this file.
# The file should be an inferior matrix containg the cost between two different stations.
def readCostTable(filename):
	fileCorrespondencia = open(filename,'r')
	connections={}
	origin=1	
	for i in fileCorrespondencia:
		informations = i.split('\t')
		destinationnation=1
		for j in informations:
			j=j.replace('\n','')
			if j!='':
				if j!='0':
					if connections.has_key(int(origin))==False:
						connections[int(origin)]={}
					if (connections[int(origin)].has_key(int(destinationnation)) == 0):
						connections[int(origin)][int(destinationnation)]=float(j)
					# as the matrix is an inferior matrix, we should duplicate the information to the superior missing part.
					if connections.has_key(int(destinationnation))==False:
						connections[int(destinationnation)]={}
					if (connections[int(destinationnation)].has_key(int(origin)) == 0):
						connections[int(destinationnation)][int(origin)]=float(j)
				
			destinationnation=destinationnation+1
		origin=origin+1
	return connections

# setNextStations: Given a stationList (- id, name, line, x, y - information), and the set of possible connections between stations,
# This function set the dictionary of the possible destinations for each station (including the cost )
def setNextStations(stationList, connections):
	for i in stationList:
		if connections.has_key(int(i.id)):
			i.destinationDic=connections[int(i.id)].copy()
	return stationList

# print_stationList: Given a stationList (- id, name, line, x, y - information), it prints the information by terminal
def print_stationList(stationList):
    print "\n"
    print " ______________ STATION LIST________________"
    print "\n"
    for i in stationList:
       print " ID : "+  str(i.id) + " - " + str(i.name) + " linea: " + str(i.line) + "   pos: (" + str(i.x) + "," + str(i.y)+")"
    print "\n"
    print "\n"

# print_connections: Given a connections dictionary, it prints the information by terminal
def print_connections(connections):
    print "\n"
    print " ______________ CONNECTIONS ________________"
    print "\n"
    for i in connections.keys():
       print " ID : "+  str(i) + "  "
       for j in connections[i].keys():
               print "     " + str(j) + " : " + str(connections[i][j])
    print "\n"
    print "\n"

