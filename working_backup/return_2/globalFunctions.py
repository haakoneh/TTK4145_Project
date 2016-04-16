import socket
from subprocess import check_output
import os
from time import sleep
from threading import Timer
import thread


def getMyIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	IP = s.getsockname()[0]
	s.close()
	return IP


def runPythonScript(filename):

	commandString = "gnome-terminal -e 'python " + str(filename) + "'"
	os.system(commandString)

def runSubprocess(filename):
	check_output("gnome-terminal -e 'python " + str(filename) + "'", shell = True)