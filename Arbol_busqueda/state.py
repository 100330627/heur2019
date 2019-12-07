from Bus import Bus
from Children import Children
from itertools import combinations
import re
import copy
import sys
import pdb

#AQUI DEFINIMOS UN ESTADO Y SUS OPERADORES
class State:
    def __init__(self,bus,children,coste_acum):
        # DUDA: AQUI FALTA EL ATRIBUTO PADRE
        self.bus = bus
        self.children = children
        self.coste_acum = coste_acum


    #MOVERME A LAS POSICIONES ADYACENTES
    
    def move(self,mapa,n):
        #MIRO EN QUE PARADA ESTOY
        generados = []
        parada = self.bus.stop

        #Busco los adyacentes en el mapa
        inicio = n * (parada - 1)
        fin = inicio + n

        casillero = mapa.grafo
        #NECESITO SU COSTE E INDICE
        count = 1
        for i in range(inicio,fin):
            if casillero[i] != -1:
                hijos = self.Movimiento(casillero[i],count,mapa.colegios)
                generados = generados + hijos
            count += 1
        
        return generados
    #AQUI ES DONDE VEO LOS NODOS QUE PUEDO EXPANDIR 
    def Movimiento(self,coste,destino,colegios):
        lista_hijos = []
        #MIRO LA PARADA DONDE ESTOY A VER SI PUEDO SUBIR/DEJAR ALGUN NINYO
        #1 Miro si puedo dejar a algun ninyo aqui
        subidos = 0
        for i in colegios:
            if self.bus.stop == i:
                for k in self.children:
                    colegio = re.search('C(.*'r'\s*)', k.escuela)
                    indice = int(colegio.group(1))
                    if colegios[indice - 1] == k.stop:
                        #pdb.set_trace()
                        self.children.remove(k)
              
            

        
        
        
        
        #2 Miro si en la parada hay chavales que puedan subir
        if subidos < self.bus.capacity:
            #DETERMINO CUANTOS PUEDEN SUBIR
            places = self.bus.capacity - subidos

            #MIRO CUANTOS HAY EN LA PARADA,ES DIFERENTE DE SI TODOS CABEN O NO CABEN
            

            #TODOS CABEN
            if self.ChildrenQueue(self.bus.capacity) == True:
                children_queue = self.getChildrenQueue()
                lista_hijos = self.combinaciones(children_queue,places,True)
                
                '''
                s = self.permutechildren_queue(children_queue)
                
                s.bus.stop = destino
                s.coste_acum += coste
                
                
                s.children = self.kids_pos(s.children,destino)
               
                lista_hijos.append(s)
                '''
            #NO TODOS CABEN
            else:
                #LISTA DE NODOS EN EXPANSION
                children_queue = self.getChildrenQueue()
                lista_hijos = self.combinaciones(children_queue,places,False)
               
               
               
                '''
                possibilities = self.GetPossibleNodes(places)
                for s in possibilities:
                    s.coste_acum += coste
                    # Y AQUI IRIA SU HEURISTIQUITA
                  
                    s.children = self.kids_pos(s.children,destino)
                    lista_hijos.append(s)
                    s.bus.stop = destino
                '''  
            for s in lista_hijos:
                s.bus.stop = destino
                s.coste_acum += coste
                
                
                s.children = self.kids_pos(s.children,destino)
        
        #NO CABEN NINYOS Y NO HAY MAS OPCION QUE MOVERME A LA OTRA POSICION
        else:
             s = copy.deepcopy(self)
             s.coste_acum += coste
             s.bus.stop = destino
             s.children = self.kids_pos(s.children,destino)
             lista_hijos.append(s)

        return lista_hijos
            
            
    def ChildrenQueue(self,places):
        
        count = 0
        for i in self.children:
            if i.stop == self.bus.stop and i.isOn == False:
                count += 1

        #TODOS LOS NINYOS DE LA PARADA PUEDEN SUBIR PREPARAMOS EL ESTADO
        return count <= places
    #COLA DE NINYOS QUE ESPERAN       
    def getChildrenQueue(self):
        cola = []
        for i in self.children:
            if i.stop == self.bus.stop and i.isOn == False:
                cola.append(i)
        return cola

    #PONGO LOS PRIMEROS DE LA COLA CHILDREN A LOS QUE ESTEN EN EL BUS CUANDO CABEN TODOS
    def permutechildren_queue(self,children_Queue):
        s = copy.deepcopy(self)
        
        for i in children_Queue:
            for j in s.children:
                if i.stop == j.stop and i.escuela == j.escuela and j.isOn == False:
                    print("ESTOY EN ",j.stop," VOY A ",j.escuela," Y ME ACABO DE SUBIR AL BUS")
                    chavalote = s.children.pop(s.children.index(j))
                    chavalote.isOn = True
                    s.children.insert(0,chavalote)
                    break
       
        
        return s


    #NO TODOS LOS NINYOS PUEDEN SUBIR
    
    def GetPossibleNodes(self,places):
            comb_list = []
            children_Queue = self.getChildrenQueue()
            comb = combinations(children_Queue, places)
            #CADA UNA DE LAS COMBINACIONES ES UN ESTADO Y LO TENEMOS QUE TRATAR POR SEPARADO
           
            for i in comb:
                s = self.permutechildren_queue(i)
                
                comb_list.append(s)
                   
                
                
            return comb_list
    
    #CAMBIO LA POSICION DE LOS NINYOS
    def kids_pos(self,lista_hijos,nexthop):
        for i in (j for j in lista_hijos if j.isOn == True):
            i.stop = nexthop
        return lista_hijos

    def combinaciones(self,cola_ninyos,places,todos_caben):
       
        if todos_caben == True:
            lista = self.comb_cola(cola_ninyos)
            return lista
        else:
            lista_comb = []
            comb = combinations(cola_ninyos, places)
            for i in comb:
                lista = self.comb_cola(i)
                lista_comb = lista_comb + lista.copy()
            return lista_comb

    def comb_cola(self,cola_ninyos):
        lista_estados = []
        rango = int(pow(2,len(cola_ninyos)))
        for i in range(0,rango):
            count = 0
            s = copy.deepcopy(self)
            while pow(2,count) <= i:
                if int(i/int(pow(2,count)))% 2 == 1:
                    s.children[count].isOn = True        
                count += 1

            #pdb.set_trace()
            lista_estados.append(s)
        return lista_estados
