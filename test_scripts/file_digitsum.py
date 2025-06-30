import re

count = 0
total = 0
file = open('regex_sum_2234456.txt')
for line in file :
    line = line.rstrip()
    file_lst = re.findall('[0-9]+', line)

    for digit in file_lst :
        num = float(digit)
        total = total + num
        count = count + 1
print('There are', count, 'values with a total=', total)
print(sum([float(digit) for digit in re.findall('[0-9]+',
     (open('regex_sum_2234456.txt')).read())])
)
