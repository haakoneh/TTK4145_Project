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



def openDoor(timer, elevator):
	print "At requested floor"
	timer.resetTimer()
	elevator.stop()
	print "Doors open"


def runElevator(masterIP, port):
	

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
	req_list = Request_List(elev)
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
		print "elev.curr: " + str(currentFloor) + " getfloor: " + str(elev.getFloorSensorSignal())
		prevState = [elev.getCurrentFloor(), elev.getMotorDirection(), 0]
		msg = msgEncoder.encode("state", prevState)
		msgBuffer.append(msg)


	elev.stop()

	##################################################

	#this loop asumes that elev.current floor is updated
	while True:
		
		#check for request
		req_list.addRequest()

		

		"""This is where we send requests to master"""

		globalRequest = req_list.getGlobalRequest()

		if globalRequest:
			msg = msgEncoder.encode("request", globalRequest)
			if not msg in msgBuffer:
				msgBuffer.append(msg)
				print "Slave sending: {}".format(msg)

		"""recieve from master"""
		try:
			masterMessage = json.loads(slave.receive())
			print 'masterMessage: ' + str(masterMessage['msgType'])

			if masterMessage['msgType'] == 'request':
				print 'inside if in slaveMain'
				"""change this function to do smart stuf"""
				req_list.addGlobalRequest(request)
				# request = self.messageParser.parse(receivedString)

			elif masterMessage['msgType'] == 'elev_id':
				print 'inside ELIF in slaveMain'
				if slave.getSlaveID() != int(masterMessage['content']):
					slave.setSlaveID(int(masterMessage['content']))

			else:
				print 'unknown msg from master'
		except:
			pass
		
		elev_panel.updateLightsByRequestList(req_list.list)

		if floor_timer.getTimeFlag():
			if floor_timer.isTimeOut(1):
				print "Doors close"
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

				# print "Trying to send state"
				"""this is where we update and send state"""
				state = [-1 , -1, -1]
				state[0] = elev.getCurrentFloor()
				state[1] = elev.getMotorDirection()
				state[2] = 2	#furthest floor
				if prevState != state:
					prevState = state
					msg = msgEncoder.encode("state", prevState)
					if not msg in msgBuffer:
						print 'newState'
						msgBuffer.append(msg)
					time.sleep(0.2)
			


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

		if msgBuffer:
			slave.send(msgBuffer.pop(0))
		else:
			slave.sendPing()


		if elev.getStopSignal():
		 	elev.stop()
		 	break

		time.sleep(0.01)





runElevator(getMyIP(), 9990)