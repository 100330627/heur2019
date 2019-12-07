from state import State
from merge import reexpansion
from Children import Children
from Bus import Bus

b = Bus(2,5)
b2 =Bus(5,5)

c1 = Children(3,"C1",True)
c2 = Children(3,"C1",True)
c3 = Children(3,"C2",True)
c4 = Children(4,"C4",False)
c5 = Children(7,"C6",False)
c6 = Children(1,"C1",False)
c7 = Children(2,"C1",False)
c8 = Children(2,"C1",False)
c9 = Children(5,"C3",True)
c10 = Children(5,"C6",True)
c11 = Children(5,"C2",False)
c12 = Children(3,"C4",False)
c13 = Children(9,"C6",False)
c14 = Children(9,"C1",False)
c15 = Children(9,"C3",False)
c16 = Children(4,"C6",False)
c17 = Children(3,"C1",False)
c18 = Children(3,"C2",False)
c19 = Children(2,"C6",False)
c20 = Children(3,"C2",False)

l1 = [c1,c2,c3,c4,c5,c17,c6,c7,c18,c8,c20]
l2 = [c1,c2,c3,c18,c4,c5,c17,c6,c8,c7,c19]
l3 = [c9,c10,c1,c2,c3,c4]
l4 = [c13,c14,c15,c16]
l5 = [c1,c2]
l6 = [c1,c2,c3,c18,c4,c5,c17,c6,c8,c7,c16]
s1 = State(b,l1,7)
s2 = State(b,l1,9)
s3 = State(b2,l3,12)
s4 = State(b2,l4,15)
s5 = State(b,l5,40)
s6 = State(b,l6,8)
expandidos = [s3,s5,s6,s4,s2]
print(reexpansion(expandidos,s1))

