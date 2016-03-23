class LinkedList(object):
        """
        Linked list class
        """
        __slots__=['__head','__tail','__cost']
        
        class Element(object):
                __slots__=['__data','__next','__list']
                def __init__(self, lis, data, next):
                        self.__list = lis
                        self.__data = data
                        self.__next = next
                def getData(self):
                        return self.__data                        
                data = property(fget = lambda self: self.getData())
                def getNext(self):
                        return self.__next
                next = property(fget = lambda self: self.getNext())
                def insertAfter(self, item):
                        self.__next = LinkedList.Element(self.__list, item, self.__next)
                        if self.__list._LinkedList__tail is self:
                                self.__list._LinkedList__tail = self.__next
                def insertBefore(self, item):
                        NuevoNodo = LinkedList.Element(self.__list, item, self)
                        if(self is self.__list._LinkedList__head):
                                self.__list._LinkedList__head = NuevoNodo
                        else:
                                temp=self.__list._LinkedList__head
                                while(temp is not self.__list._LinkedList__tail):
                                        if(temp.__next is self):
                                                temp.__next=NuevoNodo
                                                break
                                        else:
                                                temp=temp.__next
                                                if(temp is self.__list._LinkedList__tail):
                                                       raise IndexError

                def extract(self):


                        if (self == self.__list._LinkedList__head):
                                if(self == self.__list._LinkedList__tail):
                                        self.__list._LinkedList__head = self.__list._LinkedList__tail = self = None
                                        
                                else:
                                
                                        self.__list._LinkedList__head = self.__next
                                        self = None

                        else:
                                temp=self.__list._LinkedList__head
                                
                                while(temp != self.__list._LinkedList__tail):
                                    

                                        if(temp.__next is self):
                                                if(self.__list._LinkedList__tail is self):
                                                        
                                                        self.__list._LinkedList__tail = temp
                                                        self=None
                                                        temp.__next=None
                                                        break  
                                                else:
                                                        temp.__next=self.__next
                                                        self=None
                                                        break
                                        else:
                                                temp=temp.__next
                                               
                                
         
                               
                                        

                      
        def __init__(self):
                self.__head = None
                self.__tail = None
                self.__cost = None

        def setCost(self,coste):
                self.__cost=coste
        def getCost(self):
                return self.__cost
        def purge(self):
                self.__head = None
                self.__tail = None
        def getHead(self):
                return self.__head
        head = property(fget = lambda self: self.getHead())
        def getTail(self):
                  return self.__tail
        tail = property(fget = lambda self: self.getTail())
        def getIsEmpty(self):
                if((self.__head == None) and (self.__tail == None)):
                        return True
                else:
                        return False
        isEmpty = property(fget = lambda self: self.getIsEmpty())
        def getFirst(self):
                if (self.getIsEmpty() == True):
                        raise IndexError
                else:
                        return self.__head.getData()
      
        first = property(fget = lambda self: self.getFirst())
        def getLast(self):
                if self.getIsEmpty() == True:
                        raise IndexError
                else:
                        return self.__tail.getData()
        last = property(fget = lambda self: self.getLast())
        
        def prepend(self, item):
                if self.getIsEmpty():
                        NouNode=self.Element(self,item,None)
                        self.__tail = NouNode
                        self.__head = NouNode
                else:
                        self.__head.insertBefore(item)
                
                        
        def append(self, item):
                if self.getIsEmpty():
                        NouNode=self.Element(self,item,None)
                        self.__tail = NouNode
                        self.__head = NouNode
                else:
                        self.__tail.insertAfter(item)
        def __copy__(self):
                
               temp = LinkedList()
        
               if self.isEmpty:
                    return temp
               else:
                    t = self.head
                    while t != None:
                       temp.append(t.data)
                       t = t.next
                    return temp
        def extract(self, item):
                x=0
                if(self.isEmpty):
                        raise IndexError
                else:
                        temp = self.__head
                        while (temp != None):
                                if(temp.getData() == item):
                                        temp.extract()
                                x=x+1
                                temp = temp.getNext()
                        
                                
        def __str__(self):
                lista = '{'
                lista = str(lista)
                count = 0
                if(self.getIsEmpty()==False):
                        Node=self.getHead()
                        while(Node!=None):
                                if(Node!=None):
                                        if(Node.getNext() != None):
                                                lista += str(Node.getData())+", "
                                        else:
                                                lista += str(Node.getData())
                                count += 1
                                Node = Node.getNext()
                lista += "}"
                return lista
