Tab1 = []
Tab2 = []
Tab3 = []
t=0
r=0
print("saisir des nombres de tble 1")
while True:
    t=t+1
    n = int(input("Entrez un nombre de table 1 [tape 0 pour stop] : "))
    if n == 0:
        break
    Tab1.append(n)
print("saisir des nombres de tble 2")
for i in range(t):
    n = int(input("Entrez un nombre de table 2  :"))
    Tab2.append(n)
for i in range(len(Tab1)):
    r=Tab1[i]
    if r in Tab2:
        Tab3.append(r)
print("la liste 1 est :", Tab1)
print("la liste 2 est :", Tab2)
print("les elements communs aux deux listes sont :", Tab3)