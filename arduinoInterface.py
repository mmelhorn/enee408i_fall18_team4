# Jetson interface for the arduino

from collections import deque
from Adafruit_IO import Client
import numpy as np
import argparse
import imutils
import cv2
import serial
import time


#COM port selection to establish connection with the ardiuno.
PORT = '/dev/ttyACM0' #orignally set to /dev/ttyUSB0
baud = 9600

arduino = serial.Serial(PORT, baud, timeout=0) 

time.sleep(5)

# move function accepts linear and angular velocity and gives commands to arduino
# vel_lin = {0,10}
# vel_ang = {-4,4} positive is left


def setMove(vel_lin, vel_ang):
	vel_lin = vel_lin * 10
	vel_ang = -vel_ang + 5
	vel = vel_lin + vel_ang
	return str(vel)

#def getPing():
#	arduino.write('200')
#	leftPingDist = ord(arduino.read(1))
#	arduino.write('201')
#	centerPingDist = ord(arduino.read(1))
#	arduino.write('202')
#	rightPingDist = ord(arduino.read(1))
#	ping = [leftPingDist,centerPingDist,rightPingDist]
#	return ping

start = 1;
while True:
	if arduino.in_waiting == 1 or start:
		x= 250		
		if start == 0:
			x = ord(arduino.read(1))
		if(x == 250):
			print("success\n")
		else:
			print("failure\n")
			arduino.write(setMove(0,0))
			break
		arduino.write(setMove(1,0))
	start = 0

		
		
		



#while True:	
#mv = setMove(1,0)
#arduino.write(mv)
#time.sleep(3)
#mv = setMove(0, 0)
#arduino.write(mv)




#print(getPing())
#print(getPing())

arduino.close()
