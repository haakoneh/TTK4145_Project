from elev import Elevator
<<<<<<< HEAD
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
=======
import time
def main():
	elev = Elevator()
	elev.setSpeed(300)
	current_floor = -1


	while True:

>>>>>>> 6265a410603b5cc2f5fee66c9c51c1e3b927fa44
		
		if elev.getFloorSensorSignal() == 0:
			elev.setSpeed(300)
		elif elev.getFloorSensorSignal() == elev.NUM_FLOORS-1:
			elev.setSpeed(-300)

		if(elev.getFloorSensorSignal() != -1):
<<<<<<< HEAD
			#elev.current_floor = elev.getFloorSensorSignal
			#elev.setFloorIndicator(elev.getFloorSensorSignal())
=======
			elev.setFloorIndicator(elev.getFloorSensorSignal())
>>>>>>> 6265a410603b5cc2f5fee66c9c51c1e3b927fa44
			if(current_floor != elev.getFloorSensorSignal()):
				current_floor = elev.getFloorSensorSignal()
				print current_floor
				elev.setFloorIndicator(current_floor)
			time.sleep(0.01)
			
<<<<<<< HEAD
		#elev.checkFloorButtons()

		#req_list.refreshRequestList()
		req_list.addRequest()
		#elev_panel.refreshLights()
=======
		
>>>>>>> 6265a410603b5cc2f5fee66c9c51c1e3b927fa44

		if elev.getStopSignal():
			elev.stop()
			break

main()