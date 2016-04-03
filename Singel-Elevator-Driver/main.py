from elev import Elevator
import time
def main():
	elev = Elevator()
	elev.setSpeed(300)
	current_floor = -1


	while True:

		
		if elev.getFloorSensorSignal() == 0:
			elev.setSpeed(300)
		elif elev.getFloorSensorSignal() == elev.NUM_FLOORS-1:
			elev.setSpeed(-300)

		if(elev.getFloorSensorSignal() != -1):
			elev.setFloorIndicator(elev.getFloorSensorSignal())
			if(current_floor != elev.getFloorSensorSignal()):
				current_floor = elev.getFloorSensorSignal()
				print current_floor
				elev.setFloorIndicator(current_floor)
			time.sleep(0.01)
			
		

		if elev.getStopSignal():
			elev.stop()
			break

main()