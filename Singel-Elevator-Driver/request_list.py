
from elev import Elevator
from channels import INPUT, OUTPUT
from erlendMacros import *


buttonIndex = 0
floorIndex = 1

class Request_List:
	def __init__(self, elevator):
		self.list = []
		self.elevator = elevator

	def addRequest(self):
		for floor in range(INPUT.NUM_FLOORS):
			for buttonType in range(3):
				if self.elevator.getButtonSignal(buttonType, floor) == 1:
					request = [buttonType, floor, 1]
					
					if request not in self.list:
						self.list.append(request)
						self.printRequestList()

	def removeRequest(self, floor, buttonType):
		request = [floor, buttonType]
		if request in self.list:
			self.list.remove(request)
			return 1
		else:
			return 0

	def noRequests(self):
		if not self.list:
			return 1
		else:
			return 0

	def isRequests(self):
		if not self.list:
			return 0
		else:
			return 1


	def isRequestsatFloor(self, floor):



	#renamed from isRequestAtFloor to:isRequestAtFloorAndDirection by Erlend
	def isRequestAtFloorAndDirection(self, floor):
		#please use constants instead of 0, 1, 2 here
		#oh, and i don't think this one does as intended
		if self.elevator.direction == OUTPUT.MOTOR_UP:
			buttonType = 0 
		elif self.elevator.direction == OUTPUT.MOTOR_DOWN:
			buttonType = 1
		else:
			buttonType = 2

		request = [buttonType, floor]
		if request in self.list:
			return 1
		else:
			return 0



	def requestCost(self, request):
		pass

	def printRequestList(self):
		print "\n"
		for request in self.list:
			print("Floor: {}\tbuttonType: {}\tBool: {}").format(request[1], request[0], request[2])
			#print request #requestList[index]
	
	
	#checks if there are orders beyond current point in current direction
	#for starters, this returns true no matter what kind of command is issued in the request

	def requestsAtFloor(self, floor):
		for request in self.list:
					if request[floorIndex] == floor:
						return True
					else:
						return False


	def	requestsAhead(self):

		if(self.elevator.direction == OUTPUT.MOTOR_DOWN):
			for floor in range(0, self.elevator.current_floor):
				for request in self.list:
					if request[floorIndex] == floor:
						return True
					else:
						return False

		elif(self.elevator.direction == OUTPUT.MOTOR_UP):
			for floor in range (self.elevator.current_floor, INPUT.NUM_FLOORS):
				for request in self.list:
					if request[floorIndex] == floor:
						return True
					else:
						return False
		#elevator has no direction
		else:
			print "requestsAhead called without direction"




	#might be unnecessary
	def requestsBehind(self):
		return True