import re
import urllib2
import os
from bs4 import BeautifulSoup as beau
import time

temp_status = []
temp_id = []
temp_pr = []
temp_summary= []
temp_os = []


############################################ OS---BEGIN ####################################################


def os(url):
	htm = urllib2.urlopen(url)
	soup  = beau(htm)         
	elm = soup.findAll("td",{"class":"vt col_9"})
	x = 0
	for i in elm:
		alink= i.findAll("a")
		for i in alink:
			#print(i.text)
			str1 = i.text
			str1 = str1.replace('\n','')
			temp_os.append(str1)
			x = x+1
			#print('total number of bugs:')
			#print(x)

############################################ OS-----END ####################################################



############################################ PRIORITY---BEGIN ####################################################

def priority(url):
	htm = urllib2.urlopen(url)
	soup  = beau(htm)         
	elm = soup.findAll("td",{"class":"vt col_1"})
	x = 0

	temp = []
	for i in elm:
		alink= i.findAll("a")
		for i in alink:
			str1 = i.text
			str1 = str1.replace('\n','')
			temp_pr.append(str1)



############################################ PRIORITY --- END ####################################################


##################################################   BUG_ID---BEGIN #################################################

def bugid(url):
	htm = urllib2.urlopen(url)
	soup  = beau(htm)         
	elm = soup.findAll("td",{"class":"vt col_8"})
	x = 0

	temp = []
	for i in elm:
		alink= i.findAll("a")
		for i in alink:
			str1 = i.text
			str1 = str1.replace('\n','')
			temp_bugid.append(str1)

##################################################   BUG_ID ----END #################################################


##################################################   SUMMARY---BEGIN #################################################
def summary(url):
	htm = urllib2.urlopen(url)
	soup  = beau(htm)         
	elm = soup.findAll("td",{"class":"vt col_8"})
	x = 0

	temp = []
	for i in elm:
		alink= i.findAll("a")
		for i in alink:
			str1 = i.text
			str1 = str1.replace('\n','')
			temp.append(str1)	
			#print(i.text)
			#x = x+1
			#print('total number of bugs:')
			#print(x)


	temp1 = []

	for i in elm:
		alink= i.findAll('a', {"class":"label"})
		for i in alink:
			str1 = i.text
			str1 = str1.replace('\n','')
			temp1.append(str1)

	temp3 = [x for x in temp if x not in temp1]
	temp_summary.extend(temp3) #append temp_summary with data in temp3
	
	# temp = temp - temp1 deleting ommon elements

	x1 = 0
	for i in temp3:	
		print i
		print('number of bugs:')
		print x1
		x1 = x1 + 1

##################################################   SUMMARY---- END #################################################
	
	

##################################################   STATUS---BEGIN #################################################

def status(url):
	htm = urllib2.urlopen(url)
	soup  = beau(htm)         
	elm = soup.findAll("td",{"class":"vt col_6"})
	x = 0
	for i in elm:
		alink= i.findAll("a")
		for i in alink:
			#print(i.text)
			str1 = str(i.text)
			str1 = str1.replace('\n','')
			temp_status.append(str1)
			x = x+1
			#print('total number of bugs:')
			#print(x)



##################################################   STATUS --- END #################################################

url = 'https://code.google.com/p/chromium/issues/list?can=1&q=memory%20crash&colspec=ID%20Pri%20M%20Week%20ReleaseBlock%20Cr%20Status%20Owner%20Summary%20OS%20Modified&num=1000&start=0'

htm = urllib2.urlopen(url)
soup  = beau(htm)         
elm = soup.findAll("div",{"class":"pagination"})
x = 0
#print(elm)


for i in elm:
	res = i.text.split("\n")
	for j in res:
		j = j.split(" ")		
		for z in j:
			if re.match(r'[0-9]+',z):			
				print z
				x = z

x = int(x)
x = x / 1000
print ("Total number of pages")
print x

start = 0

for i in range (1,x+2):
	url = 'https://code.google.com/p/chromium/issues/list?can=1&q=memory%20crash&colspec=ID%20Pri%20M%20Week%20ReleaseBlock%20Cr%20Status%20Owner%20Summary%20OS%20Modified&num=1000&start=' + str(start)
	print url
	status(url)	
	summary(url)
	os(url)
	priority(url)
	bugid(url)
	start = (i*1000) + 1
	print start 



############################# DATABASE---- BEGIN ####################################################


		



