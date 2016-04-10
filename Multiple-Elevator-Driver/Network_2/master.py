#master.py
#import thread
import threading
from masterMeetSlave import *

statelist = []


#--------main purpose-------

# settup server

# start elevator
# thread UDP_listenforBroadcast

# refresh elevator states and order queue

# for orders in queue:
# 	elevator = findOptimalElevator(elevStateList, request)

# send(order, elevator)

#---------------------------

#startup: look for other masters first
seeker = MasterSlaveSeeker()

if(seeker.findMaster()):
	#continue as slave
	

seekerThread = threading.Thread(target = seeker.replyToSlaves)
seekerThread.start()

# seeker.replyToSlaves()
