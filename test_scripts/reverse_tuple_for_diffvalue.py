counts = dict()
friends = [ 'a', 'b', 'c' ]
for x in friends :
    counts[x] = 1
#print(counts)
counts['d'] = counts.get('d', 2)
print(counts)
print(sorted([(y,x) for x , y in counts.items()],  reverse = True   )) 