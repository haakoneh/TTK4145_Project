from socket import *
from getIP import * 
import time
#high level pseudocode

#Same procedure for all elevators
#setup() assumes no current connections


#Maybe move the initial connection code to another function than init file

class LinkNode():
	def __init__(self):

		self.nodeNr = 0		#this is changed unless this is the first active node
		self.IP = getMyIP()
		self.udpPort = 54545
		self.tcpForwardPort = 50001
		self.tcpBackwardPort = 50002

		self.forwardSock = socket.socket(AF_INET, SOCK_STREAM)
		self.forwardSock.bind((self.IP, self.tcpForwardPort))
		self.forwardSock.settimeout(1)
		self.forwardSock.listen(1)


		self.backwardSock = socket.socket(AF_INET, SOCK_STREAM)

		

		self.broadcastSock = socket.socket(AF_INET, SOCK_DGRAM)
		self.broadcastSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.broadcastSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

		self.udpSock = socket.socket(AF_INET, SOCK_DGRAM)
		self.udpSock.bind(('', self.udpPort))



		recvMsg = ""

		while True:

			#assuming no connections
			self.broadcast("seekingConnections")
			print "Broadcast done, waiting to recieve"

			recvMsg, addr = self.udpSock.recvfrom(1024) #remember timeout

			if(recvMsg == "seekingConnections"):
				if(addr[0] == self.IP):
					#message from self
					print self.IP
					pass
				else:#another elevator is seeking a connection, link with it
					print "Recieved: {}\tFrom: {}".format(recvMsg, addr)
					self.backwardSock.connect((addr[0]), self.tcpBackwardPort)

				#forwardLinkWith(addr)	
				#backwardLinkWith(addr)	
				#return
			elif(recvMsg == "linkWithMe"):
				self
				pass
			elif(recvMsg == "alreadyLinked"):
				enterLinkNetwork()
				return
			else:
				print "Unknown msg recieved: " + recvMsg

			print "Before accept"
			try:
				conn, addr = self.forwardSock.accept()
				print "connection made"
			except timeout:
				print "timeout"
			print "After accept"


			time.sleep(1)

	def forwardLinkWith(self, addr):

		#starts by sending link with me
		pass

	def backwardLinkWith(self, addr):
		#starts by sending link with me
		pass

	def enterLinkNetwork(self):
		pass

	def handleMessage(self, msg):
		#do different thing with different messages
		pass

	def broadcast(self, msg):
		self.broadcastSock.sendto(msg, ('255.255.255.255', self.udpPort))

	def udpSendto(self, msg, addr):
		self.udpSock.sendto(msg,addr)


	def run(self):
		pass


node = LinkNode()