# Jetson interface for the arduino
import serial
import time

class arduinoInterface:
	
	def __init__(self):
		#COM port selection to establish connection with the ardiuno.
		PORT = '/dev/ttyACM0' #orignally set to /dev/ttyUSB0
		baud = 9600
		self.arduino = serial.Serial(PORT, baud, timeout=0)

	# move function accepts linear and angular velocity and gives commands to arduino
	# direction = {'f', 'r', 'l'}
	# magnitude = {1-3}
	def move(self, direction, magnitude):
		if direction == 'f':
			self.arduino.write(str(magnitude))
		elif direction == 'l':
			self.arduino.write(str(magnitude+10))
		elif direction == 'r':
			self.arduino.write(str(magnitude+20))
	
	def checkForError(self):
		if self.arduino.inWaiting() > 0:
			self.arduino.reset_input_buffer();
			return 1
		return 0

	def done(self):
		self.move(0,0)
		self.arduino.close()
