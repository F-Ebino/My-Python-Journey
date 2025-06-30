import re
import sqlite3

db_connect = sqlite3.connect('domains.sqlite')
db_cursor = db_connect.cursor()

db_cursor.execute('DROP TABLE IF EXISTS Counts')

db_cursor.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

file_name = input("Enter file name: ")
if (len(file_name) < 1):
    file_name = "mbox.txt"
file_handle = open(file_name)
for line in file_handle:
    if not line.startswith("From: "):
        continue
    domain_list = re.findall(r"@(\S+)", line)
    domain = domain_list[0]

    db_cursor.execute('SELECT count FROM Counts WHERE org = ? ', (domain,))
    row = db_cursor.fetchone()
    if row is None:
        db_cursor.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (domain,))
    else:
        db_cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (domain,))
    db_connect.commit()

# https://www.sqlite.org/lang_select.html
table_10 = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in db_cursor.execute(table_10):
    print(str(row[0]), row[1])

db_cursor.close()