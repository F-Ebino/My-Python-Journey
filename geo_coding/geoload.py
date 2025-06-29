import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

# https://py4e-data.dr-chuck.net/opengeo?q=Ann+Arbor%2C+MI
serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

file_handle = open("where.data")
count = 0
nofound = 0
for line in file_handle:
    #if count > 250 :
        #print('Retrieved 250 locations, restart to retrieve more')
        #break

    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))

    try:
        data = cur.fetchone()[0]
        print("Found in database", address)
        continue
    except:
        pass

    query = dict()
    query['q'] = address

    url = serviceurl + urllib.parse.urlencode(query)

    print('Retrieving', url)
    url_handle = urllib.request.urlopen(url, context=ctx)
    data = url_handle.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        json_data= json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    if not json_data or 'features' not in json_data:
        print('==== Download error ===')
        print(data)
        break

    if len(json_data['features']) == 0:
        print('==== Object not found ====')
        nofound = nofound + 1

    cur.execute('''INSERT INTO Locations (address, geodata)
        VALUES ( ?, ? )''',
        (memoryview(address.encode()), memoryview(data.encode()) ) )

    conn.commit()

    if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

if nofound > 0:
    print('Number of features for which the location could not be found:', nofound)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")