from arduinoInterface import arduinoInterface
import time
import serial

ard = arduinoInterface()

PORT = '/dev/ttyACM0'
baud = 9600
#~ ard = serial.Serial(PORT, baud)

i=0

time1 = time.time()
while i < 10:
	
	ard.move(0,0)
	ard.setFlags()
	while  ard.isReady == 0:
		ard.setFlags()
		pass
	
	#~ ard.write(bytes(0))
	#~ while ard.inWaiting() == 0:
		#~ pass
	#~ print(ord(ard.read()))
	
	i = i + 1
	
print(time.time()-time1)

#~ ard.close()

