import copy
import pdb

def Floyd_W(size,grafo):
    
    for k in range(0,size):
        
        B = []
        for j in range(0,size):
            
            for i in range(0,size):
                if grafo[j * size + i] > 0 and grafo[k * size + i] > 0 and grafo[j * size + k] > 0:
                    B.append(min(grafo[ j * size + i],grafo[k * size + i] + grafo[j * size + k]))
                elif grafo[j * size + i] < 0:
                    if grafo[k * size + i] > 0 and grafo[j * size + k] > 0:
                        B.append(grafo[k * size + i] + grafo[j * size + k])
                    else:
                        B.append(-1)
                elif grafo[k * size + i] < 0 or grafo[j * size + k] < 0:
                    B.append(grafo[j * size + i])
        grafo.clear()
        grafo = B.copy()
        B.clear()
    
    C = []
    for i in range(0,size):
        for j in range(0,size):
            if i == j:
                C.append(-1)
            else:
                C.append(grafo[i * size + j])
        

    return C

def heuristica(C,array_stops,pos):
    return None








A = [-1,2,7,3,-1,-1,4,2,2,2,-1,3,-1,-1,8,9]
C = Floyd_W(4,A)
pdb.set_trace()

D = [1,2,2,2,3,4,4]
E = set(D)
aux = []
for i in E:
    aux.append(i)
pdb.set_trace()