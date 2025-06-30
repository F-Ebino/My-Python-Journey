endlist = list()
while True :
    inp = input("Enter file name: ")
    try :
        file = open(inp)
        break
    except :
        print("invalid file name")
for line in file :
    list = line.split()
    for word in list : 
        if word not in endlist : #creates a list that contains a word only once
            endlist.append(word)
endlist.sort()
print(endlist)