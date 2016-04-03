from IO import io
from channels import INPUT, OUTPUT
from time import sleep
#from elev_panel import Elevator_Panel

#move these to channels
from erlendMacros import *


class Elevator:
	def __init__(self):
		self.moving = False
		self.direction = OUTPUT.MOTOR_DOWN
		self.NUM_FLOORS = INPUT.NUM_FLOORS
		self.current_floor = -1
		self.previous_floor = -1

		for light in OUTPUT.LIGHTS:
			if light != -1:
				io.setBit(light, 0)

		print "Elev setup"


	def setSpeed(self, speed):
		if speed > 0:
			self.direction = OUTPUT.MOTOR_UP
		elif speed < 0:
			self.direction = OUTPUT.MOTOR_DOWN
		else:
			self.stop()

		io.setBit(OUTPUT.MOTORDIR, self.direction)
		io.writeAnalog(OUTPUT.MOTOR, 2048+4*abs(speed))
		self.moving = True

	def stop(self):
		if not self.moving:
			return
		if self.direction is OUTPUT.MOTOR_DOWN:
			io.setBit(OUTPUT.MOTORDIR, OUTPUT.MOTOR_UP)
		else:
			io.setBit(OUTPUT.MOTORDIR, OUTPUT.MOTOR_DOWN)
		self.moving = False
		sleep(0.02)
		io.writeAnalog(OUTPUT.MOTOR, 2048)

	def setButtonLamp(self, buttonType, floor, value):
		assert(floor >= 0), "ERR_ floor < 0"
		assert(floor < self.NUM_FLOORS), "ERR_ floor > NUM_FLOORS"
		assert(buttonType >= 0), "ERR_ buttonType < 0"
		assert(buttonType < self.NUM_FLOORS - 1), "ERR_ buttonType > NUM_FLOORS"

		#catch hightest level up and lowest level down

		if (OUTPUT.FLOOR_ORDER_LIGHTS[floor][buttonType] == -1):
			print "Button light does not exist"
		else:
			io.setBit(OUTPUT.FLOOR_ORDER_LIGHTS[floor][buttonType], value)
		#try:
		#	io.setBit(OUTPUT.FLOOR_ORDER_LIGHTS[floor][buttonType], value)
		#except ((buttonType == UP and floor == NUM_FLOORS - 1) or (buttonType == DOWN and floor == 0)):
		#	raise NonexistentButton("NonexistentButton")

	def setMotorDirection(self, dir):
		assert(dir in MOTOR_DIRECTION), "ERR: Invalid motor direction!"
		io.writeAnalog(MOTOR, dir)

	def setFloorIndicator(self, floor):
		assert(floor >= 0), "ERR_ floor < 0"
		assert(floor < self.NUM_FLOORS), "ERR_ floor > NUM_FLOORS"

		if floor & 0x02:
			io.setBit(OUTPUT.FLOOR_IND1, 1)
		else:
			io.setBit(OUTPUT.FLOOR_IND1, 0)

		if floor & 0x01:
			io.setBit(OUTPUT.FLOOR_IND2, 1)
		else:
			io.setBit(OUTPUT.FLOOR_IND2, 0)


	def getButtonSignal(self, button, floor):
		assert(floor >= 0)
		assert(floor < self.NUM_FLOORS)
		
		if INPUT.BUTTON_FLOORS[floor][button] == -1:
			return -1

		if(io.readBit(INPUT.BUTTON_FLOORS[floor][button])):
			return 1
		
		else:
			return 0

			
	def getFloorSensorSignal(self):
		for index, sensor in enumerate(INPUT.SENSORS):
			if io.readBit(sensor):
				self.current_floor = index
				return self.current_floor

		return -1
 
	def setDoorLamp(self, value):
		assert(value >= 0), "ERR: door lamp value < 0"
		assert(value < 1), "ERR: door lamp value > 1"
		io.setBit(OUTPUT.DOOROPEN, value)

	def getStopSignal(self):
		return io.readBit(INPUT.STOP)

	def getObstructionSignal():
		return io.readBit(INPUT.OBSTRUCTION)


	def checkFloorButtons(self):
		for floor in range(self.NUM_FLOORS):
			for buttonType in range(3):
				if self.getButtonSignal(buttonType, floor) == 1:
					#print "buttonType: {}\t floor: {}\t bool: {}".format(buttonType, floor, self.getButtonSignal(buttonType,floor))
					self.setButtonLamp(floor, buttonType, 1)
