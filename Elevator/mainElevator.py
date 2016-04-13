from elev import Elevator
import request_list
from request_list import Request_List 
from channels import INPUT, OUTPUT
from elevator_panel import Elevator_Panel 
from timer import Timer
import time
from ElevNetworkCommunication import *


networkAliveFlag = True

def openDoor(timer, elevator):
	print "At requested floor"
	timer.resetTimer()
	elevator.stop()
	print "Doors open"


def main():
	elev = Elevator()
	elev_panel = Elevator_Panel(elev)
	elev_panel.turnOffAllLights()
	req_list = Request_List(elev)
	floor_timer = Timer()
	
	stateCommunication = ExternalFileHandler('globalStateFile.txt')


	elev.setSpeed(300)

	currentFloor = -1

	while elev.getFloorSensorSignal() == -1:
		time.sleep(0.1)
		
	if ((elev.getFloorSensorSignal() != currentFloor)):
		currentFloor = elev.getFloorSensorSignal()
		print "elev.curr: " + str(currentFloor) + " getfloor: " + str(elev.getFloorSensorSignal())

	elev.stop()

	#this loop asumes that elev.current floor is updated
	while True:
		
		#check for request, and udp msg
		req_list.addRequest()
		elev_panel.updateLightsByRequestList(req_list.list)
		#udp check, added in multiple elevator 

		#check if waiting at floor
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
			
			stateCommunication.writeFile(map(int, [elev.getCurrentFloor(), elev.getMotorDirection()]))


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



		#write state to file
		#write requests to file

		if elev.getStopSignal():
		 	elev.stop()
		 	break

		time.sleep(0.01)

main()