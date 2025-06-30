import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup 
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter - ")
if len(url) < 1 :
    url = " http://py4e-data.dr-chuck.net/known_by_Keleigh.html"
html = urllib.request.urlopen(url, context = ctx).read()
clean_html = BeautifulSoup(html, "html.parser")
#print(isinstance(clean_html, str))
#print(type(html))
#print(type(clean_html))
#print(clean_html.decode)
process = 0

while process < 7 :
    links =[]
    tags = clean_html('a')
    for tag in tags:
        links.append(tag.get('href', None))
    html = urllib.request.urlopen(links[17], context = ctx).read()
    clean_html = BeautifulSoup(html, "html.parser")
    process = process + 1
print(type(links))
print(type(links[17]))
print(links[17])
    
   