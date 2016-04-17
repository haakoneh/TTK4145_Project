import threading
from MasterMeetSlave import *
from GlobalFunctions import * 
import NetworkMaster

def runMaster():
	seeker = MasterSlaveSeeker()

	seekerThread = threading.Thread(target = seeker.replyToSlaves)
	seekerThread.start()

	masterNetworkThread = threading.Thread(target = NetworkMaster.starter)
	masterNetworkThread.start()

runMaster()
