#tidenow version 3.0
#This program pulls tide data from the ports of Jersey Website
#Under a licence from the UKHO
#
#It then calculates the current tide using a simplified sinusoidal harmonic approximation
#by finding the two tide data points either side of now and working out the current tide height

import urllib2
from bs4 import BeautifulSoup
from time import sleep
import datetime as dt
import math


# open site and grab html

rawhtml = urllib2.urlopen("http://www.ports.je/Pages/tides.aspx").read(40000)
soup = BeautifulSoup(rawhtml, "html.parser")


# get the tide data (it's all in <td> tags)

rawtidedata = soup.findAll('td')


# parse all data points (date, times, heights) to one big list
# format of the list is [day, time, high tide, time, high tide, time, low tide, time, low tide]

n=0
parsedtidedata=[]
for i in rawtidedata:	
	parsedtidedata.append(rawtidedata[n].get_text())
	n += 1

# extract each class of data (day, time , height) to a separate list (there are 10 data items for each day)

tidetimes=[]
tideheights=[]
tideday=[]
lastdayofmonth=int(parsedtidedata[-10])

for n in range(0,lastdayofmonth*10,10):

	tideday.append(parsedtidedata[n])
	tidetimes.extend([parsedtidedata[n+1],parsedtidedata[n+3],parsedtidedata[n+5],parsedtidedata[n+7]])
	tideheights.extend([parsedtidedata[n+2],parsedtidedata[n+4],parsedtidedata[n+6],parsedtidedata[n+8]])

# get time now:

currentTime = dt.datetime.now()


# create a list of all the tide times as datetime objects:

dtTideTimes=[]
tideDataList=[]

for j in range (0,lastdayofmonth*4):
	if tidetimes[j]=='**':
		dtTideTimes.append('**')
	else:
		dtTideTimes.append(dt.datetime.now().replace(day=int(j/4+1), hour=int(tidetimes[j][0:2]), minute=int(tidetimes[j][3:5])))

# make a tuple for each data point and add it to a list

	tupleHolder =(dtTideTimes[j], tideheights[j])
	tideDataList.append(tupleHolder)
	
	
# find the two closest times in the list to now:

gap1 = abs(tideDataList[0][0] - currentTime)
gap2 = abs(tideDataList[0][0] - currentTime)
nearest1 = tideDataList[0]
nearest2 = tideDataList[0]

for j in range (0,lastdayofmonth*4):

	if (tideDataList[j][0] !="**"):                      
		gapx = abs(tideDataList[j][0] - currentTime) 

# check if the data point is the first or second nearest to now. 
# determine the datapoints either side of now

		if (gapx <= gap1):                            
			nearest2 = nearest1
			gap2 = gap1
			nearest1 = tideDataList[j]            
			gap1 = gapx
		elif (gap1 < gapx and gapx <= gap2): 
			nearest2 = tideDataList[j]                   
			gap2 = gapx             


# get the two nearest values in order of time:

if nearest1[0] > nearest2[0]:
	nextDataPoint = nearest1
	prevDataPoint = nearest2
	gapToNext = gap1
	gapToPrev = gap2

else:
	nextDataPoint = nearest2
	prevDataPoint = nearest1
	gapToNext = gap2
	gapToPrev = gap1

gapSum = gapToNext + gapToPrev


print prevDataPoint
print nextDataPoint

# what is the tidal range and is the tide rising or falling?

tideDifference = float(nextDataPoint[1])-float(prevDataPoint[1])

if (tideDifference<0):
	tideState='falling'
else: 
	tideState='rising'

print 'Tide is currently: ',tideState

print'Tidal Range = ', tideDifference


# some maths to deduce the height of low tide, to which the current rise can be added.

lowerTide = (float(nearest1[1]) + float(nearest2[1]) - abs(tideDifference))/2


# how far through the current tidal change are we?

timeRatio = float(gapToPrev.seconds)/float(gapSum.seconds) #scaled 0 to 1


# scale the time ratio from 0 to pi

normalisedTime = (float(gapToPrev.seconds)/float(gapSum.seconds))*math.pi 


# if tide is rising, push the data point to the rising part of the cosine wave by adding pi

if tideState == 'rising':
	normalisedTime += math.pi


# approximate the tidal change to a cosine wave, with a y range of 0 to 1, instead of +1 to -1

tideLevelCoeff=(math.cos(normalisedTime)+1)/2


# output the current tide value

currentTide = lowerTide +tideLevelCoeff*abs(tideDifference)
print 'Current Tide : ', currentTide
