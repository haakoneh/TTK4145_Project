from elev import Elevator
from IO import io
from channels import INPUT, OUTPUT

class ElevatorPanel:
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

	def updateLightsByRequestList(self, requestList, pendingRequestList):
		if not requestList and not pendingRequestList:
			self.turnOffAllLights()

		if pendingRequestList == None:
			pendingRequestList = []

		for floor in range(INPUT.NUM_FLOORS):
			for buttonType in range(INPUT.NUM_FLOOR_BUTTONS):
				if OUTPUT.FLOOR_ORDER_LIGHTS[floor][buttonType] != -1:

					if [buttonType, floor] in requestList or [buttonType, floor] in pendingRequestList:
						self.turnOnRequestLight(floor, buttonType)
					else:
						self.turnOffRequestLight(floor, buttonType)
