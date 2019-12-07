from math import pow
from math import sqrt
import pdb
import copy

lista_listas = []
A = [1,2,3,4,5,6,7,8]
rango = int(pow(2,len(A)))
for i in range(0,rango):
    lista_temp = []
    count = 0
    while pow(2,count) <= i:
        if int(i/int(pow(2,count)))% 2 == 1:
            if i == 16 or i == 32:
                pdb.set_trace()
            lista_temp.append(A[count])
        count += 1
    lista_listas.append(lista_temp.copy())


for i in lista_listas:
    print(lista_listas.index(i),end = ': ')
    for j in i:
        print(j,end = ' ')
    print()