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

while True:

	arduino.write('55')
	time.sleep(5)
	arduino.write('0')
	time.sleep(2)
	arduino.write('6')
	time.sleep(5)
	arduino.write('0')
	time.sleep(2)
	arduino.write('4')
	time.sleep(5)
	arduino.write('0')
	time.sleep(5)

