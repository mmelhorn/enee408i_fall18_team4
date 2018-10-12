# I2C test

from smbus2 import SMBus
import time


#with SMBusWrapper(1) as bus:
	#data = 200
	#b = bus.write_byte_data(42,1,data)

	#print(bus.read_byte(42))
	
	
	#print(bus.read_byte(42))
	
	#print(bus.read_byte(42))
	
	#print(ord(b))
	
bus = SMBus(1);
data = 200
b = bus.write_byte_data(42,1,data)

print(bus.read_byte(42))
	
	
print(bus.read_byte(42))
	
print(bus.read_byte(42))
	


