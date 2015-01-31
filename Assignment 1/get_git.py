import re
import urllib2
import os
from bs4 import BeautifulSoup as beau


def gitclone(url,root):
	x = url.split("https://github.com/")
	l = x[-1]        #extracting name of github lib to make directory with same name
                         # eg: https://github.com/poise/python
	t = l.split("/") #i/p poise/python --> o/p : [poise,python]
	t1 = t[0]        #t1 = poise
 	root = root.rstrip()
	t1 = root + t1   # t1 = /home/pcr/get_git/ + poise
	st = str(t1)
	print(st)        # /home/pcr/get_git/poise
	os.mkdir(st)  	#make directory /home/pcr/get_git/poise
	os.chdir(t1)     #change directory to /home/pcr/get_git/poise
	url = 'git clone ' + url #create command for git clone
                         # url = https://github.com/poise/python --> o/p : "git clone https://github.com/poise/python --> o/p --> poise/python"
	os.system(url)   # feed above command to shell to clone that lib to newely created directory
	t1 = ""


#droid function has 2 parameters url and root, this function will extract the github library from the droid html page and feed it to gitclone
def droid(url,root):
    htm = urllib2.urlopen(url) #open droid url 
    soup  = beau(htm)          #feed all the data from html page of droid to var named soup
    elm = soup.findAll('a')    #find all "a" tags

    lst = []
    for i in elm:
        x = i.attrs["href"]    #for all a tags find all attributes with hyperlink name
        lst.append(x)          #for all given href feed the value of that in a list
#    print(i.attrs["href"])

#now there are 2 hrefs in on the fdroid page both have github the one ending with issues is not the string we want
    lis = []
    for i in lst:
        if "github" in i:
            if not re.search(r"issues$",i): #if string does not have issue appent to list
                lis.append(i)
    temp = lis[-1] 
    if re.search(r"/$",temp):
        temp = temp[:-1]
        print(temp)
        gitclone(temp,root)                 #feed the url fecthed to gitclone function to perform clone
    else:
        print(temp)
        gitclone(temp,root)
#        os.system(

#function for non fdroid url to get all the git repos from github url

def github(url,root):
    htm = urllib2.urlopen(url)
    soup  = beau(htm)
    elms = soup.select("h3.repo-list-name a")

    lst = []
    for i in elms:
        x = i.attrs["href"]
#    print(i.attrs["href"])
        lst.append(x)
#    lst = lst.append(x)
#print('lst: ',lst)
    for git in lst:
        git ='https://github.com' + git + '.git'
        gitclone(git,root)
        print(git)

###################################-----------------------------#####################################
#program starts from here

url = open("config.txt",'r').readlines()
root = url[-1]
root = root.split("root_directory=")
for i in root:
	r = i

del url[-1]
temp = []
for n in url:
    x = n.split("url = ")
    temp.append(x[-1])
url = temp
temp =[]
for l in url:
    x = l.split("\n")
    temp.append(x[0])
url = temp

#os.chdir("/home/pcr/get_git/")
for l in url:
    if "droid" in l:
        droid(l,r)
         
    else:
        github(l,r)
        





    




