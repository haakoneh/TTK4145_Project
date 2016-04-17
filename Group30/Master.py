import threading
from MasterMeetSlave import *
from GlobalFunctions import * 
import NetworkMaster

def runMaster():
	print "Master"

	seeker = MasterSlaveSeeker()

	seekerThread = threading.Thread(target = seeker.replyToSlaves)
	seekerThread.start()

	masterNetworkThread = threading.Thread(target = NetworkMaster.starter, args = (23432, ))
	masterNetworkThread.start()

runMaster()
