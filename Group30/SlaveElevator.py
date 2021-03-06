from elev import Elevator
from RequestList import RequestList 
from channels import INPUT, OUTPUT
import ElevatorPanel 
from StopWatch import *
import time
import SlaveNetwork
from GlobalFunctions import *
from MessageFormatHandler import *
from colors import *

class SlaveElevator:
	def __init__(self, masterIP, port):

		self.slave = SlaveNetwork.SlaveNetwork(masterIP, port)
		self.elevIP = getMyIP()
		self.elev = Elevator()
		self.elevPanel = ElevatorPanel.ElevatorPanel(self.elev)
		self.elevPanel.turnOffAllLights()

		self.requestList = RequestList(self.elev, 'requestListFile.txt')
		self.globalRequestList = RequestList(self.elev, 'globalRequestListFile.txt')
		self.pendingRequests = RequestList(self.elev, 'pendingRequests.txt')

		self.requestList.addListToRequestList(self.pendingRequests.list)

		self.floorStopTimer = StopWatch()
		self.powerLossTimer = StopWatch()
		self.msgEncoder = MessageEncoder()
		self.msgParser = MessageParser()
		self.msgBuffer = []
		self.prevState = [-1, -1, -1]

		self.prevFloor = -1
		self.receiveNoneCounter = 0

		self.powerOutTime = 10
		

		self.runElevator()
		

	def getCurrentState(self):
		self.state = [-1 , -1, -1]
		self.state[0] = self.elev.getFloorSensorSignal()

		if(self.requestList.isRequests()):
			self.state[1] = self.elev.getMotorDirection()
		else:
			self.state[1] = OUTPUT.MOTOR_STOP
		self.state[2] = self.requestList.furthestRequestThisWay() 

		return self.state


	def sendState(self):	
		if self.prevState != self.getCurrentState():
			self.prevState = self.state
			msg = self.msgEncoder.encode("state", self.prevState)
			if not msg in self.msgBuffer:
				self.msgBuffer.append(msg)

			self.powerLossTimer.reset()	

		elif not self.requestList.isRequests():
			self.powerLossTimer.reset()

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
		self.floorStopTimer.reset()
		self.elev.stop()
		self.elev.setDoorLamp(1)

	def startFunction(self):
		self.elev.setMotorDirection(OUTPUT.MOTOR_UP)
		
		while self.elev.getFloorSensorSignal() == INPUT.NO_FLOOR:
			time.sleep(0.1)
				
		self.elev.setCurrentFloor(self.elev.getFloorSensorSignal())
		self.prevState = [self.elev.getCurrentFloor(), self.elev.getMotorDirection(), 0]
		msg = self.msgEncoder.encode("state", self.prevState)
		self.msgBuffer.append(msg)
		self.powerLossTimer.reset()
		self.elev.stop()


	def runElevator(self):

		self.startFunction()

		while self.slave.alive:

			if connectionLost(self.elevIP): 
				cprint("Connection lost: break", FAIL)
				self.elev.stop()
				self.slave.handleLossOfMaster()
				break

			elif self.elev.getStopSignal():
				cprint("Stop button pressed: break", GREEN)
				self.elev.stop()
				break

			elif self.receiveNoneCounter >= 5:
				cprint("receiveNoneCounter reached limit: break", FAIL)
				break

			while(self.powerLossTimer.isTimeOut(self.powerOutTime)):
				self.slave.send(self.msgEncoder.encode('powerLost', None))
				cprint("powerLossTimer timeout: Most likely powerloss. Rebooting shortly", WARNING)
				if self.prevState != self.getCurrentState():
					self.elev.stop()
					break

			self.requestList.addRequest()

			globalRequest = self.requestList.getGlobalRequest()

			if globalRequest:
				msg = self.msgEncoder.encode("request", globalRequest)
				if not msg in self.msgBuffer:
					self.msgBuffer.append(msg)

			receivedMessage = self.slave.receive()


			if receivedMessage != None and receivedMessage != " ":
				try:
					masterMessage = json.loads(receivedMessage)
					receiveNoneCounter = 0
				except:
					cprint("json.loads error", WARNING)
					self.slave.handleLossOfMaster()
					continue

				if masterMessage['msgType'] == 'request':
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
					cprint("Unknown message".format(receivedMessage), WARNING)
			else:
			 	cprint("received none: ".format(receivedMessage), WARNING)
			 	self.receiveNoneCounter += 1



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

			if self.msgBuffer:
				self.slave.send(self.msgBuffer.pop(0))
			else:
				self.slave.sendPing()

			if self.floorStopTimer.getTimeFlag():
				if self.floorStopTimer.isTimeOut(1):
					self.elev.setDoorLamp(0)
				else:
					time.sleep(0.1)
					continue

			if self.requestList.requestsAhead():
				self.elev.setMotorDirection(self.elev.getMotorDirection())

			elif self.requestList.isRequests():
				self.elev.reverseElevDirection()

		#we reboot the system if slave dies
		runPythonScript("main.py")