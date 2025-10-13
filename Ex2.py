Tab =[]
i=0
for i in range(5):
    i=i+1
    print("iteration numero ", i)
    print("vous etes a la saisie numero ", i)
    n = int(input("Entrez un nombre : "))
    Tab.append(n)



Tab.sort()
s=sum(Tab)
print("la liste triee est :", Tab)
print("la somme des elements de la liste est :", s)