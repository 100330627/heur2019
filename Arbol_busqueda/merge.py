from state import State
import copy
#AQUI ORDENAMOS LOS NODOS EN FUNCION A SU FUNCIONDE COSTE, 
#COMO ARGUMENTOS SE PASAN LAS LISTAS DE NODOS RECIEN GENERADOS
# Y LOS GENERADOS DE ITERACIONES ANTERIORES
def merge(lista1,lista2):
    ordenados = []
    conlista1 = 0
    conlista2 = 0
    if len(lista1) == 0:
        return lista2
    if len(lista2) == 0:
        return lista1
    while True:
       if lista1[conlista1].coste_acum > lista2[conlista2].coste_acum:
           ordenados.append(lista2[conlista2])
           conlista2 += 1
       else:
           ordenados.append(lista1[conlista1])
           conlista1 += 1
       #ESTO SEGURO QUE HAY UNA FORMA MEJOR DE HACERLO
       if conlista1 == len(lista1):
            for i in range(conlista2,len(lista2)):
                ordenados.append(lista2[i])
            return ordenados
       if conlista2 == len(lista2):
            for i in range(conlista1,len(lista1)):
                ordenados.append(lista1[i])
            return ordenados
        
#Comprobar si es un estado final 
def isFinal(s,partida):

    return (len(s.children) == 0 and s.bus.stop == partida)

def reexpansion(expandidos,s):
    for i in expandidos:
        #compruebo que el nodo de expandidos que estamos analizando no esta en la misma parada ni tiene el mismo coste acumulado
        if i.bus.stop == s.bus.stop:
            #Compruebo que no haya el mismo numero de ninyos
            if len(i.children) == len(s.children):
                #Si se cumple todo eso que no esten todos en la misma posicion,ordeno las dos listas por parada y comparo uno a uno
                sorted(i.children, key=lambda x: x.stop, reverse=False)
                sorted(s.children, key=lambda x: x.stop, reverse=False)
                flag = True
                for j in range(0,len(s.children)):
                    if i.children[j].stop != s.children[j].stop or i.children[j].escuela != s.children[j].escuela or i.children[j].isOn != s.children[j].isOn:
                        flag = False
                        break
                if flag == True:
                    return True

    
    return False


def Buscar_padre(s,lista_expandidos):
    
    id = s.father
    while id != -1:
        for i in lista_expandidos:
            if i.id == id:
                print(i.bus.stop,end=' -->')
                id = i.father
                break

    sorted(lista_expandidos, key=lambda x: x.id, reverse=False)
    print(lista_expandidos.pop(0).bus.stop)
