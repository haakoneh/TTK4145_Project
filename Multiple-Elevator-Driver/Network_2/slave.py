from runPythonScript import *
import sys
import threading
from getIP import *

sys.path.insert(0, 'Client/')
import Client

# def run():
# 	runPythonScript("Client.py")

 # if timeout:
	# if id == 1(or 0):
	# 	# become master



def run(masterIP):
	print "New slave"
	client = Client.Client(masterIP, 9998)
	slaveThread = threading.Thread(target = client.run)
	slaveThread.start()


	# if global killthread == True:
	# 	kill thread


# if(Client.run() == "master dead"):




