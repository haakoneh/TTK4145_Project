from elev import Elevator
import request_list
from request_list import Request_List 
from channels import INPUT, OUTPUT
from elevator_panel import Elevator_Panel 
from timer import *
import time
import slaveNetwork
from globalFunctions import *
from MessageFormatHandler import *
networkAliveFlag = True

printString = ""
prevPrintString = ""

def openDoor(timer, elevator):
	global printString
	printString += "\n" +   "At requested floor"
	timer.resetTimer()
	elevator.stop()
	printString += "\n" +   "Doors open"

def sendState(elev, requestList, prevState, msgEncoder, msgBuffer):
	global printString
	state = [-1 , -1, -1]
	state[0] = elev.getCurrentFloor()

	if(requestList.isRequests()):
		state[1] = elev.getMotorDirection()
	else:
		state[1] = OUTPUT.MOTOR_STOP
	state[2] = requestList.furthestRequestAway()	#furthest floor
	
	state += requestList.getGlobalFromLocal()

	if prevState != state:
		prevState = state
		msg = msgEncoder.encode("state", prevState)
		if not msg in msgBuffer:
			printString += "\n" +   'newState'
			msgBuffer.append(msg)
	return msgBuffer, prevState

def runElevator(masterIP, port):
	global printString, prevPrintString

	slave = slaveNetwork.Slave(masterIP, port)

	elev = Elevator()
	elevPanel = Elevator_Panel(elev)
	elevPanel.turnOffAllLights()
	requestList = Request_List(elev, 'requestListFile.txt')
	floorStopTimer = TimerElev()
	msgEncoder = MessageEncoder()
	msgBuffer = []

	prevState = [-1, -1, -1]
	
	elev.setSpeed(300)

	currentFloor = -1

	while elev.getFloorSensorSignal() == -1:
		time.sleep(0.1)
		
	if ((elev.getFloorSensorSignal() != currentFloor)):
		currentFloor = elev.getFloorSensorSignal()
		printString += "\n" +   "elev.curr: " + str(currentFloor) + " getfloor: " + str(elev.getFloorSensorSignal())
		prevState = [elev.getCurrentFloor(), elev.getMotorDirection(), 0]
		msg = msgEncoder.encode("state", prevState)
		msgBuffer.append(msg)


	elev.stop()

	while slave.alive:
		printString = ""
		
		#check for request
		requestList.addRequest()

		printString += "\nglobal list:\n{}\n\n".format(requestList.globalList)

		"""This is where we send requests to master"""

		globalRequest = requestList.getGlobalRequest()

		if globalRequest:
			msg = msgEncoder.encode("request", globalRequest)
			if not msg in msgBuffer:
				msgBuffer.append(msg)
				printString += "\n" +   "Slave sending: {}".format(msg)
				msgBuffer, prevState = sendState(elev, requestList, prevState, msgEncoder, msgBuffer)

		"""recieve from master"""
		try:
			masterMessage = json.loads(slave.receive())
			#printString += "\n" +   'masterMessage: ' + str(masterMessage['msgType'])

			if masterMessage['msgType'] == 'request':
				#printString += "Recieved global request from master {}".format(masterMessage["content"])
				printString += "Recieved global request from master {}".format(masterMessage["content"])
				"""change this function to do smart stuf"""
				
				#requestList.addGlobalRequest(request)
				requestList.addGlobalRequest(map(int, masterMessage['content'].split(' ')))

			elif masterMessage['msgType'] == 'elev_id':
				#printString += "\n" +   'inside ELIF in slaveMain'
				if slave.getSlaveID() != int(masterMessage['content']):
					slave.setSlaveID(int(masterMessage['content']))

			else:
				printString += "\n" +   'unknown msg from master'
		except:
		 	printString += '\nexcept for masterMessage\n'
		
		elevPanel.updateLightsByRequestList(requestList.list)

		if floorStopTimer.getTimeFlag():
			if floorStopTimer.isTimeOut(1):
				printString += "\n" +   "Doors close"
			else:
				time.sleep(0.1)
				continue

		#more requests ahead
		if requestList.requestsAhead():
			elev.setMotorDirection(elev.direction)
		
		#there are requests, but not ahead
		elif requestList.isRequests():
			elev.reverseElevDirection()

		#no orders
		else:
			if(elev.getFloorSensorSignal() != -1):
				elev.setMotorDirection(OUTPUT.MOTOR_STOP)
				elev.current_floor = elev.getFloorSensorSignal()

		#we're at a floor, we check if we should stop here
		if(elev.getFloorSensorSignal() != -1):
			if(elev.getFloorSensorSignal() != currentFloor):	
				current_floor = elev.getFloorSensorSignal()
				elev.setCurrentFloor(current_floor)
				elev.setFloorIndicator(elev.getCurrentFloor())
				# printString += "\n" +   "Trying to send state"
				"""this is where we update and send state"""

				msgBuffer, prevState = sendState(elev, requestList, prevState, msgEncoder, msgBuffer)

				# state = [-1 , -1, -1]
				# state[0] = elev.getCurrentFloor()

				# if(requestList.isRequests()):
				# 	state[1] = elev.getMotorDirection()
				# else:
				# 	state[1] = OUTPUT.MOTOR_STOP

				# state[2] = requestList.furthestRequestAway()	#furthest floor
				# state += requestList.list

				# if prevState != state:
				# 	prevState = state
				# 	msg = msgEncoder.encode("state", prevState)
				# 	if not msg in msgBuffer:
				# 		printString += "\n" +   'newState'
				# 		msgBuffer.append(msg)
	
			if requestList.isRequestsatFloor(elev.current_floor):
				if(requestList.isRequestAtFloorAndDirection(elev.current_floor)):
					requestList.removeRequestsForDirection(elev.current_floor)
					openDoor(floorStopTimer, elev)

				elif len(requestList.list) == 1:
					requestList.removeRequestsAtFloor(elev.current_floor)
					openDoor(floorStopTimer, elev)

				elif elev.checkEndPoints():		
					requestList.removeRequestsAtFloor(elev.current_floor)
					openDoor(floorStopTimer, elev)

		#printString += "\n*********\nreqList:\n{}\n\n".format(requestList.list)
		printString += "\nlocal list:\n{}\n\n".format(requestList.list)

		if msgBuffer:
			slave.send(msgBuffer.pop(0))
		else:
			slave.sendPing()


		if printString != prevPrintString:
			print printString
			prevPrintString = printString

		if elev.getStopSignal():
		 	elev.stop()
		 	break

		time.sleep(0.01)


	#runPythonScript("main.py")