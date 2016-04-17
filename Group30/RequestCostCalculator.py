from channels import INPUT

up = 0
down = 1
stop = 2

#StateList indexes
floor = 0
direction = 1
furthestRequest = 2
#######

#RequestList indexes
reqButton = 0
reqFloor = 1




def calculateCost(state, request):

	global up, down, stop, floor, direction, furthestRequest
	totalDistance = INPUT.NUM_FLOORS * 2

	if(state[furthestRequest] == request[reqFloor]):
		return 0


	if (state[direction] == stop):
		totalDistance = abs(request[reqFloor] - state[floor])
		return totalDistance


	if(isAhead(state, request)):
		if (state[direction] == request[reqButton]):
			totalDistance = abs(request[reqFloor] - state[floor])
		else:
			turnPoint = state[furthestRequest]
			distanceTilTurn = abs(state[floor] - turnPoint)
			totalDistance = distanceTilTurn + abs(request[reqFloor] - turnPoint)
	else:
		turnPoint = state[furthestRequest]
		distanceTilTurn = abs(state[floor] - turnPoint)
		totalDistance = distanceTilTurn + abs(request[reqFloor] - turnPoint)
	
	return totalDistance



def isAhead(state, request):
	global up, down, stop, floor, direction, furthestRequest

	if(state[direction] == down):

		if(state[floor] > request[reqFloor]):
			return True
		elif(state[floor] < request[reqFloor]):
			return False
		else:
			return -1
	elif(state[direction] == up):
		if(state[floor] < request[reqFloor]):
			return True
		elif(state[floor] > request[reqFloor]):
			return False
		else:
			return -1
	else:

		return True
