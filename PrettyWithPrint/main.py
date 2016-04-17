from MasterMeetSlave import *
from GlobalFunctions import * 
import SlaveElevator
import time

def main():
	seeker = MasterSlaveSeeker()

	masterIP = seeker.findMaster()

	if(masterIP):
		slaveElevator = SlaveElevator.SlaveElevator(masterIP, 23432)

	else:
		runPythonScript("Master.py")

		time.sleep(1)

		slaveElevator = SlaveElevator.SlaveElevator(getMyIP(), 23432)

main()
