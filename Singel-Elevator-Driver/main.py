from elev import Elevator
import request_list
from request_list import Request_List 
from channels import INPUT, OUTPUT
from elevator_panel import Elevator_Panel 
import time



def main():
	elev = Elevator()
	elev_panel = Elevator_Panel(elev)
	elev_panel.turnOffAllLights()
	req_list = Request_List(elev)

	elev.setSpeed(300)

	current_floor = -1

	while elev.getFloorSensorSignal() == -1:
		time.sleep(0.1)


	#this loop asumes that elev.current floor is updated
	while True:
		

		elev.current_floor = elev.getFloorSensorSignal()

		#Polls buttons for requests
		req_list.addRequest()


		#This if cluster controlls direction
		#more requests ahead
		if req_list.requestsAhead():
			continue
		#there are requests, but not ahead
		elif req_list.isRequests():
			elev.reverseElevDirection()
			elev.setMotorDirection(elev.direction)
		#no orders
		else:
			if(elev.getFloorSensorSignal() != -1):
				elev.setMotorDirection(OUTPUT.MOTOR_STOP)



		#we're at a floor, we check if we should stop here
		if(elev.getFloorSensorSignal != -1):
			#assuming the following function works
			if(req_list.isRequestsAtFloorAndDirection(elev.current_floor)):

				#THIS IS WHERE I LEFT
				#STOP ELEVATOR (MAKE TIMER.PY)
				#REMOVE INSIDE REQUESTS FOR THIS FLOOR
				#REMOVE REQUESTS FOR THE SAME DIRECTION AT THIS FLOOR



		if(elev.current_floor == 0):
			elev.setMotorDirection(OUTPUT.MOTOR_UP)
		elif(elev.current_floor == INPUT.NUM_FLOORS - 1):
			elev.setMotorDirection(OUTPUT.MOTOR_DOWN)




		if elev.getStopSignal():
		 	elev.stop()
		 	break

		time.sleep(0.01)

main()