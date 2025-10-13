Tab = []
Tab1 = []


while True:
    n = int(input("Entrez un nombre [0 pour stopper] : "))
    if n == 0:
        break
    Tab.append(n)

for i in range(len(Tab)):
    if Tab[i] % 2 != 0:  # vérifier si le nombre est impair
        Tab1.append(Tab[i])
  
      
print("les nombres premiers sont :", Tab1)
     

