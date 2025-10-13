Tab= []
while True:
    n = int(input("Entrez un nombre [0 pour stopper] : "))
    if n == 0:
        break
    Tab.append(n)

print("la liste 1 est :", Tab)
tab2=[x for x in Tab if Tab.count(x) >=2 ]
tab2=list(set(tab2))

print("la liste 2 est  :", tab2)
