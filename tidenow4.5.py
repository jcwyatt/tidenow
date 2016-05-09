##tidenow version 4.0
<<<<<<< HEAD
#This program reads a data file of tide data from the ports of Jersey Website
#Used under licence from the UKHO
=======
#This program reads a data file pulls tide data from the ports of Jersey Website
#Under a licence from the UKHO
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104
#
#It then calculates the current tide using a simplified sinusoidal harmonic approximation
#by finding the two tide data points either side of now and working out the current tide height

<<<<<<< HEAD
from time import sleep
import datetime as dt
import math
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
=======
#import urllib2
#from bs4 import BeautifulSoup
from time import sleep
import datetime as dt
import math
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104

#import the tide data from the txt file

rawTideData = ""
lineCounter = 0
<<<<<<< HEAD

# open file, clean it up and save data to a variable 

=======
# open file and save data to a variable?
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104
with open('tides2016.txt') as fobj:
        for line in fobj:
			lineCounter +=1
			line = line.replace('\n','')
			line = line.replace(' ','')
<<<<<<< HEAD
=======
#			print line
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104
			rawTideData=rawTideData + line

# parse all data points (date, times, heights) to one big list
# format of the list is [month, day, time, high tide, time, high tide, time, low tide, time, low tide]

parsedTideData = rawTideData.split("/") 

<<<<<<< HEAD
# extract each class of data to a separate list (there are 10 data items for each day)
=======
#print parsedTideData

#for i in range (0,lineCounter):
#	print parsedTideData[i*10]

# extract each class of data (day, time , height) to a separate list (there are 10 data items for each day)
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104

tideMonth=[]
tideTimes=[]
tideHeights=[]
tideDay=[]
<<<<<<< HEAD
=======
#lastdayofmonth=int(parsedTideData[-10])
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104

for n in range(0,(lineCounter-1)*10,10):
	tideMonth.extend([parsedTideData[n],parsedTideData[n],parsedTideData[n],parsedTideData[n]])
	tideDay.extend([parsedTideData[n+1],parsedTideData[n+1],parsedTideData[n+1],parsedTideData[n+1]])
	tideTimes.extend([parsedTideData[n+2],parsedTideData[n+4],parsedTideData[n+6],parsedTideData[n+8]])
	tideHeights.extend([parsedTideData[n+3],parsedTideData[n+5],parsedTideData[n+7],parsedTideData[n+9]])

<<<<<<< HEAD
=======
'''
print ('list of months: ', tideMonth)
print ('list of days: ', tideDay)
print ('list of Times: ', tideTimes)
print ('list of Heights: ', tideHeights)

print ('len of months: ', len(tideMonth))
print ('len of days: ', len(tideDay))
print ('len of Times: ', len(tideTimes))
print ('len of Heights: ', len(tideHeights))
'''
print tideTimes[30]

# get time now:

currentTime = dt.datetime.now()


>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104
# create a list of all the tide times as datetime objects:

dtTideTimes=[]
tideDataList=[]

#can't remeber how this works. Want to go through all the times and convert them to dt objects
for j in range (0,(lineCounter-1)*4):
	if tideTimes[j]=='**':
		dtTideTimes.append('**')
	else:
		dtTideTimes.append(dt.datetime.now().replace(month=int(tideMonth[j]), day=int(tideDay[j]), hour=int(tideTimes[j][0:2]), minute=int(tideTimes[j][3:5])))

# make a tuple for each data point and add it to a list

	tupleHolder =(dtTideTimes[j], tideHeights[j])
	tideDataList.append(tupleHolder)

#	print tideDataList[j]
<<<<<<< HEAD

#----------------
#Main starts here
#----------------

# get time now:

currentTime = dt.datetime.now()
			
=======
		
	
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104
# find the two closest times in the list to now:

gap1 = abs(tideDataList[0][0] - currentTime)
gap2 = abs(tideDataList[0][0] - currentTime)
nearest1 = tideDataList[0]
nearest2 = tideDataList[0]

for j in range (0,(lineCounter-1)*4):

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
<<<<<<< HEAD
	GPIO.output(14,0)
	GPIO.output(15,1)
	
else: 
	tideState='rising'
	GPIO.output(14,1)
	GPIO.output(15,0)
	
=======
else: 
	tideState='rising'
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104

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

<<<<<<< HEAD
=======

>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104
# output the current tide value

currentTide = lowerTide +tideLevelCoeff*abs(tideDifference)
print 'Current Tide : ', currentTide
<<<<<<< HEAD

#
=======
>>>>>>> 1de5b3618951aef06afa8404d912eecbfa61b104
