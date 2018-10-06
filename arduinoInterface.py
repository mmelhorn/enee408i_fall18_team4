# Jetson interface for the arduino
import serial
import time

class arduinoInterface:
	
	def __init__(self):
		#COM port selection to establish connection with the ardiuno.
		PORT = '/dev/ttyACM0' #orignally set to /dev/ttyUSB0
		baud = 9600
		self.arduino = serial.Serial(PORT, baud, timeout=0)
		#Flags and their default values
		self.isReady = 1
		self.isError = 0
		self.isEmergencyStop = 0

	# move function accepts linear and angular velocity and gives commands to arduino
	# vel_lin = {0,10}
	# vel_ang = {-4,4} positive is left
	def move(self, vel_lin, vel_ang):
		vel_lin = vel_lin * 10
		vel_ang = -vel_ang + 5
		vel = vel_lin + vel_ang
		self.isReady = 0
		self.arduino.write(str(vel))
	
	def setFlags(self):		#add error and emergency handling
		if self.arduino.in_waiting > 0:
			ardIn = ord(self.arduino.read(1))
			if ardIn == 250:
				self.isReady = 1
			elif ardIn == 255:
				self.isReady = 1
				self.isError = 1
	
	def getIsReady(self):
		self.setFlags()
		return self.isReady
		
	def getPing(self):
		self.arduino.write('200')
		leftPingDist = ord(arduino.read(1))
		self.arduino.write('201')
		centerPingDist = ord(arduino.read(1))
		self.arduino.write('202')
		rightPingDist = ord(arduino.read(1))
		ping = [leftPingDist,centerPingDist,rightPingDist]
		return ping

	#start = 1;
	#while True:
		#if arduino.in_waiting == 1 or start:
			#x= 250		
			#if start == 0:
				#x = ord(arduino.read(1))
			#if(x == 250):
				#print("success\n")
			#else:
				#print("failure\n")
				#setMove(0,0)
				#break
			#setMove(1,0)
		#start = 0


	def done(self):
		self.arduino.close()
