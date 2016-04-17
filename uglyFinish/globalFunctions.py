import socket
from subprocess import check_output
import os
from time import sleep
from threading import Timer
import thread


def getMyIP(): 
	try: 
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("gmail.com",80))
		IP = s.getsockname()[0]
		s.close()
		return IP
	except:
		return 'localhost'


def runPythonScript(filename):

	commandString = "gnome-terminal -e 'python " + str(filename) + "'"
	os.system(commandString)

def runSubprocess(filename):
	check_output("gnome-terminal -e 'python " + str(filename) + "'", shell = True)

def connectionLost(myIP):
	if getMyIP() != myIP:
		return True
	else : 
		return False