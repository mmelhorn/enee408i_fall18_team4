from arduinoInterface import arduinoInterface
import time
import serial

ard = arduinoInterface()

PORT = '/dev/ttyACM0'
baud = 9600
#~ ard = serial.Serial(PORT, baud)

i=0

time1 = time.time()

#for i in range(1,10):	
	#ard.move('r',1)
	#time.sleep(1)
	
ard.move('f',0)




	
	
	#~ ard.write(bytes(0))
	#~ while ard.inWaiting() == 0:
		#~ pass
	#~ print(ord(ard.read()))
	
	
#print(time.time()-time1)

#~ ard.close()

