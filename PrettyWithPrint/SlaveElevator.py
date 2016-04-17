from elev import Elevator
from RequestList import RequestList 
from channels import INPUT, OUTPUT
import ElevatorPanel 
from Timer import *
import time
import SlaveNetwork
from GlobalFunctions import *
from MessageFormatHandler import *
from colors import *

class SlaveElevator:
	def __init__(self, masterIP, port):
		self.printString = ""
		self.printStringPrev = ""

		self.slave = SlaveNetwork.SlaveNetwork(masterIP, port)
		self.elevIP = getMyIP()
		self.elev = Elevator()
		self.elevPanel = ElevatorPanel.ElevatorPanel(self.elev)
		self.elevPanel.turnOffAllLights()

		self.requestList = RequestList(self.elev, 'requestListFile.txt')
		self.globalRequestList = RequestList(self.elev, 'globalRequestListFile.txt')
		self.pendingRequests = RequestList(self.elev, 'pendingRequests.txt')

		self.requestList.addListToRequestList(self.pendingRequests.list)

		self.floorStopTimer = TimerElev()
		self.msgEncoder = MessageEncoder()
		self.msgParser = MessageParser()
		self.msgBuffer = []
		self.prevState = [-1, -1, -1]
		self.prevFloor = -1

		self.runElevator()

	def sendState(self):
		
		state = [-1 , -1, -1]
		state[0] = self.elev.getCurrentFloor()

		if(self.requestList.isRequests()):
			state[1] = self.elev.getMotorDirection()
		else:
			state[1] = OUTPUT.MOTOR_STOP
		state[2] = self.requestList.furthestRequestThisWay()	#furthest floor
		
		state += self.requestList.getGlobalFromLocal()

		if self.prevState != state:
			self.prevState = state
			msg = self.msgEncoder.encode("state", self.prevState)
			if not msg in self.msgBuffer:
				self.printString += "\n" +   'newState'
				self.msgBuffer.append(msg)

		return self.msgBuffer, self.prevState

	def updatePendingRequests(self, newRequestList):
		self.pendingRequests.list = newRequestList
		self.pendingRequests.updateRequestFile()

	def stopAndRemoveRequests(self):
		hallRequests = self.requestList.removeRequestsForDirection(self.elev.getCurrentFloor())
		
		for request in hallRequests:
			if request and request[0] != INPUT.BUTTON_IN:
				msg = self.msgEncoder.encode("removePending", request)
				if(msg not in self.msgBuffer):
					self.msgBuffer.append(self.msgEncoder.encode("removePending", request))

	def openDoor(self):

		self.printString += "\n" +   "At requested floor"
		self.floorStopTimer.resetTimer()
		self.elev.stop()
		self.printString += "\n" +   "Doors open"
		self.elev.setDoorLamp(1)

	def startFunction(self):
		self.elev.setMotorDirection(OUTPUT.MOTOR_UP)

		while self.elev.getFloorSensorSignal() == INPUT.NO_FLOOR:
			time.sleep(0.1)
				
		self.elev.setCurrentFloor(self.elev.getFloorSensorSignal())
		self.printString += "\n" +   "elev.curr: " + str(self.elev.getCurrentFloor()) + " getfloor: " + str(self.elev.getFloorSensorSignal())
		self.prevState = [self.elev.getCurrentFloor(), self.elev.getMotorDirection(), 0]
		msg = self.msgEncoder.encode("state", self.prevState)
		self.msgBuffer.append(msg)

		self.elev.stop()


	def runElevator(self):

		self.startFunction()

		currentFloor = -1

		while self.slave.alive:
			if connectionLost(self.elevIP) or self.elev.getStopSignal(): 
				self.elev.stop()
				break

			self.printString = ""
			
			#check for request
			self.requestList.addRequest()

			self.printString += "\nglobal list:\n{}\n\n".format(self.requestList.globalList)

			"""This is where we send requests to master"""

			globalRequest = self.requestList.getGlobalRequest()

			if globalRequest:
				msg = self.msgEncoder.encode("request", globalRequest)
				if not msg in self.msgBuffer:
					self.msgBuffer.append(msg)
					self.sendState()
	######

			receivedMessage = self.slave.receive()
			

			# print "recievedMessage: ".format(receivedMessage)


			if receivedMessage != None and receivedMessage != " ":
				try:
					masterMessage = json.loads(receivedMessage)
				except:
					cprint("json.loads error", WARNING)
					self.slave.handleLossOfMaster()
					continue

				if masterMessage['msgType'] == 'request':
					self.printString += "Recieved global request from master {}".format(masterMessage["content"])
					
					self.requestList.addGlobalRequest(map(int, masterMessage['content'].split(' ')))

				elif masterMessage['msgType'] == 'elev_id':
					if self.slave.getSlaveID() != int(masterMessage['content']):
						self.slave.setSlaveID(int(masterMessage['content']))


				elif masterMessage['msgType'] == 'pendingRequests':
					msg = self.msgParser.parse(masterMessage)
					self.updatePendingRequests(msg)

				elif masterMessage["msgType"] == "slaveLost":
					self.requestList.addListToRequestList(self.pendingRequests.list)

				else:
					self.printString += "\n" +   'unknown msg from master'

			else:

			 	self.printString += "received none"
			
			self.elevPanel.updateLightsByRequestList(self.requestList.list, self.pendingRequests.list)

			if(self.elev.getFloorSensorSignal() != INPUT.NO_FLOOR):	
				self.elev.setCurrentFloor(self.elev.getFloorSensorSignal())
				self.elev.setFloorIndicator(self.elev.getCurrentFloor())
				self.sendState()

				if self.requestList.isRequestsatFloor(self.elev.getCurrentFloor()):
					if(self.requestList.isRequestAtFloorAndDirection(self.elev.getCurrentFloor()) or 
					   self.requestList.furthestRequestThisWay() == self.elev.getCurrentFloor()):
						self.stopAndRemoveRequests()
						self.openDoor()

			# print 'self.elev.getCurrentFloor()' + str(self.elev.getCurrentFloor())

			if self.msgBuffer:
				self.slave.send(self.msgBuffer.pop(0))
			else:
				self.slave.sendPing()

			if self.printString != self.printStringPrev:
				# print self.printString
				self.printStringPrev = self.printString

			# print "direction: {}\tlocal requests: {} pending: {}".format(self.elev.direction, self.requestList.list,self.pendingRequests.list)

			if self.floorStopTimer.getTimeFlag():
				if self.floorStopTimer.isTimeOut(1):
					self.printString += "\n" +   "Doors close"
					self.elev.setDoorLamp(0)
				else:
					time.sleep(0.1)
					continue

			if self.requestList.requestsAhead():
				self.elev.setMotorDirection(self.elev.getMotorDirection())

			elif self.requestList.isRequests():
				self.elev.reverseElevDirection()

		runPythonScript("main.py")