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

	while True:
		
		if elev.getFloorSensorSignal() == 0:
			elev.setSpeed(300)
		elif elev.getFloorSensorSignal() == elev.NUM_FLOORS-1:
			elev.setSpeed(-300)

		if(elev.getFloorSensorSignal() != -1):
			#elev.current_floor = elev.getFloorSensorSignal
			#elev.setFloorIndicator(elev.getFloorSensorSignal())
			if(current_floor != elev.getFloorSensorSignal()):
				current_floor = elev.getFloorSensorSignal()
				print current_floor
				elev.setFloorIndicator(current_floor)
			time.sleep(0.01)
			
		#elev.checkFloorButtons()

		#req_list.refreshRequestList()
		req_list.addRequest()
		#elev_panel.refreshLights()

		if elev.getStopSignal():
			elev.stop()
			break

main()