#1
notes =[]
#2 
notes.append(1)
notes.append(2)
notes.append(3)
#3
#print(notes)
#4
notes.remove(2)
#5
print(notes)
#6
s=notes.count(0)
print("le nombre d'occurence de 3 est:", s)
#7 
m=len(notes)
print("il ya ", m ,"elements dans la liste")
#8

if m>=0:
    print("la liste n'est pas vide")
else:
    print("la liste est vide")
#9
notes.insert(0,5)
print(notes)