


#setup procedure
#With masterless setup, this procedure is identical for all elevators
def setupFromScratch():


	while True:
		broadcast("gief connections")
		recievedMsg , addr = recieve()	#with a certain timeout
	
	if recievedMsg == "gief connections"):

		linkWith(addr)
		#linkWith(addr, addr)?? Where 1st and 2nd parameter are forward and backward link respectively?

