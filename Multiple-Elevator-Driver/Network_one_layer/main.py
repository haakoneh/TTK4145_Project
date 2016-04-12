import threading

import sys
from masterMeetSlave import *
from globalFunctions import * 
import master
import Slave
import time

#Slave = imp.load_source('Slave', 'Slave/Slave.py')
#import Slave
sys.path.insert(0, 'Slave/')

import Slave

globalResetFlag = 0

def main():

	print "main"
	seeker = MasterSlaveSeeker()

	masterIP = seeker.findMaster()

	if(masterIP):
		#print masterIP
		#continue as slave
		Slave.slaveInit(masterIP)
		
	else:
		print "before master.run()"

		master.run()
		print "after master.run()"

		time.sleep(0.01)

		Slave.slaveInit(getMyIP())
		print "after slave.run()"
		
		runPythonScript("processMonitor.py")
		print "Monitor setup"

		#Slave.run(masterIP)#master needs it's own local slave




main()

# while True:
# 	if globalResetFlag == 1:
# 		globalResetFlag = 0
# 		main()
# 	time.sleep(1)
