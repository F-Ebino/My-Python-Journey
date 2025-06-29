import sqlite3
import json
import codecs

conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
file_handle = codecs.open('where.js', 'w', "utf-8")
file_handle.write("myData = [\n")
count = 0
for row in cur :
    data = str(row[1].decode())
    try: json_data= json.loads(str(data))
    except: continue

    if len(json_data['features']) == 0: continue

    try:
        lat = json_data['features'][0]['geometry']['coordinates'][1]
        lng = json_data['features'][0]['geometry']['coordinates'][0]
        where = json_data['features'][0]['properties']['display_name']
        where = where.replace("'", "")
    except:
        print('Unexpected format')
        print(json_data)

    try :
        print(where, lat, lng)

        count = count + 1
        if count > 1 : file_handle.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        file_handle.write(output)
    except:
        continue

file_handle.write("\n];\n")
cur.close()
file_handle.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")

