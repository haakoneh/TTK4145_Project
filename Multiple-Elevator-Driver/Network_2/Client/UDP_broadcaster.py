from getIP import * 
from MessageParser import *
import time
from socket import *

class UDP_broadcaster():
	def __init__(self):
		self.nodeNr = 0		#this is changed unless this is the first active node
		self.IP = getMyIP()
		self.udpPort = 54545
		
		self.broadcastSock = socket(AF_INET, SOCK_DGRAM)
		self.broadcastSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.broadcastSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		

		self.udpSock = socket(AF_INET, SOCK_DGRAM)
		self.udpSock.bind(('', self.udpPort))
		self.udpSock.settimeout(0.2)

	def broadcaster(self):
		msg = 'hei'
		self.parser = MessageParser()
		for i in range(0,5):
			self.broadcastSock.sendto(msg, ('255.255.255.255', self.udpPort))
			time.sleep(0.1)
			recvMsg, addr = self.udpSock.recvfrom(4096)
			if(addr[0] == self.IP):
				print 'echo'
				pass
			else:
				if(self.parser.parse(recvMsg) == 'master_confirmed'):
					return True
		return False

#udp = UDP_broadcaster()
#print 'broadcast: ' + str(udp.broadcaster())