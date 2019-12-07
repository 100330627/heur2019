from itertools import combinations
A = [1,2,3,4,5]
comb = combinations(A,3)
count = 1
for i in comb:
    print(count,":",i)
    count += 1