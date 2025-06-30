import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup 
import ssl
import re

url = input("Enter url >> ")
if len(url) < 1 : 
    url = " http://py4e-data.dr-chuck.net/comments_2234461.json"
web_data = urllib.request.urlopen(url).read()
parsed_data = json.loads(web_data)
data_list = parsed_data["comments"]

counts = []
loops = 0
for dict in data_list :
    print(dict)
    counts.append(float(dict["count"]))
    loops += 1

print(sum(counts), loops, sep="\n\n")
