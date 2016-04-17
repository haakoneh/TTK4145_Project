from elev import Elevator
from channels import INPUT, OUTPUT
import os.path
import time

class Request_List:
	def __init__(self, elevator, fileName):
		self.list = []
		self.elevator = elevator
		self.file = fileName
		self.globalList = []
		self.readRequestFile()

	def addRequest(self):
		"""Adds request if it does not alredy exist in list"""
		for floor in range(INPUT.NUM_FLOORS):
			for buttonType in range(3):
				if self.elevator.getButtonSignal(buttonType, floor) == 1:
					request = [buttonType, floor]
					if buttonType != INPUT.BUTTON_IN:
						if request not in self.globalList:
							print "adding global request in addRequest"
							self.globalList.append(request)

					elif request not in self.list:
						self.list.append(request)
						self.printRequestList()

		self.updateRequestFile()
	
	def addGlobalRequest(self, request):
		if not request in self.list:
			self.list.append(request)
			self.updateRequestFile()

	def getGlobalRequest(self):
		if not self.globalList:
			return []
		return self.globalList.pop()

	def readRequestFile(self):
		"""Reads from file during initialization, only copies orders from inside elevator"""
		#new stuff##############################
		if os.path.isfile(self.file):
		#########################################
			with open(self.file, 'r') as f:
				string_list = [line.rstrip('\n') for line in f]
			

			for string in string_list:
				request = map(int, string[1:-1].split(','))
				if request[0] == INPUT.BUTTON_IN:
					self.list.append(request)
		else:
			print "No file: {}".format(self.file)

	def updateRequestFile(self):
		"""Updates file whenever the request list is changed"""
		with open(self.file, 'w') as f:
			if self.list != None:
			    for s in self.list:
			        f.write(str(s) + '\n')


	def removeRequestByRequest(self, request):
		""""""	
		if request in self.list:
			self.list.remove(request)
			self.updateRequestFile()
			return 1
		else:
			return 0

	def removeRequest(self, buttonType, floor):
		""""""
		return self.removeRequestByRequest([buttonType, floor])

	def removeRequestsAtFloor(self, floor):
		requests = []
		for buttonType in INPUT.BUTTON_TYPES:
			requests.append([buttonType,floor])
			self.removeRequest(buttonType, floor)
			print '\033[92m' + "removing request: ".format([buttonType,floor]) + '\033[0m'

		return requests

	def removeRequestsForDirection(self, floor):
		if self.elevator.direction == OUTPUT.MOTOR_UP:
			buttonType = INPUT.BUTTON_UP
		elif self.elevator.direction == OUTPUT.MOTOR_DOWN:
			buttonType = INPUT.BUTTON_DOWN

		request    = [buttonType, floor]
		request_in = [INPUT.BUTTON_IN, floor]
		
		if request in self.list:
			self.list.remove(request)
			self.updateRequestFile()
			return 1

		elif request_in in self.list:
			self.list.remove(request_in)
			self.updateRequestFile()
			return 1

		else: return 0	

	def removeAndReturnRequestsForDirection(self, floor):

		hallRequests = []

		print '\033[94m' + "Before furthest request away Check. Removing all requests" + '\033[0m'

		if(self.furthestRequestThisWay() == self.elevator.getCurrentFloor()):
			print '\033[94m' + "Print furthest request away. Removing all requests" + '\033[0m'
			return self.removeRequestsAtFloor(floor)

		if floor == 0 :
			buttonType = INPUT.BUTTON_UP
		elif floor == INPUT.NUM_FLOORS -1:
			buttonType = INPUT.BUTTON_DOWN
		elif self.elevator.direction == OUTPUT.MOTOR_UP:
			buttonType = INPUT.BUTTON_UP
		elif self.elevator.direction == OUTPUT.MOTOR_DOWN:
			buttonType = INPUT.BUTTON_DOWN

		request    = [buttonType, floor]
		request_in = [INPUT.BUTTON_IN, floor]
		
		if request in self.list:
			hallRequests.append(request)
			self.list.remove(request)
			self.updateRequestFile()
			return hallRequests

		elif request_in in self.list:
			self.list.remove(request_in)
			self.updateRequestFile()
			return []

		else: return []	

	def getGlobalFromLocal(self):
		globalInLocal = []
		for request in self.list:
			if request[0] != INPUT.BUTTON_IN:
				globalInLocal.append(request[0])
				globalInLocal.append(request[1])
		return globalInLocal

	def isRequests(self):
		if self.list:	return 1
		else:			return 0

	def isRequestsatFloor(self, floor):
		for buttonType in INPUT.BUTTON_TYPES:
			request = [buttonType, floor]
			if request in self.list:
				return 1
		return 0

	def isRequestAtFloorAndDirection(self, floor):
		if self.elevator.direction == OUTPUT.MOTOR_UP:
			buttonType = INPUT.BUTTON_UP
		elif self.elevator.direction == OUTPUT.MOTOR_DOWN:
			buttonType = INPUT.BUTTON_DOWN
		else:
			buttonType = INPUT.BUTTON_IN
	
		request    = [buttonType, 		floor]
		request_in = [INPUT.BUTTON_IN, 	floor]
		
		if request in self.list or request_in in self.list:
			return 1
		else:			
			return 0

	def printRequestList(self):
		print 'Printing reqList'
		for request in self.list:
			print request
	
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
					return 1
			return 0

		elif(self.elevator.direction == OUTPUT.MOTOR_UP):
			for floor in range (self.elevator.current_floor, INPUT.NUM_FLOORS):
				if self.isRequestsatFloor(floor):
					return 1
			return 0
		elif(self.elevator.direction == OUTPUT.MOTOR_STOP):
			# for floor in range (self.elevator.current_floor, INPUT.NUM_FLOORS):
			# 	if self.isRequestsatFloor(floor):
			# 		return 1
			# return 0
			if self.list:
				return 1
			else:
				return 0


		else:
			print "requestsAhead called without direction"
	
	def furthestRequestAway(self):
		if not self.list:
			return self.elevator.getCurrentFloor()

		if self.elevator.direction == OUTPUT.MOTOR_UP :
			furthestAway = INPUT.NUM_FLOORS + 1
			for request in self.list:
				if request[1] < furthestAway:
					furthestAway = request[1]

		elif self.elevator.direction == OUTPUT.MOTOR_DOWN :
			furthestAway = -1
			for request in self.list:
				if request[1] > furthestAway:
					furthestAway = request[1]
		return furthestAway

	def furthestRequestThisWay(self):
		if not self.list:
			return self.elevator.getCurrentFloor()
		furthestAway = -1

		if self.elevator.direction == OUTPUT.MOTOR_UP :
			for request in self.list:
				if request[1] > furthestAway:
					furthestAway = request[1]

		elif self.elevator.direction == OUTPUT.MOTOR_DOWN :
			furthestAway = INPUT.NUM_FLOORS + 1
			for request in self.list:
				if request[1] < furthestAway:
					furthestAway = request[1]
		else:
			for request in self.list:
				furthestAway = max(abs(request[1] - self.elevator.getCurrentFloor()), furthestAway)
		print "Furthestaway: ", furthestAway
		return furthestAway


	def furthestRequestThisWayasdasd(self):
		if not self.list:
			return self.elevator.getCurrentFloor()

		if self.elevator.direction == OUTPUT.MOTOR_UP :
			furthestAway = -1
			for request in self.list:
				if request[1] > furthestAway:
					furthestAway = request[1]

		elif self.elevator.direction == OUTPUT.MOTOR_DOWN :
			furthestAway = INPUT.NUM_FLOORS + 1
			for request in self.list:
				if request[1] < furthestAway:
					furthestAway = request[1]
		return furthestAway


	def addListToRequestList(self, newList):
		for item in newList:
			if item not in self.list:
				self.list.append(item)
		self.updateRequestFile()