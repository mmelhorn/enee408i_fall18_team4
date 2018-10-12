# Jetson interface for the arduino
import serial
from smbus2 import SMBus
import time

class arduinoInterface:
	
	def __init__(self):
		#COM port selection to establish connection with the ardiuno.
		self.bus = SMBus(1);
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
		self.bus.write_byte_data(42,1,vel);
	
	def setFlags(self):		#add error and emergency handling
		receive_byte = self.bus.read_byte(42);
		if receive_byte > 0:
			self.isReady = 1

			
	
	def getIsReady(self):
		self.setFlags()
		return self.isReady
		
	def getPing(self):
		self.bus.write_byte_data(42,1,200);
		leftPingDist = self.bus.read_byte(42);
		self.bus.write_byte_data(42,1,201);
		centerPingDist =self.bus.read_byte(42);
		self.bus.write_byte_data(42,1,202);
		rightPingDist = self.bus.read_byte(42);
		ping = [leftPingDist,centerPingDist,rightPingDist]
		return ping

	def done(self):
		self.move(0,0)
		self.bus.close()
