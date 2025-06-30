count = dict()
while True :
    inp = input("Enter a file name: ")
    try :
        file = open(inp)
        break
    except :
        print("invalid file name")
for line in file :
    if line.startswith("From ") :
        list = line.split()
        list = list[5]
        hrs = list[:2]
        #print(hrs)
        count[hrs] = count.get(hrs, 0) +1

for hr, frq in sorted(count.items()) :
    print(hr, frq)