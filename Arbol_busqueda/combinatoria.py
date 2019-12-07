from itertools import combinations
A = [1,2,3,4,4]
comb = combinations(A,2)
count = 1
for i in comb:
    print(count,":",i)
    count += 1