#master.py
#import thread
import threading
import sys
from masterMeetSlave import *
from runPythonScript import *
#import imp
#NetworkMaster = imp.load_source('NetworkMaster', 'Server/NetworkMaster.py')

sys.path.append('Server/')

import NetworkMaster


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
def run():
	seeker = MasterSlaveSeeker()

	print "before replyThread"
	seekerThread = threading.Thread(target = seeker.replyToSlaves)
	seekerThread.start()

	print "Spawning NetworkMaster.starter()"

	masterNetworkThread = threading.Thread(target = NetworkMaster.starter)
	masterNetworkThread.start()
	

