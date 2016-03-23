from math import *
from Tkinter import *
import tkMessageBox

def lectura2(filename):
    txtMetroLyon = open(filename,'r')
    vEstaciones=[]
    linia='0'
    while len(linia)>0:
        linia = txtMetroLyon.readline().split()
        if len(linia)>0 :
            vEstaciones.append(linia)
    txtMetroLyon.close()
    return vEstaciones

class getCamino(object):
    __slots__ = ['__fichero1', '__fichero2', '__lista', '__salida', '__llegada']

    def __init__(self, fichero1, fichero2):       
        self.__fichero1 = lectura2(fichero1)
        self.__fichero2 = lectura2(fichero2)
        self.__lista = []
        self.__llegada = ""
        self.__salida = ""

    def getFichero1(self):
        return self.__fichero1    

    def getFichero2(self):
        return self.__fichero2

    def getLista(self):
        return self.__lista

    def getSalida(self):
        return self.__salida

    def getLlegada(self):
        return self.__llegada

    def AlgoritmoAestrella(self, Origen, Destino, heur):
        top = Toplevel()
        self.__salida = self.estacion(Origen)
        self.__llegada = self.estacion(Destino)
        if (self.__salida == self.__llegada):
            tkMessageBox.showinfo("Advertencia", "Usted ya se encuentra en " + Destino + ", Elija otro destino posible.")
        else:         
            self.__lista.append([self.__salida])
            i = 1  
            while (self.objetivo(self.__lista) or len(self.__lista)==0):
                C = self.__lista[0]
                self.__lista.remove(C)
                E = self.Expandir(C)
                E=self.EliminarCiclos(E)
                self.__lista=self.ordenadarLista(E, heur)
                i=i+1
                
            if len(self.__lista)==0:
                print "No existe solucion"
                tkMessageBox.showinfo("heuristica", "No existe solucion")
            else:
                tiempo,transbordo=self.costeCamino(self.__lista, 0)
                
                LblTiempo = Label(top, text= "Tiempo: "+str(tiempo)+" minutos")
                LblTiempo.grid(row=3, columnspan=5)
                LblParadas = Label(top, text= "Paradas realizadas: "+str(len(self.__lista[0])-1))
                LblParadas.grid(row=4, columnspan=5)
                LblHeur1 = Label(top, text= "Transbordos: "+str(transbordo))
                LblHeur1.grid(row=5, columnspan=5)
                LblHeur2 = Label(top, text= "El camino es:")
                LblHeur2.grid(row=5, columnspan=5)
                LblHeur3 = Label(top, text= "\t"+str(self.paradasCamino(self.__lista[0])))
                LblHeur3.grid(row=5, columnspan=5)
            top.mainloop()

    def Expandir (self, lista):
        vecinos = []
        parada=lista[0]    
        
        for i in range (len(self.__fichero2)):
            if int(self.__fichero2[parada][i]) != 0:
                vecinos.append(i)

        caminos=[]
        for i in range(len(vecinos)):
            caminos.append([])
        
        for i in range(len(caminos)):
            caminos[i].append(vecinos[i])
            for j in range(len(lista)):
                caminos[i].append(lista[j])
                
        if self.__lista != []:
            for i in range(len(self.__lista)):
                caminos.append(self.__lista[i])
        return caminos

    def estacion(self, parada):
        trobat=0
        for i in range(len(self.__fichero1)):
            if self.__fichero1[i][1]==parada.upper():
                estacion=i
                trobat=1
        if trobat==1:
            return estacion


    def EliminarCiclos(self, E):
        eliminar=[]
        for i in range(len(E)):
            for j in range(len(E[i])):
                if E[i][j]==E[i][0] and j!=0:
                    eliminar.append(i)
                    break;
        i=len(eliminar)
        if i > 0:
            while i > 0:
                E.remove(E[eliminar[i-1]])
                i = i - 1
        return E  

    def objetivo(self, lista):     
        if self.__fichero1[lista[0][0]][1]==self.__fichero1[self.__llegada][1]:
            return False
        else:
            return True

    def ordenadarLista(self, E, heuristica):
        costes=[]
        t=0
        for i in range(len(E)):
            g,t = self.costeCamino(E, i)
            h = self.heuristica(heuristica, E[i][0], t, len(E[i]))
            total = g + h
            costes.append(total)
        
        lista_ordenada=[]
        asignados=[]
        anterior=-1
        for i in range(len(costes)):
            menor=99999
            for j in range(len(costes)):
                if menor > costes[j] and anterior <= costes[j] and not(j in asignados):
                    menor=costes[j]
                    asigna=j
                    
            lista_ordenada.append(E[asigna])
            asignados.append(asigna)
            anterior=costes[asigna]
    
        return lista_ordenada

    def heuristica(self, metodo, inicio, transbordos, paradas):
        heur=0.0
        if metodo == "Distancia":
            x1 = int(self.__fichero1[inicio][3])
            y1 = int(self.__fichero1[inicio][4])
            x2 = int(self.__fichero1[self.__llegada][3])
            y2 = int(self.__fichero1[self.__llegada][4])
            heur = sqrt(((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2)))
            return heur
        else:
            if metodo =="Paradas":            
                heur = paradas*12
                return heur
            else:
                if metodo == "Transbordos":
                  
                    heur = transbordos*20 
                    return heur

    def costeCamino(self, camino, posicion):
        j = len(camino[posicion])-1
        g = 0
        transbordo=0
        while j >= 1:                
            g = g + int(self.coste(camino[posicion][j], camino[posicion][j-1]))
            
            if (self.__fichero1[camino[posicion][j]][2]!=self.__fichero1[camino[posicion][j-1]][2]):
                transbordo = transbordo + 1
            j = j - 1
            
        return g,transbordo
    
    def coste(self, inicio, fin):      
        if (self.__fichero2[inicio][fin])!=0:
            return self.__fichero2[inicio][fin]

    def paradasCamino(self, camino):
        indicaciones = ""
        i = len(camino) - 1
        destino = len(camino)
        while (i >= 0):
            if (i != 0) or (i ==len(camino) - 1):
                indicaciones = indicaciones + str(self.__fichero1[camino[i]][1])+ " (linea "+str(self.__fichero1[camino[i]][2])+")"
                if (self.__fichero1[camino[i]][2] != self.__fichero1[camino[i-1]][2]):
                    indicaciones = indicaciones + "\n\n TRANSBORDO!"
                indicaciones = indicaciones + "\n\n" + str(self.__fichero2[camino[i]][camino[i-1]])+" minutos \n\n"
            i = i - 1
        indicaciones = indicaciones + str(self.__fichero1[camino[0]][1])+ " (linea "+str(self.__fichero1[camino[0]][2])+")"
        return indicaciones
