#THIS VERSION SEEMS TO BE MESSING UP THE TIDE HEIGHTS!!!!


import urllib2
from bs4 import BeautifulSoup
from time import sleep
import datetime as dt


#open site and grab html

rawhtml = urllib2.urlopen("http://www.ports.je/Pages/tides.aspx").read(40000)
soup = BeautifulSoup(rawhtml, "html.parser")


#get the tide data (it's all in <td> tags)

rawtidedata = soup.findAll('td')


#parse all data points (date, times, heights) to one big list
#format of the list is [day,tm,ht,tm,ht,tm,lt,tm,lt]

n=0
parsedtidedata=[]
for i in rawtidedata:	
	parsedtidedata.append(rawtidedata[n].get_text())
	n += 1

#extract each class of data (day, time , height) to a separate list (there are 10 data items for each day)

tidetimes=[]
tideheights=[]
tideday=[]
lastdayofmonth=int(parsedtidedata[-10])

for n in range(0,lastdayofmonth*10,10):

	tideday.append(parsedtidedata[n])
	tidetimes.extend([parsedtidedata[n+1],parsedtidedata[n+3],parsedtidedata[n+5],parsedtidedata[n+7]])
	tideheights.extend([parsedtidedata[n+2],parsedtidedata[n+4],parsedtidedata[n+6],parsedtidedata[n+8]])

#get time now:

currentTime = dt.datetime.now()


#create a list of all the tide times as datetime objects:

dtTideTimes=[]
tideDataList=[]

for j in range (0,lastdayofmonth*4):
	#print tidetimes[j][0:2], tidetimes[j][3:6]
	if tidetimes[j]=='**':
		dtTideTimes.append('**')
	else:
		dtTideTimes.append(dt.datetime.now().replace(day=int(j/4+1), hour=int(tidetimes[j][0:2]), minute=int(tidetimes[j][3:5])))
	tupleHolder =(dtTideTimes[j], tideheights[j])
	tideDataList.append(tupleHolder)

for j in range (0,lastdayofmonth*4):
	print tideDataList[j]

#find the two closest times in the list to now:

gap1 = abs(tideDataList[0][0] - currentTime)
nearest1 = tideDataList[0]
print gap1	

for j in range (0,lastdayofmonth*4):
	#go through all the days
	if (tideDataList[j][0] !="**"):
		gap2 = abs(tideDataList[j][0] - currentTime)
		print tideDataList[j][0], gap2, nearest1
		if (gap2 < gap1):
			nearest2 = nearest1
			nearest1 = tideDataList[j]
			gap1 = gap2

print (nearest1, nearest2)
				
#this nearly works!!! Gave the two nearest high tides, not nearest high and low.

