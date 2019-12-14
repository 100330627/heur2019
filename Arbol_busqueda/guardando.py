from lectura import leer_fichero
from lectura import getSize
from lectura import LeerPosiciones
from lectura import GetColegios
from lectura import GetChildren
from lectura import GetBus
from static_inf import Mapa
from Children import Children
from state import State
from array import array
from merge import merge
from merge import isFinal
from merge import reexpansion
from merge import Buscar_padre

import sys
import pdb

import copy
#EN ESTE FICHERO VAMOS A GUARDAR EL ESTADO INICIAL DEL PROGRAMA LO QUE OCURRIRA A CONTINUACION TE SORPRENDERA


#LOS PROFESORES DE HEURISTICA ODIAN A ESTE TIPO ASI ES COMO GUARDA SUS NODOS

#GENERADOS
nodos_generados = []

#EXPANDIDOS
lista_expandidos = []

# Obtengo el contenido del fichero, le paso una posicion y la anterios
lineas = leer_fichero()

#Leo el contenido

#1 Tamanyo del grafo n * n
n = getSize(lineas[0])
#2 Vamos a leer el grafo

#Leo todos los valores
casillas = array('l')
#3 Guardo el array con los costes del grafo
for i in range(1,n+1):
    temp_array = LeerPosiciones(lineas[i],i+1,n)
    casillas = casillas+temp_array
#4 guardo la posicion de los colegios
colegios = GetColegios(lineas[n + 1],n+2)
print(colegios)
#5 Obtengo la información dinamica

#5.1 Posicion inicial de los infantes
kids = GetChildren(lineas[ n + 2], n+3)

#5.2 Posicion del bus
bus = GetBus(lineas[n + 3],n+4)

#La informacion estatica la tengo en este objeto
map = Mapa(casillas,n,colegios)

#DUDA, esto habria que mejorarlo
#Tengo que crear objetos children según vea en mi tupla paradas
children_list = []
for i in kids:
    for j in i:
        for k in range(0,j[1]):
            children_list.append(Children(j[0],j[2],False))

#METO UN ESTADO
father = 0
contador_id = -1
initial = State(bus,children_list,0,father,contador_id)
partida = initial.bus.stop
nodos_generados.append(initial)
#Saco el primero de la lista de generados
s = nodos_generados.pop(0)
count = 0


while isFinal(s,partida) == False:
   
    lista_expandidos.append(s)
    lista_generados = s.move(map,n)
    '''
    if s.id == 1 or s.id == 0 or s.id == 5 or s.id == 14 or s.id == 30 or s.id == 45 or s.id == 63 or s.id == 100 or s.id == 134 or s.id == 191:
        pdb.set_trace()
    '''
    #LA MANERA DE ORDENAR LOS HIJOS QUE NO QUIEREN QUE CONOZCAS

    generados_ordenada = sorted(lista_generados, key=lambda x: x.coste_acum, reverse=False)
    for i in generados_ordenada:
        contador_id += 1
        i.id = contador_id
    nodos_generados = merge(generados_ordenada,nodos_generados)
    
    count += 1 
    try:
        s = nodos_generados.pop(0)
    except IndexError:
        print("NO SOLUCION")
        sys.exit(0)
    
    for i in generados_ordenada:
        print("Soy ",i.id," Hijo de ",i.father)
        for k in i.children:
            print("Voy a ",k.escuela," estoy en ",k.stop," voy en el bus es ",k.isOn) 
        print("################################################################################")
    
    



    while reexpansion(lista_expandidos,s) == True and len(nodos_generados) > 0:
        try:
            s = nodos_generados.pop(0)
        except IndexError:
            print("NO SOLUCION")
            sys.exit(0)

    
    

Buscar_padre(s,lista_expandidos)
