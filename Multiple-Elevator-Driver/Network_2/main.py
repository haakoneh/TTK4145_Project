import threading
#import imp
import sys
from masterMeetSlave import *
from runPythonScript import *
import master
#Client = imp.load_source('Client', 'Client/Client.py')
#import Client
sys.path.insert(0, 'Client/')

import Client

def main():
	seeker = MasterSlaveSeeker()

	masterIP = seeker.findMaster()

	if(masterIP):
		#print masterIP
		#continue as slave
		Client.run(masterIP)
		
	else:
		master.run()


main()
