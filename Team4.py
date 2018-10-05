#Import packages here.
from collections import deque
from Adafruit_IO import Client
import numpy as np
import argparse
import imutils
import cv2
import serial
import time
from arduinoInterface import setMove

#COM port selection to establish connection with the ardiuno.
PORT = '/dev/ttyACM0' #orignally set to /dev/ttyUSB0
baud = 9600

arduino = serial.Serial(PORT, baud, timeout=0) 

time.sleep(5)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

#Establish lower and upper boundaries for green (tennis ball) in the HSV color space.
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

#Initialize list of tracked points, frame counters, and coordinate deltas.
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY, dZ) = (0, 0, 0)
direction = ""

#Establish connection with the default camera, if video camera is connected,
#then that becomes the default video capturing device.
if not args.get("video", False):
	camera = cv2.VideoCapture(1)

prevMovement = ' '
while True: # infinite loop
	
	if (True):
		#Current frame.
		(grabbed, frame) = camera.read()

		#Resize the frame, blur it, and convert it to the HSV color space.
		frame = imutils.resize(frame, width=600)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		#Construct a mask for "green", then perform
		#a series of dilations and erosions to remove any small blobs left in the mask.
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		#Find contours in the mask and initialize the current (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None

		#initialize variables
		radius = 0
		x = 0
		y = 0
		xPrev = 0 # used for determining if ball left view left or right

		#Proceed only if at least one contour was found
		if len(cnts) > 0:
			flag = 0
			#Find the largest contour in the mask, then use
			#it to compute the minimum enclosing circle and centroid.
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			xPrev = x

			#Proceed only if the radius meets a minimum size.
			if radius > 10:
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				pts.appendleft(center)
		else:
			radius = 0
			x = 0
			y = 0
			flag = 1

		#######################################################

		
		#calculate the int radius, int x, int y
		rad = int(round(radius))
		xAxis = int(round(x))
		yAxis = int(round(y))
		xPrev = int(round(xPrev))


		#Communcation with arduino. 
		movement = ' '
		#if flag == 0:
		start = 1;
		if rad >= 50:
#			arduino.write(setMove(0,0))
	#		while arduino.in_waiting == 0:
#				pass
#			x = arduino.read(1)
#			if(ord(x) == 250):
#				print("success\n")
#			else:
#				print("failure\n")
#				arduino.write(setMove(0,0))
#				break
			print("stop")
	
		if xAxis >= 250 and xAxis <= 350 and rad < 50:
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
			print("forward")

		if xAxis <= 250 and rad < 50:
#			arduino.write(setMove(0,2))
#			while arduino.in_waiting == 0:
#				pass
#			x = arduino.read(1)
#			if(ord(x) == 250):
#				print("success\n")
#			else:
#				print("failure\n")
#				arduino.write(setMove(0,0))
#				break
			print("turn left")

		if xAxis >= 350 and rad < 50:
#			arduino.write(setMove(0,-2))
#			while arduino.in_waiting == 0:
#				pass
#			x = arduino.read(1)
#			if(ord(x) == 250):
#				print("success\n")
#			else:
#				print("failure\n")
#				arduino.write(setMove(0,0))
#				break
			print("turn right")

		#if flag == 1:
			#if xPrev <= 10: #exited left - x is < 10
				#movement = 'f'
				#print("find left")
			#if xPrev >=580: #exited right - x is > 580
				#movement = 'i'
				#print("find right")



		#Write to arduino
		#print("Movement:" + movement)
		#time.sleep(0.1)

		if (prevMovement != movement):
			print(movement)
			arduino.write(movement.encode())
			prevMovement = movement


		#Place direction info on screen
		cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (0, 0, 255), 3)
		cv2.putText(frame, "x: {}, y: {}, rad: {}, xPrev: {}".format(xAxis, yAxis, rad, xPrev),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
			0.35, (0, 0, 255), 1)

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		counter += 1

		#Break loop if "q" is pressed.
		if cv2.waitKey(1) == ord('q'):
			break
		#time.sleep(0.5)

camera.release()
cv2.destroyAllWindows()