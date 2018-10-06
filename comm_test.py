from arduinoInterface import arduinoInterface
import time

ard = arduinoInterface()
i=0
while True:
	lin = int(input("lin: "))
	ang = int(input("ang: "))
	ard.move(lin,ang)
	while  ard.getIsReady() == 0:
		i = i + 1
	print(ard.getIsReady())
	print(i)
	i=0


