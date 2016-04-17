from MasterMeetSlave import *
from GlobalFunctions import * 
import SlaveElevator
import time

def main():

	TCP_PORT = 23432

	seeker = MasterSlaveSeeker()

	masterIP = seeker.findMaster()

	if(masterIP):
		slaveElevator = SlaveElevator.SlaveElevator(masterIP, TCP_PORT)

	else:
		runPythonScript("Master.py")

		time.sleep(1)

		slaveElevator = SlaveElevator.SlaveElevator(getMyIP(), TCP_PORT)

main()
