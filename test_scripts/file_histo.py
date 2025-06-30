histogram = dict()
emails = list()
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
        emails.append(list[1])

for email in emails :
    histogram[email] = histogram.get(email, 0) + 1

mail = None
frq = None
for email,count in histogram.items() :
    if mail is None or count > frq :
        mail = email
        frq = count
print(mail, frq)