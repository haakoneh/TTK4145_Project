#from elev import Elevator
#from channels import INPUT, OUTPU


class Elevator_Panel:

	def turnOffLights(self):
		for light in OUTPUT.LIGHTS:
			if light != -1:
				io.setBit(light, 0)

	
				
