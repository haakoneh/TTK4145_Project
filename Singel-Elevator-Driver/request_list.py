
from elev import Elevator
from channels import INPUT, OUTPUT
from erlendMacros import *

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
		else
			return 0

	def isRequestAtFloor(self, floor):
		if self.elevator.direction == OUTPUT.MOTOR_UP:
			buttonType = 0 
		else if self.elevator.direction == OUTPUT.MOTOR_DOWN:
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
	
	