# PublicTrans GUI
#
# Authors: 
# Group: 
# _________________________________________________________________________________________
# Intel.ligencia Artificial 
# Grau en Enginyeria Informatica
# Curs 2013 - 2014
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________
from Tkinter import *

import ScrolledText
import tkMessageBox
from MapaMetro import *
from CercaInformada import *



class _Astargui:
	#__init__ contains the window design, including default values.
    def __init__(self, master):
		#DEFAULT VALUES
        self.initComplete = 0
        self.id_origen=-1
        self.coord_origin=[]
        self.id_desti=-1
        self.coord_destination=[]
        self.typePreference=-1
        self.connections={}
        self.names=[]
        self.filenameMetro=StringVar()
        self.filenameConnections=StringVar()
        self.filenameTimeStations=StringVar()
        self.filenameTimeConnections=StringVar()
        self.filenameMetro.set("Stations.txt")
        self.filenameConnections.set("Connections.txt")
        self.filenameTimeStations.set("TempsEstacions1.txt")
        self.filenameTimeConnections.set("TempsTransbordaments1.txt")

		#WINDOW DEFINITION
        frame = Frame(master, width=1250, height=750)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        self.master.title("PUBLIC - TRANS")

		# CALCULATE BUTTON DEFINITION
        self.Button_Calculate = Button(self.master,text="Calcular Ruta", relief="raised", width="15")
        self.Button_Calculate.place(x=15, y=3, width=117, height=28)
        self.Button_Calculate.bind("<ButtonRelease-1>", self.Button_Calculate_Click)

		#QUIT BUTTON DEFINITION
        self.Button_Quit = Button(frame,text="Sortir", width="15", command=frame.quit)
        self.Button_Quit.place(x=250, y=3, width=117, height=28)
        self.Button_Quit.bind("<ButtonRelease-1>", self.Button_Quit_Click)

		#GLOBAL BOXES
        OriginDestinationFrame = LabelFrame(self.master, text="Dades de la consulta")
        OriginDestinationFrame.pack(fill="both", expand="yes")
        OriginDestinationFrame.place(x=20, y= 30, width=1200, height=350)
        ResultsFrame = LabelFrame(self.master, text="Results")
        ResultsFrame.pack(fill="both", expand="yes")
        ResultsFrame.place(x=20, y= 400, width=1200, height=350)

		#TITLES
        self.Label1 = Label(self.master,text="ORIGEN : ")
        self.Label1.place(x=50+250, y=280)
        self.Label_3 = Label(self.master,text="DESTI : ")
        self.Label_3.place(x=320+250, y=280)
        self.Label_4 = Label(self.master,text="RUTA TROBADA:")
        self.Label_4.place(x=650, y=420, width=112)
        self.Information_Origin_Selection= Label(self.master,text="Selecciona Estacio Metro ORIGEN :", justify=LEFT)
        self.Information_Origin_Selection.place(x=300, y=80)
        self.Information_Destination_Selection= Label(self.master,text="Selecciona Estacio Metro DESTI :", justify=LEFT)
        self.Information_Destination_Selection.place(x=560, y=80)
        self.Information_Origin_Selection= Label(self.master,text="Tambe pots indicar les teves coordenades :", justify=LEFT)
        self.Information_Origin_Selection.place(x=310, y=300)
        self.Information_Preferences= Label(self.master,text="Selecciona Preferencies : ", justify=LEFT)
        self.Information_Preferences.place(x=900, y=80)
        self.Label_x_origin= Label(self.master,text="x = ", justify=LEFT)
        self.Label_x_origin.place(x=350, y=330)
        self.Label_y_origin= Label(self.master,text="y = ",justify=LEFT)
        self.Label_y_origin.place(x=420, y=330)
        self.Label_x_destination= Label(self.master,text="x = ", justify=LEFT)
        self.Label_x_destination.place(x=620 , y=330)
        self.Label_y_destination= Label(self.master,text="y = ", justify=LEFT)
        self.Label_y_destination.place(x=700 , y=330)
        self.LabelFilenameMetro= Label(self.master,text="Fitxer del Metro de la ciutat: ", justify=LEFT)
        self.LabelFilenameMetro.place(x=70, y=80)
        self.Text_filenameMetro= Entry(self.master,textvariable=self.filenameMetro)
        self.Text_filenameMetro.place(x=70, y=100, width=170, height=20)	
        self.LabelFilenameCorrespondences= Label(self.master,text="Fitxer de Correspondencies :", justify=LEFT)
        self.LabelFilenameCorrespondences.place(x=70, y=120)
        self.Text_filenameConnections= Entry(self.master,textvariable=self.filenameConnections)
        self.Text_filenameConnections.place(x=70, y=140, width=170, height=20)
        self.LabelFilenameTimeConnections= Label(self.master,text="Fitxer de Temps de Transbords :", justify=LEFT)
        self.LabelFilenameTimeConnections.place(x=70, y=160)		
        self.Text_filenameTimeConnections= Entry(self.master,textvariable=self.filenameTimeConnections)
        self.Text_filenameTimeConnections.place(x=70, y=180, width=170, height=20)
        self.LabelFilenameTimeStations= Label(self.master,text="Fitxer de Temps Entre Estacions :", justify=LEFT)
        self.LabelFilenameTimeStations.place(x=70, y=200)		
        self.Text_filenameStations= Entry(self.master,textvariable=self.filenameTimeStations)
        self.Text_filenameStations.place(x=70, y=220, width=170, height=20)
		
		# OUTPUTS TITLES
        self.Label_5 = Label(self.master,text="Temps Total: ", image="", width="15", justify=LEFT, anchor=W)
        self.Label_5.place(x=80, y=450, width=113, height=23)
        self.Label_6 = Label(self.master,text="Distancia :", image="", width="15", justify=LEFT, anchor=W)
        self.Label_6.place(x=80, y=500, width=113, height=23)
        self.Label_7 = Label(self.master,text="Transbords : ", width="15", justify=LEFT, anchor=W)
        self.Label_7.place(x=80, y=550, width=113, height=23)
        self.Label_8 = Label(self.master,text="Parades : ", image="", width="15", justify=LEFT, anchor=W)
        self.Label_8.place(x=80, y=600, width=113, height=23)
        self.Label_9 = Label(self.master,text="Nodes Expandits : ", image="", width="15", justify=LEFT, anchor=W)
        self.Label_9.place(x=80, y=650, width=113, height=23)
        self.Label_10 = Label(self.master,text="Llista Nodes", width="15", justify=LEFT)
        self.Label_10.place(x=300, y=450, width=120, height=27)
        self.Label_11 = Label(self.master,text=" Prof. Solucio : ", image="", width="15", justify=LEFT, anchor=W)
        self.Label_11.place(x=80, y=700, width=113, height=23)

		# OUTPUT MESSAGES
        self.text_expandedNodes=StringVar() # Will contain the amount of expanded nodes in the search
        self.text_time=StringVar() # Will contain the travel times it takes
        self.text_distance=StringVar() # Will contain the travel distance it takes
        self.text_connections=StringVar()# Will contain the connections times it takes
        self.text_stopStations=StringVar()# Will contain the stops it takes
        self.text_depth=StringVar() # will containt the depth of the optimal solution
		
		#DEFAULT VALUES FOR OUTPUT MESSAGES
        self.text_expandedNodes.set("0")
        self.text_time.set("0")
        self.text_distance.set("0")
        self.text_connections.set("0")
        self.text_stopStations.set("0")
        self.text_depth.set("0")
        self.sms_time = Message(self.master,textvariable=self.text_time, aspect=200)
        self.sms_time.place(x=200, y=450)

		#OUTPUT MESSAGES - DEFINITION
        self.sms_distance = Message(self.master,textvariable=self.text_distance,aspect=200)
        self.sms_distance.place(x=200, y=500)
        self.sms_connections = Message(self.master,textvariable=self.text_connections)
        self.sms_connections.place(x=200, y=550)
        self.sms_stopStations = Message(self.master,textvariable=self.text_stopStations)
        self.sms_stopStations.place(x=200, y=600)
        self.sms_expandedNodes = Message(self.master,textvariable=self.text_expandedNodes)
        self.sms_expandedNodes.place(x=200, y=650)
        self.sms_depth= Message(self.master,textvariable=self.text_depth)
        self.sms_depth.place(x=200, y=700)

		# ORIGIN STATIONS LIST
        lbframe = Frame( self.master )
        self.Origin_Listbox_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Origin_Listbox = Listbox(lbframe, width="15", selectmode="extended", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Origin_Listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Origin_Listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.Origin_Listbox_frame.place(x=50+250, y=104, width=250, height=170)
        self.Origin_Listbox.bind("<ButtonRelease-1>", self.Origin_Listbox_Click)

		
		# DESTINATION STATIONS LIST
        lbframe = Frame( self.master )
        self.Destination_Listbox_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Destination_Listbox = Listbox(lbframe, width="15", selectmode="extended", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Destination_Listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Destination_Listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.Destination_Listbox_frame.place(x=310+250, y=104, width=250, height=170)
        self.Destination_Listbox.bind("<ButtonRelease-1>", self.Destination_Listbox_Click)

		# PREFERENCES - MINIMUM DISTANCE
        self.Check_Button_Distance_Radiobutton = Radiobutton(self.master,text="Minima Distancia", variable=self.typePreference, value=0, justify=LEFT)
        self.Check_Button_Distance_Radiobutton.place(x=900, y=130)
        self.RadioGroup1_StringVar = StringVar()
        self.RadioGroup1_StringVar.set("check_button_distance")
        self.RadioGroup1_StringVar_traceName = self.RadioGroup1_StringVar.trace_variable("w", self.RadioGroup1_StringVar_Callback)
        self.Check_Button_Distance_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

		# PREFERENCES - MINIMUM STOP STATIONS
        self.Check_Button_StopStations_Radiobutton = Radiobutton(self.master,text="Minim Parades", variable=self.typePreference, value=1, justify=LEFT)
        self.Check_Button_StopStations_Radiobutton.place(x=900, y=160)
        self.Check_Button_StopStations_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

		# PREFERENCES - MINIMUM TIME
        self.Check_Button_Time_Radiobutton = Radiobutton(self.master,text="Minim Temps",  variable=self.typePreference, value=2, justify=LEFT)
        self.Check_Button_Time_Radiobutton.place(x=900, y=190)
        self.Check_Button_Time_Radiobutton.configure(variable=self.RadioGroup1_StringVar )

		# PREFERENCES - MINIMUM CONNECTIONS
        self.Check_Button_Connections_Radiobutton = Radiobutton(self.master,text="Minim Transbords", variable=self.typePreference, value=3, justify=LEFT)
        self.Check_Button_Connections_Radiobutton.place(x=900, y=220)
        self.Check_Button_Connections_Radiobutton.configure(variable=self.RadioGroup1_StringVar )


		# EXPANDED NODES OUTPUT MESSAGE		
        self.Text_NodeList = ScrolledText.ScrolledText(self.master)
        self.Text_NodeList.pack(side=LEFT, fill=BOTH, expand=1)
        self.Text_NodeList.place(x=330, y=500, width=250, height=200)

		# OPTIMAL PATH OUTPUT MESSAGE	
        self.Route_Text = ScrolledText.ScrolledText(self.master)
        self.Route_Text.pack(side=LEFT, fill=BOTH, expand=1)
        self.Route_Text.place(x=650, y=450, width=550, height=280)
        self.master.resizable(0,0) # Linux may crash in this line. In this case, just comment
		
		# ORIGIN AND DESTINATION SELECTED
        self.v_origin=StringVar()
        self.v_destination=StringVar()
        self.origen_message = Label(self.master,textvariable=self.v_origin)
        self.origen_message.place(x=120+250, y=280)
        self.desti_message = Label(self.master,textvariable=self.v_destination)
        self.desti_message.place(x=370+250, y=280)
        self.v_origin.set("")
        self.v_destination.set("")

		# COORDINATES BOXES - X ORIGIN
        self.string_origin_position_x=StringVar()
        self.string_origin_position_x.set("")
        self.Text_x_origin= Entry(self.master,textvariable=self.string_origin_position_x)
        self.Text_x_origin.place(x=380, y=330, width=40, height=20)		

		# COORDINATES BOXES - Y ORIGIN
        self.string_origin_position_y=StringVar()
        self.string_origin_position_y.set("")
        self.Text_y_origin= Entry(self.master,textvariable=self.string_origin_position_y)
        self.Text_y_origin.place(x=450, y=330, width=40, height=20)	
		
		# COORDINATES BOXES - X DESTINATION
        self.string_destination_position_x=StringVar()
        self.string_destination_position_x.set("")
        self.Text_x_destination= Entry(self.master,textvariable=self.string_destination_position_x)
        self.Text_x_destination.place(x=650, y=330, width=40, height=20)	
		
		# COORDINATES BOXES - Y DESTINATION
        self.string_destination_position_y=StringVar()
        self.string_destination_position_y.set("")
        self.Text_y_destination= Entry(self.master,textvariable=self.string_destination_position_y)
        self.Text_y_destination.place(x=730, y=330, width=40, height=20)	
		
        # COORDINATES SEARCH BUTTON
        self.Button_Calculate = Button(self.master,text="Establir coordenades", relief="raised")
        self.Button_Calculate.place(x=800, y=330, width=117, height=28)
        self.Button_Calculate.bind("<ButtonRelease-1>", self.Button_Update_Position)
		
        # UPDATE CITY INFORMATION BUTTON
        self.Button_Update_City = Button(self.master,text="Actualitzar informacio ciutat", relief="raised", width="15", command= self.Button_Update_City)
        self.Button_Update_City.place(x=55, y=250, width=200, height=28)
        #self.Button_Update_City.bind("<ButtonRelease-1>", self.Button_Update_City())
		
		
        #FILENAMES BOXES SETTING: FILENAMES DEFAULT VALUES
        self.filenameMetro.set(self.filenameMetro.get())
        self.filenameConnections.set(self.filenameConnections.get())

		#CONNECTION WITH MAPAMETRO.PY -> Update Station Information
        self.stationList=readStationInformation(self.filenameMetro.get())
        self.connections=readCostTable(self.filenameConnections.get())
        self.stationList=setNextStations(self.stationList, self.connections)
        self.timeConnections=readCostTable(self.filenameTimeConnections.get())
        self.timeStations=readCostTable(self.filenameTimeStations.get())

		#READING CITY INFORMATION
        ids=0
        indexes=[]
        for i in self.stationList:
            ids=ids+1
            if i.name not in self.names: # Do not consider as different station two entries with the same name
                indexes.append(ids)
                self.names.append(i.name)
   
        self.names, self.order_names=zip(*sorted(zip(self.names,indexes))) # Sort alphabetically the list of stations. Keep the index order		
       
	   # INSERT PREVIOUS INFORMATION READ INTO THE LISTBOXES
        for i in self.names:
           self.Destination_Listbox.insert(END, i)
		   
        for i in self.names:
            self.Origin_Listbox.insert(END, i)
			
	#Button_Update_City : Button "Actualitzar informacio Ciutat" calls this function.
	#                     It reads the corresponding files and update the City Information into the variables.
    def Button_Update_City(self):
        pass
		# Get filenames
        self.filenameMetro.set(self.filenameMetro.get())
        self.filenameConnections.set(self.filenameConnections.get())
        
		#Update City Information
        self.stationList=readStationInformation(self.filenameMetro.get())
        self.connections=readCostTable(self.filenameConnections.get())
        self.stationList=setNextStations(self.stationList, self.connections)
        self.timeConnections=readCostTable(self.filenameTimeConnections.get())
        self.timeStations=readCostTable(self.filenameTimeStations.get())
        
		#Delete current station lists
        self.Destination_Listbox.delete(0, END)
        self.Origin_Listbox.delete(0, END)
		
        self.names=[]
        ids=0
        indexes=[]
       
	   #Reading city Information
        ids=0
        indexes=[]
        for i in self.stationList:
            ids=ids+1
            if i.name not in self.names: # Do not consider as different station two entries with the same name
                indexes.append(ids)
                self.names.append(i.name)
   
        self.names, self.order_names=zip(*sorted(zip(self.names,indexes))) # Sort alphabetically the list of stations. Keep the index order		
       
	   # Insert previous information read into the listBoxes
        for i in self.names:
           self.Destination_Listbox.insert(END, i)
		   
        for i in self.names:
            self.Origin_Listbox.insert(END, i)
		

	#Button_Update_City : Button "Calcular Ruta" calls this function.
	#                     It Execute AStar Algorithm [from CercaInformada.py] and shows the optimal path found.
    def Button_Calculate_Click(self, event): 
        pass
		#Delete current NodeList Information from previous seraches
        self.Text_NodeList.delete('0.0',END)
		#Delete current Path Information from previous seraches
        self.Route_Text.delete('0.0',END)
		
        if self.id_origen!=-1: # If an origin is selected, continue
            if self.id_desti!=-1: # If a destination is selected, continue
                if self.typePreference!=-1: # If a preference is selected, run ASTAR algorithm and show the Optimal Path
                    time,distance,connections,stopStations,expanded_nodes,llista_nodes,path, min_distance_origin,min_distance_destination, num_depth=AstarAlgorithm(self.stationList, self.connections,self.coord_origin,self.coord_destination,self.typePreference,self.timeConnections, self.timeStations)
                    self.Update_Resultant_Path(time,distance,connections,stopStations,expanded_nodes,llista_nodes,path, min_distance_origin,min_distance_destination, self.coord_origin, self.coord_destination, num_depth)
                else:
                    self.Update_Resultant_Path([],[],[],[],[],[]," NO HAS SELECCIONAT CAP PREFERENCIA",[],[],[],[],[])
            else:
                self.Update_Resultant_Path([],[],[],[],[],[]," NO HAS SELECCIONAT CAP DESTI",[],[],[],[],[])
        else:
            self.Update_Resultant_Path([],[],[],[],[],[]," NO HAS SELECCIONAT CAP ORIGEN",[],[],[],[],[])

	#Button_Update_Position : Button "Establir Coordenades" calls this function.
	#                     It Update Coordinates values from the boxes		
    def Button_Update_Position(self, event):
        self.string_destination_position_x.set(self.string_destination_position_x.get())
        self.string_destination_position_y.set(self.string_destination_position_y.get())
        self.string_origin_position_x.set(self.string_origin_position_x.get())
        self.string_origin_position_y.set(self.string_origin_position_y.get())
        self.coord_destination=[int(self.string_destination_position_x.get())]
        self.coord_destination.append(int(self.string_destination_position_y.get()))
        self.coord_origin=[int(self.string_origin_position_x.get())]
        self.coord_origin.append(int(self.string_origin_position_y.get()))
        self.v_origin.set("")
        self.v_destination.set("")
        self.id_desti=0 # To know that an origin is selected
        self.id_origen=0 # To know that a destination is selected
		
	#Button_Quit_Click : Button "Sortir" calls this function.
	#                     It closes the application		
    def Button_Quit_Click(self, event): 
        pass

	#Update_Resultant_Path : It update the output messages [Information] to the GUI			
    def Update_Resultant_Path(self,time,distance,connections,stopStations,expanded_nodes,llista_nodes,path, min_distance_origin,min_distance_destination, coord_origin, coord_destinationnation, num_depth):
        pass
        from decimal import Decimal, ROUND_DOWN

        if time!=[]:
            distance = Decimal(str(distance)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            time = Decimal(str(time)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            self.text_expandedNodes.set(str(expanded_nodes))
            self.text_time.set(str(time))
            self.text_distance.set(str(distance))
            self.text_connections.set(str(connections))
            self.text_stopStations.set(str(stopStations))
            self.Text_NodeList.insert(END, str(llista_nodes))
            self.text_depth.set( str(num_depth))
            self.Route_Text.insert(END,Print_path(path, self.stationList, min_distance_origin,min_distance_destination, coord_origin, coord_destinationnation))
        else:
            self.Route_Text.insert(END,Print_Error(path))
	
    #Origin_Listbox_Click : Origin Listbox calls this function.
	#                     It updates the origin selected 
    def Origin_Listbox_Click(self, event): 
        pass
        self.id_origen=self.order_names[int(self.Origin_Listbox.curselection()[0])]
        self.v_origin.set(str(self.stationList[self.id_origen-1].name))
        self.string_origin_position_x.set(str(self.stationList[self.id_origen-1].x))
        self.string_origin_position_y.set(str(self.stationList[self.id_origen-1].y))
        self.coord_origin=[int(self.stationList[self.id_origen-1].x)]
        self.coord_origin.append(int(self.stationList[self.id_origen-1].y))	
   
    #Destination_Listbox_Click : Destination Listbox calls this function.
	#                     It updates the destination selected  
    def Destination_Listbox_Click(self, event):
        pass
        self.id_desti=self.order_names[int(self.Destination_Listbox.curselection()[0])]
        self.v_destination.set(str(self.stationList[self.id_desti-1].name))
        self.string_destination_position_x.set(str(self.stationList[self.id_desti-1].x))
        self.string_destination_position_y.set(str(self.stationList[self.id_desti-1].y))
        self.coord_destination=[int(self.stationList[self.id_desti-1].x)]
        self.coord_destination.append(int(self.stationList[self.id_desti-1].y))
		
	#RadioGroup1_StringVar_Callback : CheckList calls this function.
	#                                 It updates the preference selected by the user
    def RadioGroup1_StringVar_Callback(self, varName, index, mode):
        pass

        self.typePreference=self.RadioGroup1_StringVar.get()		

	#Print_Error : Format string to print an error
def Print_Error(stringError):
	stringList=""
	stringList= stringList + "===========================================================\n"	
	stringList= stringList + "                  ERROR  \n"
	stringList= stringList + "===========================================================\n\n"
	stringList= stringList + "\t" +stringError
	return stringList
	
	#Print_Error : Format string to print the optimal path to follow in our search
def Print_path(path, stationList, min_distance_origin, min_distance_destination,coord_origin, coord_destinationnation):
        pass
        stringList=""
        if(min_distance_origin!=0):
            stringList = stringList + " WALK FROM: \t[" + str(coord_origin[0]) + "," + str(coord_origin[1]) + "] \t TO : \t" + str(stationList[path[0]-1].name) + "\n"
		
        stringList= stringList + "===========================================================\n"
        stringList=stringList + "     ORIGEN :\t" + str(path[0])  + "\t" + str(stationList[path[0]-1].line)   + "\t"  + str(stationList[path[0]-1].name)  +"\n"
        stringList= stringList + "===========================================================\n"
        for i in path[1:-1]:
           stringList= stringList + "\t" + str(i)  + "\t" + str(stationList[i-1].line)  + "\t" + str(stationList[i-1].name) + "\n"#+"      " +  str(stationList[i-1].destins[idCamins[i]]) + "\t\t" + str(stationList[i-1].destins[idCamins[i]])
        stringList= stringList + "===========================================================\n"
        stringList= stringList + "     DESTI :\t" + str(path[len(path)-1])  + "\t" + str(stationList[path[len(path)-1]-1].line)   + "\t"  + str(stationList[path[len(path)-1]-1].name)   + "\n"
        stringList= stringList + "===========================================================\n"
        if(min_distance_destination!=0):
            stringList = stringList + " WALK FROM: \t" +  str(stationList[path[len(path)-1]-1].name) +" \t TO : \t[" + str(coord_destinationnation[0]) + "," + str(coord_destinationnation[1]) + "] \n" 
        return stringList

def main():
    root = Tk()
    app = _Astargui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
