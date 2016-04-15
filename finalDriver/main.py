import threading

import sys
from masterMeetSlave import *
from globalFunctions import * 
#import master
#import slaveMain
import time

#Slave = imp.load_source('Slave', 'Slave/Slave.py')
import slaveMain

globalResetFlag = 0

def main():

	print "main"
	seeker = MasterSlaveSeeker()

	masterIP = seeker.findMaster()

	if(masterIP):

		#proceed as slave
		print "proceed as slave"
		#runPythonScript("slaveMain.py")
		slaveMain.runElevator(masterIP, 40404)
	else:

		#proceed as Master
		print "before master.run()"
		runPythonScript("master.py")
		#master.run()
		print "after master.run()"

		time.sleep(1)

		#runPythonScript("processMonitor.py")
		#print "Monitor setup"
		
		slaveMain.runElevator(getMyIP(), 40404)
		#slaveMain.runElevator(getMyIP(), 9998)
		#runPythonScript("slaveMain.py")
		print "after slave.run()"
		
		

		#Slave.run(masterIP)#master needs it's own local slave




main()

