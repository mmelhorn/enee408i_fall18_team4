#Import
import numpy as np
import argparse
import imutils
import cv2
import serial, time

################################################
import socket
import sys
import time
# server info
SERVER_IP = "10.104.113.61"
SERVER_PORT = 5001

# commands
STOP = "STOP"
FOUND = "FOUND"

# message format
DELIM = ","
MSG_END = "!"
MSG_TEMP = "%s" + DELIM + "%s" + MSG_END

# misc.
TEAM_NO = 2 #5
BUF_SIZE = 1024
sock = None
###############################################

FIRST_FOUND = 0
FOLLOWING = 0


#COM port selection to establish connection with the ardiuno.
PORT = 'COM4'
baud = 19200
#arduino = serial.Serial(PORT, baud, timeout=0) 

time.sleep(3)

#Establish lower and upper boundaries for green (tennis ball) in the HSV color space.
greenLower = (29, 96, 46)
greenUpper = (64, 255, 255)

#Initialize list of tracked points, frame counters, and coordinate deltas.
counter = 0
(dX, dY, dZ) = (0, 0, 0)
direction = ""

#Establish connection with the default camera, if video camera is connected,
#then that becomes the default video capturing device.
#if not args.get("video", False):
camera = cv2.VideoCapture(1)

####################################################################
# return 0 on success, -1 on failure
def handshake(team_no, target_ip=SERVER_IP):
	global TEAM_NO
	global sock
	if sock == None:
		sock = socket.socket()
		TEAM_NO = str(team_no)
		sock.settimeout(5)
		try:
			sock.connect((target_ip,SERVER_PORT))
			sock.send(str(TEAM_NO).encode("UTF-8"))
			data = sock.recv(BUF_SIZE)
			if data != TEAM_NO.encode("UTF-8"):
				print("Error in handshake")
				sock = None
				return -1
		except socket.timeout:
			print("Could not connect to server at %s:%d" % (target_ip, PORT))
			sock = None
			return -1
		print("Handshake success")
		sock.setblocking(0) # non-blocking	
		return 0
	else:
		print("Socket already connected")
		return 0

# returns a list of tuples ie [(team number, command), (team number, command)]
# or None if no data on socket or error in parsing
def recv():
	try:
		data = sock.recv(BUF_SIZE)
		if (data == None):
			return None
		data = data.decode("utf-8")
		#data = str(data)
		#print(data)
		msgs = data.strip(MSG_END).split(MSG_END) 	# split messages
		ret_msgs = list()
		for msg in msgs:
			s = msg.split(DELIM) 
			if len(s) != 2:
				print("Malformed packet")
				return None						# split team num and command
			ret_msgs.append((s[0],s[1])) 			# packed into tuples
		return ret_msgs
	except socket.error:
		print("No data found")
		return None
	#except Error:
	#	print("Malformed packet")
	#	return None

# call to broadcast STOP command
def send_stop():
	string = str(TEAM_NO) + ',STOP!'
	string = string.encode('UTF-8')
	sock.send(string)

# call to broadcast FOUND command
def send_found():
	sock.send(MSG_TEMP % (TEAM_NO, FOUND))

# call on exit
def close():
	sock.close()
###################################################

handshake(TEAM_NO, SERVER_IP)

while True: # infinite loop
	
	#Current frame.
	(grabbed, frame) = camera.read()

	#Resize the frame, blur it, and convert it to the HSV color space.
	frame = imutils.resize(frame, width=600)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#Construct a mask for "green", then perform
	#a series of dilations and erosions to remove any small blobs left in the mask.
	kernel = np.ones((5,5))
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, kernel)#, iterations=1)
	mask = cv2.dilate(mask, kernel)#, iterations=1)

	#Find contours in the mask and initialize the current (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	#Proceed only if at least one contour was found
	if len(cnts) > 0:
		
		FIRST_FOUND = FIRST_FOUND + 1;
		
		if ((FIRST_FOUND == 1) and (FOLLOWING == 0)):
			send_stop();
			FOLLOWING = 1;

		flag = 0
		#Find the largest contour in the mask, then use
		#it to compute the minimum enclosing circle and centroid.
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) #(x,y)

	else:
		FOLLOWING = 0;
		#FIRST_FOUND = 0;
		radius = 0
		x = 0
		y = 0
		flag = 1

	#######################################################

	#calculate the int radius, int x, int y
	rad = int(round(radius))
	xAxis = int(round(x))
	yAxis = int(round(y))
	
	# Communication with server
	data = recv()
	if (data is not None):
		flag = 2
		print("RECEIVED STOP")

	#Communcation with arduino. Stop = 0, Straight = 1, left = 2, right = 3
	movement = ' '
	if flag == 0:
		if rad >= 40:
			movement = 's'
			print("stop")
			
		if xAxis >= 250 and xAxis <= 350 and rad < 50:
			movement = 'm'
			print("forward")
			
		if xAxis <= 250 and rad < 50:
			movement = 'l'
			print("turn left")
			
		if xAxis >= 350 and rad < 50:
			movement = 'r'
			print("turn right")

	if flag == 1:
		movement = 'f'
		print("find")

	if flag == 2:
		movement = 's'
		#arduino.flushOutput()
		#arduino.flushInput()
		
		#arduino.write(movement.encode())
		#data = arduino.readline()
		print("STOPPING FOR 5 SECONDS")
		time.sleep(5)
	
	#Write to arduino
	#print(movement)
	#arduino.flushOutput()
	#arduino.flushInput()
	
	#arduino.write(movement.encode())
	#data = arduino.readline()
	#if data:
		#print(data)
		#print("\n\nfinished")
	
	#Place direction info on screen
	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(frame, "x: {}, y: {}, rad: {}".format(xAxis, yAxis, rad),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	#Place contor that is being followed

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	#Break loop if "q" is pressed.
	if cv2.waitKey(1) == ord('q'):
		break

	#serial.flush()


camera.release()
cv2.destroyAllWindows()
