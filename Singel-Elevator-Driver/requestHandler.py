from elev import Elevator
from channels import INPUT, OUTPUT
from IO import io

from erlendMacros import *

requestList = []
requestDict = {}

def turnOffAllLights():
	for light in OUTPUT.LIGHTS:
		if light != -1:
			io.setBit(light, 0)
	print "lights should be turned off\n"


def refreshLights(elevator):
	for floor in range(INPUT.NUM_FLOORS):
		for buttonType in range(3):

			if ((buttonType == UP and floor == INPUT.NUM_FLOORS - 1) or (buttonType == DOWN and floor == 0)):
				pass

			else:
				if [buttonType, floor] in requestList:
					elevator.setButtonLamp(buttonType, floor, 1)
				else:
					elevator.setButtonLamp(buttonType, floor, 0)

