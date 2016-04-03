


from elev import Elevator
from IO import io
from channels import INPUT, OUTPUT
requestList = []

class Elevator_Panel:
	def __init__(self, elevator):
		self.elevator = elevator

	def turnOffAllLights(self):
		for light in OUTPUT.LIGHTS:
			if light != -1:
				io.setBit(light, 0)
		print "lights should be turned off"

	def turnOffRequestLight(self, floor, buttonType):
		self.elevator.setButtonLamp(buttonType, floor, 1)

	def turnOffRequestLight(self, floor, buttonType):
		self.elevator.setButtonLamp(buttonType, floor, 0)
