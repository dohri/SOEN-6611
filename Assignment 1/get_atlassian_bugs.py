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
#print(url)
for i in url:
	if "url" in i:
		url1 = i
	if "project_tag" in i:
		project_tag = i
	if "bug_start" in i:
		bug_start = i
	if "bug_end" in  i:
		bug_end = i
	if "max_timeout_secs" in i:
		max_timeout_secs = i
	if "root_directory" in i:
		root = i

root = root.split("root_directory = ")
for i in root:
	r = i
r = r.rstrip()
#print(r)

url1 = url[0]
url1 =  url1.split("url = ")
for i in url1:
	url2 = i
url2 = url2.rstrip()
#print(url2)

project_tag = project_tag.split("project_tag = ")
for i in project_tag:
	project_tag1 = i
project_tag1 = project_tag1.rstrip()
#print(project_tag1)

bug_start = bug_start.split("bug_start = ")
for i in bug_start:
	bug_start1 = i
bug_start1 = bug_start1.rstrip()
#print(bug_start1)


bug_end = bug_end.split("bug_end = ")
for i in bug_end:
	bug_end1 = i
bug_end1 = bug_end1.rstrip()
#print(bug_end1)


max_timeout_secs =  max_timeout_secs.split("max_timeout_secs = ")
for i in max_timeout_secs:
	max_timeout_secs1 = i
max_timeout_secs1 = max_timeout_secs1.rstrip()
#print(max_timeout_secs1)

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
#rng = input("enter starting number starting from:")
#rng1 = input("enter end number:")
ip = temp.index(str(bug_start1))
ip2 = temp.index(str(bug_end1))
#print(ip)
#print(ip2)
raw_input("press enter to continue \n")
#print(ip,"::",ip2)
temp = temp[int(ip2):int(ip)]
temp3 = []

print("Bugs will be downloaded in directory: ",r)

os.mkdir(r)
os.chdir(r)
for i in temp: 
	bugnumb = i
	i = "https://hibernate.atlassian.net/browse/" + bug_name + "-" + i
	download_bug(bugnumb,i)
	time_out = randint(1,int(max_timeout_secs1))
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

            
