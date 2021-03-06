'''
A python program to import tide data from a portsofjersey website
tidenowx.x.py
It pulls the data in from the tide site, a month at a time
It looks for the class headers associated with date,time and height information
and then creates a list of these bits of html
'''

import urllib2
from bs4 import BeautifulSoup
from time import sleep
import datetime as dt


#open site and grab html

rawhtml = urllib2.urlopen("http://www.ports.je/Pages/tides.aspx").read(40000)
soup = BeautifulSoup(rawhtml, "html.parser")


#get the tide data (it's all in <td> tags)

rawtidedata = soup.findAll('td')


#get just the month and year (it's in the 1st h2 tag on the page)

rawmonthyear = soup.findAll('h2')[0].get_text()
print ('Month and Year: ', rawmonthyear)

#parse it all to a list

n=0
parsedtidedata=[]
for i in rawtidedata:	
	parsedtidedata.append(rawtidedata[n].get_text())
#	print (parsedtidedata[n]) #leave in for debugging for now
	n += 1


#create lists of each data type

tidetimes=[]
tideheights=[]
tideday=[]


#extract data to each list (there are 10 data items for each day)

lastdayofmonth=int(parsedtidedata[-10])

for n in range(0,lastdayofmonth*10,10):

	tideday.append(parsedtidedata[n])
	tidetimes.extend([parsedtidedata[n+1],parsedtidedata[n+3],parsedtidedata[n+5],parsedtidedata[n+7]])
	tideheights.extend([parsedtidedata[n+2],parsedtidedata[n+4],parsedtidedata[n+6],parsedtidedata[n+8]])

print('data for the nth of the month')
n=13
p=n*4
print tideday[n]
print tidetimes[p:p+4]
print tideheights[p:p+4]	

#fill a list with datetime objects for the month:
time1 = dt.datetime(tidetimes[n]
print (time1)
	

