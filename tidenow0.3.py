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
print 'Month and Year: ', rawmonthyear


currentDataMonth = dt.datetime.strptime(rawmonthyear[6:9], "%b")
currentWorldMonth = dt.datetime.now().strftime("%b")

currentDataYear = dt.datetime.now().strftime("%Y")

print 'current data month: ', currentDataMonth
print 'current real month: ', currentWorldMonth
print currentDataYear



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

#get time now:
#time format 2015-10-14 21:53:59.037098
#yyyy-mm-dd hh:mm
currentTime = dt.datetime.now()
print currentTime
madeupTime = dt.datetime(2015, 10, 15, 22, 30)
print madeupTime

timeDiff = madeupTime - currentTime
print timeDiff

#create a list of all the tide times as dt objects:
dtTideTimes=[]

for j in range (0,lastdayofmonth*4):
	#print tidetimes[j][0:2], tidetimes[j][3:6]
	if tidetimes[j]=='**':
		dtTideTimes.append('**')
	else:
		dtTideTimes.append(dt.datetime.now().replace(day=int(j/4+1), hour=int(tidetimes[j][0:2]), minute=int(tidetimes[j][3:5])))
	print dtTideTimes[j]
	
