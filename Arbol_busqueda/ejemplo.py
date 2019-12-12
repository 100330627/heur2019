import pdb
import copy
A = [2,3,4,5,6,7]
B = A.copy()
for i in A:
    B.remove(i)
    print("iiiiiiiiiiii")
pdb.set_trace()