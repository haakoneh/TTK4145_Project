from elev import Elevator
import request_list
from request_list import Request_List 

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

	while True:
		if elev_panel.noRequests():
			time.sleep(0.1)

		else: 
			if(elev.getFloorSensorSignal() != -1):
				if(current_floor != elev.getFloorSensorSignal()):
					current_floor = elev.getFloorSensorSignal()
					print current_floor
					elev.setFloorIndicator(current_floor)
					#Check if req is fulfilles
			
			
			
			req_list.addRequest()

		if elev.getStopSignal():
			elev.stop()
			break



main()