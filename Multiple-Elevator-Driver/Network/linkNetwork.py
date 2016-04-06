from socket import *
from getIP import * 
import time
#high level pseudocode

#Same procedure for all elevators
#setup() assumes no current connections



class LinkNode():
	def __init__(self):

		self.nodeNr = 0		#this is changed unless this is the first active node
		self.IP = getMyIP()
		self.udpPort = 30000
		self.tcpPort = 50001

		#self.tcpSocket = socket.socket(AF_INET, SOCK_STREAM)

		self.broadcastSock = socket.socket(AF_INET, SOCK_DGRAM)
		self.broadcastSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

		self.udpRecvSock = socket.socket(AF_INET, SOCK_DGRAM)
		self.udpRecvSock.bind(("", self.udpPort))



		recvMsg = ""

		while True:

			#assuming no connections
			self.broadcast("seekingConnections")
			print "Broadcast done, waiting to recieve"

			recvMsg, addr = self.udpRecvSock.recvfrom(1024) #remember timeout

			if(recvMsg == "seekingConnections"):
				if(addr[0] == self.IP):
					pass
				else:
					print "Recieved: {}\tFrom: {}".format(recvMsg, addr)

				#forwardLinkWith(addr)	#either TCP connection, or UDP "connection"
				#backwardLinkWith(addr)	
				#return
			elif(recvMsg == "linkWithMe"):
				pass
			elif(recvMsg == "alreadyLinked"):
				enterLinkNetwork()
				return

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
		self.broadcastSock.sendto(msg, ('<broadcast>', self.udpPort))

	def run(self):
		pass


node = LinkNode()