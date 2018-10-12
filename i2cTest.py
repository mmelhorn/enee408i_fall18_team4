# I2C test

from smbus2 import SMBusWrapper
import time


with SMBusWrapper(1) as bus:
	data = 5
	b = bus.write_byte_data(42,1,data)

	print(bus.read_byte(42))
	
	b = bus.write_byte_data(42,1,6)
	
	print(bus.read_byte(42))
	
	print(bus.read_byte(42))
	
	#print(ord(b))


