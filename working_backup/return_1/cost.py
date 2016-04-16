
#maxCost = 2*NR_FLOORS - 1
#we asume that motor direction and buttonTYpe agree here
up = 0
down = 1
stop = 2

#used as indexes for lists: state[] and request[]
#we assume request[floor, buttonType]
############
floor = 0
direction = 1
furthestRequest = 2
buttonType = 1
############

NUM_FLOORS = 3



def calculateCost(state, request):
	global up, down, stop, floor, direction, furthestRequest, buttonType
	totalDistance = NUM_FLOORS * 2

	print "state: ", state
	print "request: ", request

	if (state[direction] == stop):
		print "dir == stop"
		#Here it's assumed that if elev.direction is stop, elevator doesn't have requests
		totalDistance = abs(request[floor] - state[floor])
		return totalDistance


	if(isAhead(state, request)):
		if (state[direction] == request[buttonType]):
			totalDistance = abs(request[floor] - state[floor])
		else:
			turnPoint = state[furthestRequest]
			distanceTilTurn = abs(state[floor] - turnPoint)
			totalDistance = distanceTilTurn + abs(request[floor] - turnPoint)
	else:
		turnPoint = state[furthestRequest]
		distanceTilTurn = abs(state[floor] - turnPoint)
		totalDistance = distanceTilTurn + abs(request[floor] - turnPoint)
	
	return totalDistance



def isAhead(state, request):
	global up, down, stop, floor, direction, furthestRequest, buttonType

	if(state[direction] == down):

		if(state[floor] > request[floor]):
			return True
		elif(state[floor] < request[floor]):
			return False
		else:
			print "state[floor] == request[floor]"
			return -1
	elif(state[direction] == up):
		if(state[floor] < request[floor]):
			return True
		elif(state[floor] > request[floor]):
			return False
		else:
			print "state[floor] == request[floor]"
			return -1
	else:
		#state is directionless, which means we're probably orderless, pretend it's ahead
		print "No direction"
		return True

def costTest():
	#[floor, button, furthestFloor]
	r1 = [2, up]
	r2 = [2, down]
	r3 = [3, up]
	r4 = [3, down]
	r5 = [1, down]
	r6 = [4, down]

	s1 = [3, down, 4]
	s2 = [3, down, 1]
	s3 = [2, up, 1]
	s4 = [2, down, 1]
	s5 = [2, down, 1]
	s6 = [3, down, 0]

	print("Cost1: {}").format(calculateCost(s1, r1))
	print("Cost2: {}").format(calculateCost(s2, r2))
	print("Cost3: {}").format(calculateCost(s3, r3))
	print("Cost4: {}").format(calculateCost(s4, r4))
	print("Cost5: {}").format(calculateCost(s5, r5))
	print("Cost6: {}").format(calculateCost(s6, r6))



	r = [2, up]
	s = [0, up, 3]
	print calculateCost(s,r)

#costTest()
