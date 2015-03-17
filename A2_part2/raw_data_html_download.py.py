import re
import urllib2
import os
from bs4 import BeautifulSoup as beau
import time
import os
import requests
from requests.exceptions import HTTPError
from socket import timeout


temp_status = []
temp_id = []
temp_pr = []
temp_summary= []
temp_os = []
notdown =[]

global len1

#url = 'https://code.google.com/p/chromium/issues/list?can=1&q=100%25%20CPU&colspec=ID%20Pri%20M%20Week%20ReleaseBlock%20Cr%20Status%20Owner%20Summary%20OS%20Modified&num=1000&start=2000'

#url = 'https://code.google.com/p/chromium/issues/list?can=1&q=page%20rendering&colspec=ID%20Pri%20M%20Week%20ReleaseBlock%20Cr%20Status%20Owner%20Summary%20OS%20Modified&num=1000&start=6000'

url = 'https://code.google.com/p/chromium/issues/list?can=1&q=memory%20crash&colspec=ID%20Pri%20M%20Week%20ReleaseBlock%20Cr%20Status%20Owner%20Summary%20OS%20Modified&num=1000&start=1000'

############################################ OS---BEGIN ####################################################

temp_bugid = []
temp = [] 
temp4 = []

#----------------------------------------------XXXX-------------------------------------------------------------------------
# Function to prepare list of all bugs on a page
#----------------------------------------------XXXX-------------------------------------------------------------------------

# Find all bug ids and put it in a list 
def bugid(url):
	htm = urllib2.urlopen(url)
	soup  = beau(htm)         
	elm = soup.findAll("td",{"class":"vt id col_0"})
	x = 0

	temp = []
	for i in elm:
		alink= i.findAll("a")
		for i in alink:
			str1 = i.text
			str1 = str1.replace('\n','')
			str1 = str1.replace(' ','')
			temp_bugid.append(str1)
			
	temp  = temp_bugid[0:496]
	temp3 = [x for x in temp_bugid if x not in temp]
	temp4.extend(temp3)

#----------------------------------------------XXXX-------------------------------------------------------------------------

#----------------------------------------------XXXX-------------------------------------------------------------------------

#l1 = [u'121183', u'120945']

#[u'53017']


l = []

#----------------------------------------------XXXX-------------------------------------------------------------------------
# Automated function to download bugs
#----------------------------------------------XXXX-------------------------------------------------------------------------
def download_bug(len1,temp_bugid):
		while(len1 != 0): 
			l1 = temp_bugid #use temp list l1 
			print "start of while loop" 
			temp_bugid = []	#flush global list
			for i in l1:
				bugnumber = i + '.html'	
				url = 'https://code.google.com/p/chromium/issues/detail?id='+i 
				try:
					page = urllib2.urlopen(url)
					#htm = urllib2.urlopen(url)
					soup  = beau(page)
					#bugnumber = bugno + '.html'
					print bugnumber
					s = open(bugnumber,'w')
					s.write(str(soup))
					#time.sleep(3)
				except:  #except with no arguments will catch the exception and pass it and move onto next iteration 
					print "bugnumber = %s" % (bugnumber)
					temp_bugid.append(i) #append empty list with all bugs that were not downloaded for which 
					# there was error in try and exception was raised then iterate while on left length until its is 0
			#one can catch Httpsresponse exception as Urllib2.HTTpsreponse
			print temp_bugid
			len1 = len(temp_bugid)
			print "length of temp_bugid = %s" % len1	
			#finally:
			#	l.append(i)
				#	raise Exception("There was an error: %r %d" % e,bugnumber)
			#except timeout:
			#	logging.error('socket timed out - URL %s', url)

#----------------------------------------------XXXX-------------------------------------------------------------------------

#----------------------------------------------XXXX-------------------------------------------------------------------------
bugid(url)
len1 = len(temp_bugid)
#print temp_bugid
print "lenght of bug id =%d" % len1

r = '/home/dhruv/Documents/bugs/bugs1000' #used different directories as it is a generalised script
os.chdir(r)
download_bug(len1,temp_bugid)
'''
print l
fo = open("bugs.txt", "rw+")
for i in l:
	fo.write("%s\n" % i)

fo.close()
'''


