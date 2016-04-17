from GlobalFunctions import * 
import time
from socket import *
from MessageFormatHandler import *


class MasterSlaveSeeker():
	def __init__(self):

		self.nodeNr = 0	
		self.bufferSize = 4096
		self.IP = getMyIP()
		self.udpPort = 45454
		
		self.broadcastSock = socket(AF_INET, SOCK_DGRAM)
		self.broadcastSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.broadcastSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		self.bcMsg = "looking for master"


		self.udpSock = socket(AF_INET, SOCK_DGRAM)
		self.udpSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.udpSock.bind(('', self.udpPort))
		self.udpSock.settimeout(0.2)

		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()

		self.bcReplyMsg = "You're my slave now ;*"
		self.bcMsgEncoded = self.messageEncoder.encode('udp', self.bcMsg)

	#rename
	def findMaster(self):
		for i in range(0,5):
			try:
				self.broadcastSock.sendto(self.bcMsgEncoded , ('255.255.255.255', self.udpPort))
			except:
				self.broadcastSock.sendto(self.bcMsgEncoded , ('localhost', self.udpPort))
			time.sleep(0.1)
			recvMsg, addr = self.udpSock.recvfrom(self.bufferSize)
			decMsg = self.messageParser.parse(recvMsg)

			if(addr[0] == self.IP and decMsg == self.bcMsg):
				print 'echo from IP: {}\tport: {}'.format(self.IP,self.udpPort)
				
			else:
				if(decMsg == self.bcReplyMsg):
					print "Master found, with IP: " + str(addr[0])
					return addr[0]
				else:
					print decMsg
		print "No masters found"
		return False

	def replyToSlaves(self):
		while True:
			try:
				recvMsg, addr = self.udpSock.recvfrom(self.bufferSize)
				decMsg = self.messageParser.parse(recvMsg)
				print "Received: {}".format(decMsg)
			except timeout:
				continue
			if(decMsg == self.bcMsg):
				udpMsg = self.messageEncoder.encode('udp', self.bcReplyMsg)
				self.udpSock.sendto(udpMsg,(addr[0], self.udpPort))
				print "Sending to IP: {}\tPort: {}".format(addr[0], self.udpPort)
