##tidenow version 4.0
#This program reads a data file of tide data from the ports of Jersey Website
#Used under licence from the UKHO
#
#It then calculates the current tide using a simplified sinusoidal harmonic approximation
#by finding the two tide data points either side of now and working out the current tide height

from time import sleep
import datetime as dt
import math
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


coil_A_1_pin = 7
coil_A_2_pin = 8
coil_B_1_pin = 23
coil_B_2_pin = 24
led_falling_pin = 15
led_rising_pin = 14
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(led_falling_pin,GPIO.OUT)
GPIO.setup(led_rising_pin,GPIO.OUT)

def forward(delay, steps):
	for i in range(0, steps):
		setStep(1, 0, 1, 0)
		sleep(delay)
		setStep(0, 1, 1, 0)
		sleep(delay)
		setStep(0, 1, 0, 1)
		sleep(delay)
		setStep(1, 0, 0, 1)
		sleep(delay)
 
def backwards(delay, steps):
	for i in range(0, steps):
		setStep(1, 0, 0, 1)
		sleep(delay)
		setStep(0, 1, 0, 1)
		sleep(delay)
		setStep(0, 1, 1, 0)
		sleep(delay)
		setStep(1, 0, 1, 0)
		sleep(delay)
 
def setStep(w1, w2, w3, w4):
	GPIO.output(coil_A_1_pin, w1)
	GPIO.output(coil_A_2_pin, w2)
	GPIO.output(coil_B_1_pin, w3)
	GPIO.output(coil_B_2_pin, w4)

#test the stepper and LED
forward (0.005, 20)
GPIO.output(led_rising_pin,0)
GPIO.output(led_falling_pin,1)
sleep (3)
backwards (0.005, 20)
GPIO.output(led_rising_pin,1)
GPIO.output(led_falling_pin,0)
sleep (3)
#import the tide data from the txt file

rawTideData = ""
lineCounter = 0

# open file, clean it up and save data to a variable 

with open('tides2016.txt') as fobj:
        for line in fobj:
			lineCounter +=1
			line = line.replace('\n','')
			line = line.replace(' ','')
			rawTideData=rawTideData + line

# parse all data points (date, times, heights) to one big list
# format of the list is [month, day, time, high tide, time, high tide, time, low tide, time, low tide]

parsedTideData = rawTideData.split("/") 

# extract each class of data to a separate list (there are 10 data items for each day)

tideMonth=[]
tideTimes=[]
tideHeights=[]
tideDay=[]

for n in range(0,(lineCounter-1)*10,10):
	tideMonth.extend([parsedTideData[n],parsedTideData[n],parsedTideData[n],parsedTideData[n]])
	tideDay.extend([parsedTideData[n+1],parsedTideData[n+1],parsedTideData[n+1],parsedTideData[n+1]])
	tideTimes.extend([parsedTideData[n+2],parsedTideData[n+4],parsedTideData[n+6],parsedTideData[n+8]])
	tideHeights.extend([parsedTideData[n+3],parsedTideData[n+5],parsedTideData[n+7],parsedTideData[n+9]])

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

#----------------
#Main starts here
#----------------

prevTide = 6.0

while True:

# get time now:

	currentTime = dt.datetime.now()
			
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
		GPIO.output(led_rising_pin,0)
		GPIO.output(led_falling_pin,1)
	
	else: 
		tideState='rising'
		GPIO.output(led_rising_pin,1)
		GPIO.output(led_falling_pin,0)
	

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
	
#get the stepper motor to move to indicate tidal change	

	tideChange = prevTide - currentTide
	tideChangeSteps = (abs(tideChange) / 12) * 256

	print ("Tidal Change = ", tideChange)
	print ("motor steps = " , int(tideChangeSteps))

	delay = 0.005
	
	if (tideChange > 0): 
		backwards(delay, int(tideChangeSteps))	
	else:
		forward(delay, int(tideChangeSteps))
	
	setStep(0,0,0,0)

	prevTide = currentTide
	
	sleep (600)

