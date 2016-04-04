
maxCost = 2*NR_FLOORS - 1

def calulateCost(globalRequest):
	if(globalRequest is ahead):
		totalDistance = abs(globalRequest.floor - currentFloor)
	else:
		lastRequestFloor = req_list.furthermostRequest() #(in current direction)
		currentToNextFloor = abs(elev.currentFloor - lastRequestFloor)

		totalDistance = abs(lastRequestFloor - elev.currentFloor) + abs(lastRequestFloor - globalRequest.floor)

	return totalDistance
