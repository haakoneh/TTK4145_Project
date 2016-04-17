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

def updatePendingRequests(requestList, newData):
	"""we completely replace pendingRequestlist when master tells us to"""
	requestList = newData


def stopAndRemoveRequests(elev, msgBuffer, msgEncoder, requestList):

	hallRequests = requestList.removeAndReturnRequestsForDirection(elev.current_floor)

	print "hallRequests: ", hallRequests

	for request in hallRequests:
		if request:
			print "sending remove message to master:\n\tmsg: {}".format(msgEncoder.encode("removePending", request))
			msgBuffer.append(msgEncoder.encode("removePending", request))

	return msgBuffer


def runElevator(masterIP, port):
	global printString, prevPrintString

	slave = slaveNetwork.Slave(masterIP, port)

	elev = Elevator()
	elevPanel = Elevator_Panel(elev)
	elevPanel.turnOffAllLights()

	requestList = Request_List(elev, 'requestListFile.txt')
	globalRequestList = Request_List(elev, 'globalRequestListFile.txt')
#New stuff relating to pendingRequsts####################
	pendingRequests = Request_List(elev, 'pendingRequests.txt')
#########################################################

	floorStopTimer = TimerElev()
	msgEncoder = MessageEncoder()
	msgParser = MessageParser()
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
		printString += "\n \t\t\tID: {}".format(slave.getSlaveID())
		receivedMessage = slave.receive()
		# try:
		if receivedMessage != None:
			masterMessage = json.loads(receivedMessage)
			#printString += "\n" +   'masterMessage: ' + str(masterMessage['msgType'])

			if masterMessage['msgType'] == 'request':
				#printString += "Recieved global request from master {}".format(masterMessage["content"])
				printString += "Recieved global request from master {}".format(masterMessage["content"])
				"""change this function to do smart stuf"""
				
				#requestList.addGlobalRequest(request)
				requestList.addGlobalRequest(map(int, masterMessage['content'].split(' ')))

			elif masterMessage['msgType'] == 'elev_id':
				if slave.getSlaveID() != int(masterMessage['content']):
					slave.setSlaveID(int(masterMessage['content']))

#New stuff related to pending request added here
#######################################################
			elif masterMessage['msgType'] == 'pendingRequests':
				print "\n\t\t\t****pendingRequests: {}".format(pendingRequests.list)
				msg = msgParser.parse(masterMessage)
				print "msgtype == pending, masterMessage: {}\nmasterMessage parsed: {}".format(masterMessage, msg)
				pendingRequests.list = msg
				print "\n\t\t\t****pendingRequests: {}".format(pendingRequests.list)
				updatePendingRequests(pendingRequests, pendingRequests.list)
				print "\nAttempting to update pending requestfile"
				pendingRequests.updateRequestFile()


#######################################################

			else:
				printString += "\n" +   'unknown msg from master'
		# except:
		else:
		 	# printString += '\nexcept for masterMessage\n with message: {}'.format(receivedMessage)
		 	printString += "received none"
		
		elevPanel.updateLightsByRequestList(requestList.list, pendingRequests.list)

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

			if requestList.isRequestsatFloor(elev.current_floor):
				if(requestList.isRequestAtFloorAndDirection(elev.current_floor)):

					msgBuffer = stopAndRemoveRequests(elev, msgBuffer, msgEncoder, requestList)

					openDoor(floorStopTimer, elev)

				elif requestList.furthestRequestThisWay() == elev.getCurrentFloor():
					requestList.removeRequestsAtFloor(elev.getCurrentFloor())
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