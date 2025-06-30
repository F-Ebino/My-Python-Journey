import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup 
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


url = input("Enter - ")
if len(url) < 1 :
    url = "http://py4e-data.dr-chuck.net/comments_2234458.html"
html = urllib.request.urlopen(url, context = ctx).read()
clean_html = BeautifulSoup(html, "html.parser")

comments = []
total = 0
counts = 0
tags = clean_html("span")
print(tags)
for tag in tags :
    #comments.append(int(tag.contents[0]))
    #print( tag.contents)
    #print(type(tag.contents))
    #print('TAG:', tag)
    #print('URL:', tag.get('href', None))
    #print('Contents:', tag.contents[0])
    #print('Attrs:', tag.attrs
    nums = int(tag.contents[0])
    total = total + nums
    counts = counts + 1
    

#print(sum(comments))
print(total, counts, sep="\r\n\r\n")