import copy
A = [1,2,3,4]
i = 2

count =  0
C = []
while pow(2,count) <= i:
    B = []
    if int(i/int(pow(2,count)))% 2 == 1:
        B.append(A[count])       
    count += 1
    C.append(B.copy())