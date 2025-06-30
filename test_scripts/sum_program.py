count = 0
sum = 0
while True :
    inp = input("Enter a number: ")
    if inp == "done" :
        break
    try :
        num = int(inp)
        sum = sum + num
        count = count + 1
    except :
        print("invalid input")
if count == 0 :
    quit()
print(sum, count, sum/count)