from math import pow
import copy
import pdb
lista = [1,2,3,4,5,6]
lista_listas = []
print(pow(2,3))
sup = int(len(lista))
for i in range(0,int(pow(2,sup))):
    lista_temp = []
    if (int((i/1)) %2) == 1:
        lista_temp.append(lista[0])
    if (int((i/2))%2) == 1:
        lista_temp.append(lista[1])
    if (int((i/4))%2) == 1:
        lista_temp.append(lista[2])
    if (int((i/8))%2) == 1:
        lista_temp.append(lista[3])
    if (int((i/16))%2) == 1:
        lista_temp.append(lista[4])
    if (int((i/32))%2) == 1:
        lista_temp.append(lista[5])
    
    lista_listas.append(lista_temp.copy())
    print(i,": ",len(lista_temp))
for i in lista_listas:
    print(lista_listas.index(i),": ",end = ' ')
    for j in i:
        print(j,end=' ')
    print()
