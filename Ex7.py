Tab= []
while True:
    n = int(input("Entrez un nombre [0 pour stopper] : "))
    if n == 0:
        break
    Tab.append(n)

print("la liste des longueurs des mots est :", Tab)
for i in range(len(Tab)):
    if Tab [i] < 0 :
        Tab.remove(Tab[i])
        Tab.insert(i,0)
print("la liste des longueurs des mots est :", Tab)
