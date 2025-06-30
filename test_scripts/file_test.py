sum = 0
count = 0
while True :
    inp = input("Enter a file name: ")
    try :
        file = open(inp)
        break
    except :
        print("invalid file name")
for line in file :
    if line.startswith("X-DSPAM-Confidence: ") :
        idx = line.find("0")
        decmls = line[idx:]
        num = float(decmls)
        sum = sum + num
        count = count + 1
if count == 0 :
    print("oopsie")
    quit()
avg = sum/count
print("Average spam confidence:", avg)
    #line = line.rstrip()
    #line = line.upper()
    #print(line)