#processMonitor
import socket
import slaveNetwork
import master
import time
from globalFunctions import * 
# class Monitor():
# 	def __init__(self, port):
# 		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 		self.sock.bind((UDP_IP, port))
# 		self.sock.settimeout(1)
# 		self.bufferSize = 100

# 	def processDead(self):
# 		#returns true if process is assumed dead

# 		try:
# 			recvData, addr = self.sock.recvfrom(self.bufferSize)
# 		except socket.timeout:
# 			#dead
# 			return True

# 		if()


UDP_IP = "localhost"
UDP_PORT = 30000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1)
bufferSize = 100



def slaveMonitor():
	print "in slaveMonitor"
	while True:
		try:
			try:
				recvData = sock.recvfrom(bufferSize)
				print recvData
			except socket.timeout:
				print "trying to start main.py"
				#runPythonScript("main.py")

				print "timeout"
				break
		except:
			print "Dead"
slaveMonitor()