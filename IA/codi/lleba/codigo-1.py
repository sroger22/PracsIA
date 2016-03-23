from math import *
from Tkinter import *
import tkMessageBox

def lectura2(filename):
    '''
    Funcion para la lectura de un fichero plano.
    '''
    fichero=open(filename,'r')
    f=[]
    linia='0'
    while len(linia)>0:
        linia = fichero.readline().split()
        if len(linia)>0 :
            f.append(linia)
    fichero.close()
    return f

class getCamino(object):
    __slots__ = ['__fichero1', '__fichero2', '__lista', '__salida', '__llegada']

    def __init__(self, fichero1, fichero2):
        
        '''
        Inicializacion de los atributos de la clase getCamino
        '''        

        self.__fichero1 = lectura2(fichero1)
        self.__fichero2 = lectura2(fichero2)
        self.__lista = []
        self.__salida = 0
        self.__llegada = 0


    def getFichero1(self):
        '''
        Funcion que nos retorna el fichero1, informacion sobre cada parada.
        (identificador, nombre, linea, posicion X, posicion Y)
        '''
        return self.__fichero1    

    def getFichero2(self):
        '''
        Funcion que nos retorna el fichero2, informacion de conexion enre paradas y sus costes
        '''
        return self.__fichero2

    def getLista(self):
        '''
        Funcion que nos retorna la lista de caminos
        '''
        return self.__lista

    def getSalida(self):
        '''
        Funcion que nos retorna la estacion de salida
        '''
        return self.__salida

    def getLlegada(self):
        '''
        Funcion que nos retorna la estacion de llegada
        '''
        return self.__llegada

    def Star(self, Origen, Destino, heur):
        '''
        Funcion que implementa el algoritmo de busqueda A*.
        '''
        top = Toplevel()
        self.__salida=self.buscar(Origen)
        self.__llegada=self.buscar(Destino)
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
            #print i
            #print self.__fichero2[parada][i]
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
        
    def buscar(self, parada):
        '''
        Funcion que busca una parada entrada en la lista de paradas de metro y nos retorna su identificador.
        '''
        trobat=0
        for i in range(len(self.__fichero1)):
            if self.__fichero1[i][1]==parada.upper():
                estacion=i
                trobat=1
        if trobat==1:
            return estacion
        else:
            raise IndexError ("Parada " +str(parada) + " no encontrada")
    def EliminarCiclos(self, E):
        '''
        Funcion que retorna la lista pasada por parametro una vez se ha
        elimninado los posibles ciclos de los caminos de la lista.

            Primero recorremos la lista de caminos en busca de alguna parada
            repetida en el camino, y nos guardamos el numero del camino.

            Para finalizar recorremos la lista de forma inversa para ir
            eliminando los caminos detectados anteriormente.

            Retornamos la lista.
        '''
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
        '''
        Funcion que compara la primera parada del primer camino de la lista con la
        parada objetivo devolviendo false cuando sea el objetivo.
        '''       
        if self.__fichero1[lista[0][0]][1]==self.__fichero1[self.__llegada][1]:
            return False
        else:
            return True
        
     #def Expandir(self, lista):
        '''
        Funcion que Retorna la lista pasada por parametro una vez se ha
        expandido las estaciones posibles del primer camino de esta lista.
        

        Primero nos preparamos una lista 'vecinos' con el identificador
        de las estaciones accessibles desde la primera estacion del
        primer camino.

        Despues nos preparamos otra lista 'caminos' de la misma longitud
        que 'vecinos', donde posteriormente anexaremos los vecinos entrados
        antes y  resto de estaciones que ya teniamos en el camino.

        Para finalizar si la lista de caminos de la clase 'self.__lista'
        no esta vacia anexaremos el resto de caminos que no han sido
        expandidos.

        Retornamos la lista.
        '''
        '''
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
        '''
    def ordenadarLista(self, E, heuristica):
        '''
        Funcion que retorna la lista pasada por parametro ordenada de menor a
        mayor segun la heuristica pasada por parametro.
    
        Primeramente obtenemos una lista con el coste (acomulado + heuristica)
        de cada uno de los caminos de la lista de caminos 'E'

        Para finalizar ordenamos la lista de costes 'costes' generando una
        lista auxiliar 'lista_ordenada' que sera la nueva lista de caminos
        ya ordenada.

        Retornamos la lista.
        '''
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
        '''
        Es la funcion que nos devuelve la heuristica a utilizar.
        '''
        h=0.0
        if metodo == "Distancia":
            x1 = int(self.__fichero1[inicio][3])
            y1 = int(self.__fichero1[inicio][4])
            x2 = int(self.__fichero1[self.__llegada][3])
            y2 = int(self.__fichero1[self.__llegada][4])
            h = sqrt(((x1-x2)*(x1-x2)) + ((y1-y2)*(y1-y2)))
            return h
        else:
            if metodo =="Paradas":
                '''Generamos un coste adicional por cada para realizada para asi buscar el camino con menor numero de paradas posibles'''
                h = paradas*12 
                return h
            else:
                if metodo == "Transbordos":
                    '''Generamos un coste de 20 por cada transbordo asi las diferencias de tiempo entre paradas quedan minimizadas'''
                    h = transbordos*20 
                    return h
                else:
                    raise IndexError ("Error al introducir la heuristica ('distancia' o 'transbordos' o 'paradas'")

    def costeCamino(self, camino, posicion):
        '''
        Funcion que retorna el coste de un camino dado (por camino y posicion)
        y el numero de transbordos de este.

        '''

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
        '''
        Funcion que retorna el coste para ir de una estacion inicio a una
        estacion fin, segun lo establecido en el fichero2 
        '''
        
        if (self.__fichero2[inicio][fin])!=0:
            return self.__fichero2[inicio][fin]
        else:
            raise IndexError ("Camino imposible," + str(self.__fichero1[inicio][1]) + "y "+str(self.__fichero1[fin][1]) +" no tienen conexion")

    def paradasCamino(self, camino):
        indicaciones = ""
        i = len(camino) - 1
        destino = len(camino)
        while (i >= 0):
            if (i != 0) or (i ==len(camino) - 1):
                indicaciones = indicaciones + str(self.__fichero1[camino[i]][1])+ " (linea "+str(self.__fichero1[camino[i]][2])+")"
                if (self.__fichero1[camino[i]][2] != self.__fichero1[camino[i-1]][2]):
                    indicaciones = indicaciones + "\n\n TRANSBORDO!!!!"
                indicaciones = indicaciones + "\n\n" + str(self.__fichero2[camino[i]][camino[i-1]])+" minutos \n\n"
            i = i - 1
        indicaciones = indicaciones + str(self.__fichero1[camino[0]][1])+ " (linea "+str(self.__fichero1[camino[0]][2])+")"
        return indicaciones
