Tab = []
while True:
    n = int(input("Entrez un nombre [0 pour stopper] : "))
    if n == 0:
        break
    Tab.append(n)

max_repetition = 0
max = None

for i in range(len(Tab)):
    rep = Tab.count(Tab[i])  # compte combien de fois Tab[i] apparaît
    if rep > max_repetition:
        max_repetition = rep
        max = Tab[i]

if max is not None:
    print(f"Le nombre le plus répété est ",max, "(" ,max_repetition,")fois")
else:
    print("Aucun nombre n'a été entré.")
