import threading

import sys
from masterMeetSlave import *
from runPythonScript import *
from getIP import *
import master
import slave
import time

#Client = imp.load_source('Client', 'Client/Client.py')
#import Client
sys.path.insert(0, 'Client/')

import Client

globalResetFlag = 0

def main():

	print "main"
	seeker = MasterSlaveSeeker()

	masterIP = seeker.findMaster()

	if(masterIP):
		#print masterIP
		#continue as slave
		slave.run(masterIP)
		
	else:
		print "before master.run()"

		master.run()
		print "after master.run()"

		time.sleep(0.01)

		slave.run(getMyIP())
		print "after slave.run()"
		
		runPythonScript("processMonitor.py")
		print "Monitor setup"

		#Client.run(masterIP)#master needs it's own local slave




main()

# while True:
# 	if globalResetFlag == 1:
# 		globalResetFlag = 0
# 		main()
# 	time.sleep(1)
