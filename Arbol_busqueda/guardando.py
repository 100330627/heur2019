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
    
    print("EXPANSIOOOOOOOOON ",count)
    for i in lista_generados:
        print("NODO ",lista_generados.index(i),": ")
        
        for k in i.children:

            print(i.children.index(k)," estoy en ",k.stop, " voy a ", k.escuela," y estoy en el bus es ",k.isOn)
        print("Me ha valido ",i.coste_acum,)

    #LA MANERA DE ORDENAR LOS HIJOS QUE NO QUIEREN QUE CONOZCAS

    generados_ordenada = sorted(lista_generados, key=lambda x: x.coste_acum, reverse=False)
    for i in generados_ordenada:
        contador_id += 1
        i.id = contador_id
    nodos_generados = merge(generados_ordenada,nodos_generados)
    
    count += 1 
    
    s = nodos_generados.pop(0)
    
    
    while reexpansion(lista_expandidos,s) == True:
        s = nodos_generados.pop(0)
        if len(nodos_generados) == 0:
            print("NO SOLUCION")
            sys.exit(-1)
    
Buscar_padre(s,lista_expandidos)