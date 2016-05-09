from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)


for i in range (0,4):
	print("falling")
	GPIO.output(14,0)
	GPIO.output(15,1)
	sleep (5)	
	print ("rising")
	GPIO.output(14,1)
	GPIO.output(15,0)
	sleep(5)
GPIO.cleanup()
