import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup 
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'
while True :
    address = input("Enter location >>")
    if len(address) < 1 :
        address = "Faculté de Médecine et de Pharmacie Marrakech, Morocco"
    address = address.strip()
    query = {}
    query["q"] = address

    url = serviceurl + urllib.parse.urlencode(query)
    raw_data = urllib.request.urlopen(url, context = ctx).read()
    print(type(raw_data))
    #parsed_data = json.loads(raw_data)
    data = raw_data.decode()
    

    try :
        parsed_data = json.loads(data)
    except :
        parsed_data = None

    if not parsed_data or 'features' not in parsed_data:
        print('==== Download error ===')
        print(data)
        break

    if len(parsed_data['features']) == 0:
        print('==== Object not found ====')
        print(data)
        break

    #print(json.dumps(parsed_data, indent=4))
    try:
        print(parsed_data["features"][0]['geometry']['coordinates'][1])
        print(parsed_data['features'][0]['geometry']['coordinates'][0])
        print(parsed_data['features'][0]['properties']['display_name'])
        where = parsed_data['features'][0]['properties']['display_name']
        where = where.replace("'", "")
        print(where)  

    except:
        #print(type(parsed_data["features"][0]["properties"]["plus_code"]))
        print(json.dumps(parsed_data, indent=4))
    # parsed_data["features"][0]["properties"]["plus_code"]
