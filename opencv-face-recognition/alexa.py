# USAGE
# python alexa.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import struct 
import sys
import serial
import time
from arduinoInterface import arduinoInterface
from collections import deque
# last 3 imports added
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import logging
from random import randint
# flask imports added

app = Flask(__name__)
ask = Ask(app,"/")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# construct the argument parser and parse the arguments, first two args added
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


#global variables will go here
global name1 
global proba 
#global camera


@ask.launch
def welcomemsg():
	welcome_msg = render_template('welcome')
	return question(welcome_msg)

@ask.intent("IdentifyIntent")
def facial_recog():

	#arg parsing

	# load our serialized face detector from disk
	print("[INFO] loading face detector...")
	protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
	modelPath = os.path.sep.join([args["detector"],
		"res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open(args["recognizer"], "rb").read())
	le = pickle.loads(open(args["le"], "rb").read())

	# if a video path was not supplied, grab the reference
	# to the webcam, this entire block added
	if not args.get("video", False):
	   video = cv2.VideoCapture(1)
	# Read video
	else:
	   video = cv2.VideoCapture(args["video"])

	while True:
		global name1
		name1 = " "
		global proba
		proba = 0
	
		# grab the frame from the threaded video stream
		_,frame = video.read() #edit made here

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections
			if confidence > args["confidence"]:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

				# perform classification to recognize the face
				preds = recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				name1 = le.classes_[j]

				# draw the bounding box of the face along with the
				# associated probability
				text = "{}: {:.2f}%".format(name1, proba * 100)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(frame, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)


		#show output frame	
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		if proba > 0.5 and name1 is not "unknown":
			return question("You are " + name1)

		if key == ord("q"):
			break

	#cv2.destroyAllWindows()
	#vs.stop()


@ask.intent("FollowIntent")
def follow():

	cv2.destroyAllWindows()
	#vs.stop()	
	arduino = arduinoInterface()

	#global camera

	#global vars for movement control
	time_present = time.time()
	time_past = 0
	run_code = 0

	time_start = time.time()

	#time.sleep(5)

	#ap2 = argparse.ArgumentParser()
	#ap2.add_argument("-v", "--video",
	#help="path to the (optional) video file")
	#ap2.add_argument("-b", "--buffer", type=int, default=32,
	#help="max buffer size")
	#args = vars(ap2.parse_args())

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
	
			#Decide whether or not to move
			time_present = time.time();
			time_response_margin = 1
			if(time_present - time_past > time_response_margin):
				run_code = 1
				time_past = time_present
			else:
				run_code = 0

			min_radius = 30
			max_radius = 100
			left_border = 150
			right_border = 450
	
			#Run move code
			if run_code==1:
				if rad >= max_radius:
					arduino.move('f',0)
					print("stop")

				if xAxis >= left_border and xAxis <= right_border and rad < max_radius and rad > min_radius:
					arduino.move('f',1)
					print("forward")

				if xAxis <= left_border and rad < max_radius and rad > min_radius:
					arduino.move('l',1)
					print("turn left")

				if xAxis >= right_border and rad < max_radius and rad > min_radius:
					arduino.move('r',1)
					print("turn right")
				if rad < min_radius:
					arduino.move('f',0)
					print("out of range")

			if (prevMovement != movement):
				print(movement)
				#arduino.write(movement.encode())
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
			
			#time.sleep(7)

			if time.time() - time_start > 7:
				arduino.move('f',0)
				return question("should I continue to follow")
	

	#Stop motors and close serial port
	#arduino.done()

	camera.release()
	cv2.destroyAllWindows()




@ask.intent("MemoryGameIntent")

#def startUp():
	#Stop motors and close serial port
	#arduino.done()

	#camera.release()
	#cv2.destroyAllWindows()

def nextRound():
	numbers = [randint(0, 9) for _ in range(3)]
	round_msg = render_template('round', numbers = numbers)
	session.attributes['numbers'] = numbers[::-1]
	return question(round_msg)

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):
	winning_numbers = session.attributes['numbers']
	if [first, second, third] == winning_numbers:
		msg = render_template('win')
	else:
		msg = render_template('lose')
	return question(msg + " what's next") #don't want to be a statement like in example so we can continue

@ask.intent("StopIntent")

def stop():
	ard = arduinoInterface()
	ard.move('f',0)
	#camera.release()
	cv2.destroyAllWindows()
	return question("should I do something else")

@ask.intent("EndIntent")

def end():
	return statement("goodbye")

@ask.intent("WheelyIntent")

def wheely():
	ard = arduinoInterface()
	ard.move('f',3)
	#time.sleep(.5)
	#ard.move('f',0)
	#camera.release()
	cv2.destroyAllWindows()
	return question("initiating wheely pop")

#new intents
	

app.run()
