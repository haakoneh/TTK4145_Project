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


def runElevator(masterIP, port):
	global printString, prevPrintString

	###########
	floorIndex = 1
	buttonIndex = 0

	##########



	#elevator initialization
	##############################################

	slave = slaveNetwork.Slave(masterIP, port)

	elev = Elevator()
	elev_panel = Elevator_Panel(elev)
	elev_panel.turnOffAllLights()
	req_list = Request_List(elev, 'requestListFile.txt')
	floor_timer = TimerElev()
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

	##################################################

	#this loop asumes that elev.current floor is updated
	while True:
		printString = ""
		
		#check for request
		req_list.addRequest()

		printString += "\nglobal list:\n{}\n\n".format(req_list.globalList)

		"""This is where we send requests to master"""

		globalRequest = req_list.getGlobalRequest()

		if globalRequest:
			msg = msgEncoder.encode("request", globalRequest)
			if not msg in msgBuffer:
				msgBuffer.append(msg)
				printString += "\n" +   "Slave sending: {}".format(msg)

		"""recieve from master"""
		# try:
		masterMessage = json.loads(slave.receive())
		#printString += "\n" +   'masterMessage: ' + str(masterMessage['msgType'])

		if masterMessage['msgType'] == 'request':
			printString += "Recieved global request from master {}".format(masterMessage["content"])
			"""change this function to do smart stuf"""
			
			
			#req_list.addGlobalRequest(request)

			printString += "*******request = {}".format()
			req_list.addGlobalRequest()




		elif masterMessage['msgType'] == 'elev_id':
			#printString += "\n" +   'inside ELIF in slaveMain'
			if slave.getSlaveID() != int(masterMessage['content']):
				slave.setSlaveID(int(masterMessage['content']))

		else:
			printString += "\n" +   'unknown msg from master'
		# except:
		# 	pass
		
		elev_panel.updateLightsByRequestList(req_list.list)

		if floor_timer.getTimeFlag():
			if floor_timer.isTimeOut(1):
				printString += "\n" +   "Doors close"
			else:
				time.sleep(0.1)
				continue

		#more requests ahead
		if req_list.requestsAhead():
			elev.setMotorDirection(elev.direction)
		
		#there are requests, but not ahead
		elif req_list.isRequests():
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
				state = [-1 , -1, -1]
				state[0] = elev.getCurrentFloor()
				state[1] = elev.getMotorDirection()
				state[2] = 2	#furthest floor
				if prevState != state:
					prevState = state
					msg = msgEncoder.encode("state", prevState)
					if not msg in msgBuffer:
						printString += "\n" +   'newState'
						msgBuffer.append(msg)
	
			if req_list.isRequestsatFloor(elev.current_floor):
				if(req_list.isRequestAtFloorAndDirection(elev.current_floor)):
					req_list.removeRequestsForDirection(elev.current_floor)
					openDoor(floor_timer, elev)

				elif len(req_list.list) == 1:
					req_list.removeRequestsAtFloor(elev.current_floor)
					openDoor(floor_timer, elev)

				elif elev.checkEndPoints():		
					req_list.removeRequestsAtFloor(elev.current_floor)
					openDoor(floor_timer, elev)

		#printString += "\n*********\nreqList:\n{}\n\n".format(req_list.list)
		printString += "\nlocal list:\n{}\n\n".format(req_list.list)


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

#runElevator(getMyIP(), 40404)