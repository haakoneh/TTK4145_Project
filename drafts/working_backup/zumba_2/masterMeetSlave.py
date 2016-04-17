from globalFunctions import * 
import time
from socket import *
from MessageFormatHandler import *


class MasterSlaveSeeker():
	def __init__(self):

		self.nodeNr = 0		#this is changed unless this is the first active node
		self.bufferSize = 4096
		self.IP = getMyIP()
		self.udpPort = 45454
		print self.udpPort
		
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

		#deliberately set without timeout
		# self.bcListener = socket(AF_INET, SOCK_DGRAM)
		# self.bcListener.bind(('', self.udpPort2))
		self.bcReplyMsg = "You're my slave now ;P"
		self.bcMsgEncoded = self.messageEncoder.encode('udp', self.bcMsg)

	#rename
	def findMaster(self):
		for i in range(0,5):

			self.broadcastSock.sendto(self.bcMsgEncoded , ('255.255.255.255', self.udpPort))
			time.sleep(0.1)
			recvMsg, addr = self.udpSock.recvfrom(self.bufferSize)
			decMsg = self.messageParser.parse(recvMsg)
			if(addr[0] == self.IP and decMsg == self.bcMsg):
				print 'echo from IP: {}\tport: {}'.format(self.IP,self.udpPort)
				
			else:
				# if(self.parser.parse(recvMsg) == 'master_confirmed'):
				if(decMsg == self.bcReplyMsg):
					print "Master found, with IP: " + str(addr[0])
					return addr[0]
				else:
					print decMsg
		print "No masters found"
		return False

	#called by master. If it gets a message, it replies "i'm master, shut up"
	#might wanna make it utilize MessageParser for code aesthetics
	def replyToSlaves(self):
		"looking for slaves"

		while True:
			#print "Looking for potential slaves"
			try:
				recvMsg, addr = self.udpSock.recvfrom(self.bufferSize)
				decMsg = self.messageParser.parse(recvMsg)
				print "Recieved: {}".format(decMsg)
			except timeout:
				continue
			if(decMsg == self.bcMsg):
				udpMsg = self.messageEncoder.encode('udp', self.bcReplyMsg)
				self.udpSock.sendto(udpMsg,(addr[0], self.udpPort))
				print "Sending to IP: {}\tPort: {}".format(addr[0], self.udpPort)
				#tell the broadcaster that you're the master


#udp = UDP_broadcaster()
#print 'broadcast: ' + str(udp.broadcaster())