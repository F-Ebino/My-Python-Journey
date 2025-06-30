score = input("Enter Score: ")
try :
    scr = float(score)
except :
    print("Error, please enter a numeric value between 0.0 and 1.0")
    quit()
#A >= 0.9
#B >= 0.8
#C >= 0.7
#D >= 0.6
#F < 0.6
if scr >= 0.9 :
    print("A")
elif scr >= 0.8 :
    print("B")
elif scr >= 0.7 :
    print("C")
elif scr >= 0.6 :
    print("D")
elif scr < 0.6 :
    print("F")