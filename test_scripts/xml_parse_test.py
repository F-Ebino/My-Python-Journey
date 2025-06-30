import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup 
import ssl
import re


url = input("Enter url >> ")
if len(url) < 1 : 
    url = "http://py4e-data.dr-chuck.net/comments_2234460.xml"
html = urllib.request.urlopen(url).read()
xml = ET.fromstring(html)

counts = xml.findall('comments//count')
nums = []
loops = 0
for count in counts :
   nums.append(float(count.text))
   loops += 1

print(sum(nums), loops, sep="\n\n")

