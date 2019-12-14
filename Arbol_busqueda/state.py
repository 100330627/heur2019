from Bus import Bus
from Children import Children
from itertools import combinations
import re
import copy
import sys
import pdb

#AQUI DEFINIMOS UN ESTADO Y SUS OPERADORES
class State:
    def __init__(self,bus,children,coste_acum,father,id):
        # DUDA: AQUI FALTA EL ATRIBUTO PADRE
        self.bus = bus
        self.children = children
        self.coste_acum = coste_acum
        self.father = father
        self.id = id


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
        
        clon = copy.deepcopy(self)
        clon.father = self.id
        '''
        if clon.father == 7 and clon.bus.stop == 9:
            pdb.set_trace()
        '''
        for i in colegios:
            if clon.bus.stop == i:
                lista_ej = []
                for k in clon.children:
                    
                    colegio = re.search('C(.*'r'\s*)', k.escuela)
                    indice = int(colegio.group(1)) 
                    flag = True
                    if colegios[indice - 1] == k.stop:
                        
                        flag = False
                        
                    
                    if flag == True:
                        lista_ej.append(k)
                clon.children.clear()
                clon.children = lista_ej
        subidos = 0 
        for i in (k for k in clon.children if k.isOn == True):
            subidos += 1
        
        
        #2 Miro si en la parada hay chavales que puedan subir
        if subidos < clon.bus.capacity:
            #DETERMINO CUANTOS PUEDEN SUBIR
            places = clon.bus.capacity - subidos

            #MIRO CUANTOS HAY EN LA PARADA,ES DIFERENTE DE SI TODOS CABEN O NO CABEN
            

            #TODOS CABEN
            if self.ChildrenQueue(clon,clon.bus.capacity) == True:
                children_queue = self.getChildrenQueue(clon)
                lista_hijos = self.combinaciones(clon,children_queue,places,True)

            #NO TODOS CABEN
            else:
                #LISTA DE NODOS EN EXPANSION
                children_queue = self.getChildrenQueue(clon)
                lista_hijos = self.combinaciones(clon,children_queue,places,False)
               

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
        for k in lista_hijos:
            if self.reexpansion_padre(k) == True:
                lista_hijos.remove(k)
        return lista_hijos
            
            
    def ChildrenQueue(self,clone,places):
        
        count = 0
        for i in clone.children:
            if i.stop == clone.bus.stop and i.isOn == False:
                count += 1

        #TODOS LOS NINYOS DE LA PARADA PUEDEN SUBIR PREPARAMOS EL ESTADO
        return count <= places
    #COLA DE NINYOS QUE ESPERAN       
    def getChildrenQueue(self,clone):
        cola = []
        for i in clone.children:
            if i.stop == clone.bus.stop and i.isOn == False:
                cola.append(i)
        return cola

    #PONGO LOS PRIMEROS DE LA COLA CHILDREN A LOS QUE ESTEN EN EL BUS CUANDO CABEN TODOS
  
    #CAMBIO LA POSICION DE LOS NINYOS
    def kids_pos(self,lista_hijos,nexthop):
        for i in (j for j in lista_hijos if j.isOn == True):
            i.stop = nexthop
        return lista_hijos

    def combinaciones(self,clone,cola_ninyos,places,todos_caben):
       
        if todos_caben == True:
            lista = self.comb_cola(clone,cola_ninyos)
           
            return lista
        else:
            lista_comb = []
            comb = combinations(cola_ninyos, places)
            for i in comb:
                lista = self.comb_cola(clone,i)
                lista_comb = lista_comb + lista.copy()
            return lista_comb

    def comb_cola(self,clon,cola_ninyos):
        lista_estados = []
        rango = int(pow(2,len(cola_ninyos)))
        for i in range(0,rango):
            count = 0
            s = copy.deepcopy(clon)
            for k in s.children:
                if k.stop == s.bus.stop and k.isOn == False:
                    s.children.remove(k)
            while pow(2,count) <= i:
                if int(i/int(pow(2,count)))% 2 == 1:
                    cola_ninyos[count].isOn = True        
                count += 1
            s.children = s.children + cola_ninyos
            lista_estados.append(s)
        return lista_estados

    def reexpansion_padre(self,i):
        if i.bus.stop == self.bus.stop:
                #Compruebo que no haya el mismo numero de ninyos
                if len(i.children) == len(self.children):
                    #Si se cumple todo eso que no esten todos en la misma posicion,ordeno las dos listas por parada y comparo uno a uno
                    sorted(i.children, key=lambda x: x.stop, reverse=False)
                    sorted(self.children, key=lambda x: x.stop, reverse=False)
                    flag = True
                    for j in range(0,len(s.children)):
                        if i.children[j].stop != self.children[j].stop or i.children[j].escuela != self.children[j].escuela or i.children[j].isOn != self.children[j].isOn:
                            flag = False
                            break
                    if flag == True:
                        return True