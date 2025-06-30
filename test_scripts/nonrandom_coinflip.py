print("Enter a number between 0 and 100:")
while True :
    inp = input("> ")
    num = float(inp)
    if num < 50 :
        print("tails")
    elif num > 50 :
        print("heads")
    elif num == 50 :
        print("except 50")
        print("try again")
        continue
    break
if num > 50 :
    print("you go first.")
elif num < 50 :
    print("you go second.")