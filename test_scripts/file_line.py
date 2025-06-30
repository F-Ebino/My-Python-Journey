count = 0
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
        print(list[1])
        count = count + 1
if count == 0 :
    print("oopsie")
    quit()
print("There were", count, "lines in the file with From as the first word")