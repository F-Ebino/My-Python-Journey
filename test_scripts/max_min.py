max = None
min = None
while True :
    inp = input("Enter a number: ")
    if inp == "done" :
        break
    try :
        num = int(inp)
    except :
        print("invalid input")
        continue
    if max is None :
        max = num
    elif max <  num :
        max = num
    if min is None :
        min = num
    elif min > num :
        min = num
print("Maximum is", max)
print("Minimun is", min)