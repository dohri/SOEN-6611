import urllib2
from bs4 import BeautifulSoup as beau
import re
import os
from random import randint
import time

def download_bug(bugno,url):
		web_page = urllib2.urlopen(url)
#		htm = urllib2.urlopen(url)
		soup  = beau(web_page)
		bugnumber = bugno + '.html'
		print bugnumber
		s = open(bugnumber,'w')
		s.write(str(soup))


url = open("bugs_conf.txt",'r').readlines()
root = url[-1]
root = root.split("root_directory = ")
for i in root:
	r = i
r = r.rstrip()
'''
del url[-1]
temp = []
for n in url:
    x = n.split("url = ")
    temp.append(x[-1])
'''
url1 = url[0]
url1 = url1.split("url = ")
for i in url1:
	url2 = i
htm = urllib2.urlopen(url2)
#htm = urllib2.urlopen("https://f-droid.org/repository/browse/?fdid=uk.org.crimetalk")
soup  = beau(htm)
#s = open('web.html','w')
#print(e)
elm = soup.findAll('a')

lst = []
for i in elm:
    x = i.attrs["href"]
    lst.append(x)
#    print(i.attrs["href"])
#print(lst)
temp = []
for i in lst:
    if "/browse/" in i:
        temp.append(i)
t1 = []
for i in temp:
    x = i.split("/browse/")
    t1.append(x[-1])
#print(t1)
temp = []
temp2 = []
for i in t1:
    x = i.split("-")
    temp.append(x[-1])
    temp2.append(x[0])
    
bug_name = temp2[0]

temp1 = []
x = 0
for i in temp:
	temp1.append(int(i))
	x = x + 1
#print(temp1)
bugno = temp1
print(bugno)


print('This web page has bug follwing bug numbers with range:'+ temp[-1] + "-" + temp[0] + ":: TOTAL bugs: " + str(x))
print('Please enter range of bugs to be downloaded in increasing order that is smallest to largest')
rng = input("enter starting number starting from:")
rng1 = input("enter end number:")
ip = temp.index(str(rng))
ip2 = temp.index(str(rng1))
#print(ip,"::",ip2)
temp = temp[int(ip2):int(ip)]
temp3 = []
os.mkdir(r)
os.chdir(r)
for i in temp: 
	bugnumb = i
	i = "https://hibernate.atlassian.net/browse/" + bug_name + "-" + i
	download_bug(bugnumb,i)
	time_out = randint(1,60)
	print("Next bug will be downloaded after " + str(time_out) + "Sec")
	time.sleep(time_out)
	
	
#print temp3
'''

	
'''

#for i in temp:
#	if str(rng) in i:
#		indx = temp.index(str(rng))
#	if str(rng1) in i:
#		indx2 = temp.index(str(rng))
#print('\n\nINDEX:' +  str(indx) + ":: " + str(indx2))
		
raw_input("press enter to exit ;")
'''
lis = []
for i in lst:
    if "github" in i:
        if not re.search(r"issues$",i):
            lis.append(i)
temp = lis[-1]
if re.search(r"/$",temp):
    temp = temp[:-1]
    print(temp)
else:
    print(temp)
'''

            
