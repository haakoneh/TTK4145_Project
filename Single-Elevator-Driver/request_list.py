
from elev import Elevator
from channels import INPUT, OUTPUT
from erlendMacros import *
import time

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
					request = [buttonType, floor]
					
					if request not in self.list:
						self.list.append(request)
						self.printRequestList()

	def removeRequest(self, floor, buttonType):
		request = [buttonType, floor]
		if request in self.list:
			self.list.remove(request)
			return 1
		else:
			return 0

	def removeRequestsForDirection(self, floor):
		if self.elevator.direction == OUTPUT.MOTOR_UP:
			buttonType = INPUT.BUTTON_UP
		elif self.elevator.direction == OUTPUT.MOTOR_DOWN:
			buttonType = INPUT.BUTTON_DOWN

		request    = [buttonType, floor]
		request_in = [INPUT.BUTTON_IN, floor]
		
		if request in self.list:
			self.list.remove(request)
			return 1
		elif request_in in self.list:
			self.list.remove(request_in)
			return 1
		else:
			return 0
			

	def removeRequestsAtFloor(self, floor):
		for buttonType in INPUT.BUTTON_TYPES:
			self.removeRequest(floor, buttonType)


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
		for buttonType in INPUT.BUTTON_TYPES:
			request = [buttonType, floor]
			if request in self.list:
				return 1
		return 0
		
		


	#renamed from isRequestAtFloor to:isRequestAtFloorAndDirection by Erlend
	def isRequestAtFloorAndDirection(self, floor):

		if self.elevator.direction == OUTPUT.MOTOR_UP:
			buttonType = INPUT.BUTTON_UP
		elif self.elevator.direction == OUTPUT.MOTOR_DOWN:
			buttonType = INPUT.BUTTON_DOWN
		

		request    = [buttonType, floor]
		request_in = [INPUT.BUTTON_IN, floor]
		
		if request in self.list or request_in in self.list:
			return 1
		else:
			return 0



	def requestCost(self, request):
		pass

	def printRequestList(self):
		print "\n"
		for request in self.list:
			#print("Floor: {}\tbuttonType: {}\tBool: {}").format(request[1], request[0], request[2])
			#print request #requestList[index]
			print request
	
	
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
				if self.isRequestsatFloor(floor):
					return True

			return False

		elif(self.elevator.direction == OUTPUT.MOTOR_UP):
			for floor in range (self.elevator.current_floor, INPUT.NUM_FLOORS):
				if self.isRequestsatFloor(floor):
					return True

			return False
		#elevator has no direction
		else:
			print "requestsAhead called without direction"




	#might be unnecessary
	def requestsBehind(self):
		return True