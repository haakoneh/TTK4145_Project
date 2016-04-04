from elev import Elevator
import request_list
from request_list import Request_List 
from channels import INPUT, OUTPUT
from elevator_panel import Elevator_Panel 
from timer import Timer
import time


def main():
	elev = Elevator()
	elev_panel = Elevator_Panel(elev)
	elev_panel.turnOffAllLights()
	req_list = Request_List(elev)
	floor_timer = Timer()

	elev.setSpeed(300)

	currentFloor = -1

	while elev.getFloorSensorSignal() == -1:
		time.sleep(0.1)
		
	if ((elev.getFloorSensorSignal() != currentFloor)):
		#if(1 != -1):
		currentFloor = elev.getFloorSensorSignal()
		print "elev.curr: " + str(currentFloor) + " getfloor: " + str(elev.getFloorSensorSignal())

	elev.stop()

	#this loop asumes that elev.current floor is updated
	while True:
		
		#check for request, and udp msg
		req_list.addRequest()
		elev_panel.updateLightsByRequestList(req_list.list)
		#udp check

		#check if waiting at floor
		if floor_timer.getTimeFlag():
			if floor_timer.isTimeOut(1):
				print "Doors close"
				pass
			else:
				time.sleep(0.1)
				continue

		#This if cluster controlls direction
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
			elev.setFloorIndicator(elev.getFloorSensorSignal())
				
			if req_list.isRequestsatFloor(elev.current_floor):
				#assuming the following function works
				if(req_list.isRequestAtFloorAndDirection(elev.current_floor)):
					print "At requested floor"
					req_list.removeRequestsForDirection(elev.current_floor)
					floor_timer.resetTimer()
					elev.stop()
					print "Doors open"

				elif elev.checkEndPoints():
					print "at requested floor"
					req_list.removeRequestsAtFloor(elev.current_floor)
					#Wait at floor for 1 sec
					floor_timer.resetTimer()
					elev.stop()
					print "Doors open"

		if elev.getStopSignal():
		 	elev.stop()
		 	break

		time.sleep(0.01)

main()