


from elev import Elevator
from IO import io
from channels import INPUT, OUTPUT


#buttonIndex = 0
#floorIndex = 1

class Elevator_Panel:
	def __init__(self, elevator):
		self.elevator = elevator

	def turnOffAllLights(self):
		for light in OUTPUT.LIGHTS:
			if light != -1:
				io.setBit(light, 0)

	def turnOnRequestLight(self, floor, buttonType):
		self.elevator.setButtonLamp(buttonType, floor, 1)

	def turnOffRequestLight(self, floor, buttonType):
		self.elevator.setButtonLamp(buttonType, floor, 0)


	def updateLightsByRequestList(self, requestList):
		if not requestList:
			self.turnOffAllLights()
		
		for floor in range(INPUT.NUM_FLOORS):
			for buttonType in range(INPUT.NUM_FLOOR_BUTTONS):
				if OUTPUT.FLOOR_ORDER_LIGHTS[floor][buttonType] != -1:
					if [buttonType, floor] in requestList:
						self.turnOnRequestLight(floor, buttonType)
					else:
						self.turnOffRequestLight(floor, buttonType)