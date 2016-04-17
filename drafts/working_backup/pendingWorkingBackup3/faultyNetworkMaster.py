# -*- coding: utf-8 -*-
from threading import Thread, Lock
import SocketServer
# from socket import *
import socket
import json
import time
from globalFunctions import * 
import select
from MessageFormatHandler import *
from MessageFormatHandler import MessageParser
from cost import *

NR_Floors = 4

ipAdresses = []
connections = []
stateList = []
stateDict = {}
IDCounter = 0
allMsgBuffers = {}
pendingRequests =[]

#elevConnections = []		#list of elevators, the index will be the ID of the respecitve elevator

printString = ""

class SlaveHandler(Thread):
	"""
	This is the SlaveHandler class. Everytime a new Slave connects to the
	server, a new SlaveHandler object will be created. This class represents
	only connected Slaves, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	def __init__(self, connection,addr, lock):


		print "New Slave handler made"
		super(SlaveHandler, self).__init__()
		global IDCounter, connections, stateDict, NR_Floors, allMsgBuffers, pendingRequests
		self.connection = connection
		self.addr = addr
		self.slaveID = -1
		connections.append(self.connection)
		self.updateID()

		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()
		self.msgBuffer = []
		self.lock = lock

		self.stayAlive = True #should be set to false at removeSlave

		allMsgBuffers[str(self.slaveID)] = []
		#used for allMsgBuffers, maybe it should be used for stateDict and connections too
		
	def msgToAllBuffers(self, msg):
		for msgBuffer in allMsgBuffers:
			allMsgBuffers[msgBuffer].append(msg)
		
	def pingToSlave(self):

		id_ping = self.messageEncoder.encode('elev_id', self.getID())
		self.connection.send(id_ping)
	
	def getID(self):
		return self.slaveID


	def sendRequestToBestSlave(self, request):
		global printString
		bestElevator = -1

		lowestCost = NR_Floors*2 #should be the maximum cost
		for elevator in stateDict:
			cost = calculateCost(stateDict[elevator], request)
			if elevator >= 0:
				if(cost < lowestCost):
					lowestCost = cost
					bestElevator = elevator

		printString += "\nBest elevator: {}\tcost: {}".format(bestElevator, cost)

		msg = self.messageEncoder.encode('request', request)


		"""send request to the most suited elevator's buffer"""
		self.lock.acquire()
		if not str(bestElevator) in allMsgBuffers:
			printString += "\n" +   "new entry in allMsgBuffers"
			allMsgBuffers[str(bestElevator)] = [msg]
		else:
			printString += "\n" +   "trying to append to allMsgBuffers: {}".format(msg)
			printString += "\nallMsgbuffers: {}\nallMsgbuffers['elevator']{}".format(allMsgBuffers,allMsgBuffers[str(bestElevator)])
			if not msg in allMsgBuffers[str(bestElevator)]:
				print "in the if statement, about to append"
				allMsgBuffers[str(bestElevator)].append(msg)
				print "failed to append request, even though it wasn't already in the buffer"
			else:
				printString += "\n request: {} not added".format(request)
			print "after if statement"

		self.lock.release()
		return printString

	def updateID(self):
		global printString
		try:
			self.slaveID = connections.index(self.connection)
		except:
			print "slave not found in connections list"
			self.slaveID = -1
		printString +=  "\nID ipdated to: {}".format(self.slaveID)


	def addPendingGlobalRequest(self, request):
		self.lock.acquire()
		if(request not in pendingRequests):
			pendingRequests.append(request)
		self.lock.release()
	def removePendingGlobalRequst(self, request):
		self.lock.acquire()
		if(request in pendingRequests):
			pendingRequests.remove(request)
		self.lock.release()
	def broadcastPendingRequests(self):
		self.lock.acquire()
		#msg = {"msgType": "pendingRequests", "content": pendingRequests}	
		msg = self.messageEncoder.encode('pendingRequests', pendingRequests)
		self.msgToAllBuffers(str(msg))
		self.lock.release()

	def removeSlave(self):
		global printString
		#print printString
		print "\t\t\tRemoving slave nr: {}".format(self.getID())

		self.lock.acquire()
		del allMsgBuffers[str(self.getID())]
		del stateDict[(str(self.slaveID))]
		connections.remove(self.connection)
		self.lock.release()
		print "\t\t\tRemoving should be complete, id set to -1"

		self.slaveID = -1

	def getMsgBuffer(self):
		#returns none if the msg buffer has been removed
		default = " "
		return allMsgBuffers.get(str(self.slaveID), default)


	def run(self):
		prevPrintString = ""

		
		while True:
			printString = ""
			self.updateID()
			try:
				receivedString = self.connection.recv(4096)
			except:
				printString += "Failed to recieve from slave nr{}: ".format(self.getID())
				print printString
				self.removeSlave()
				break

			if(receivedString):
				try:
					message = json.loads(receivedString)
				except:
					printString += "\njson.loads fail\n with: {}".format(receivedString)
					print printString
					self.removeSlave()
					break
			else:
				printString += "\n Received nothing (probably empty pending list)"

			printString += "\n" +   'message' + str(message)



			if message['msgType'] == 'state':
				self.lock.acquire()
				stateDict[str(self.getID())] = self.messageParser.parse(receivedString)
				self.lock.release()
				printString += "\n" +   'stateDict: ' + str(stateDict)

			elif message['msgType'] == 'ping':
				ping = self.messageParser.parse(receivedString)
				pass

			elif message['msgType'] == 'request':
				request = self.messageParser.parse(receivedString)
				printString += "request = {}".format(request)
				printString = self.sendRequestToBestSlave(request)
#new stuff added here
###################
				# print "adding pending request"
				# self.addPendingGlobalRequest(request)
				# print "adding pendingRequests to all buffers"
				# self.broadcastPendingRequests()
###################

			printString += "\n" +   "Self IP: {}".format(getMyIP())#store this on setup instead
			printString += "\n" + str(self.getID()) + " buffer contains: " + str(self.getMsgBuffer())
			printString += "\n" "allMsgBuffers: {}".format(allMsgBuffers)

			if str(self.getID()) in allMsgBuffers:
				if allMsgBuffers[str(self.getID())]:
					printString += "\n" +   "***Sending request to slave nr: {}\trequest: {}".format(self.getID(), allMsgBuffers[str(self.getID())])
					sendstuff = allMsgBuffers[str(self.getID())].pop(0)
					printString += "\n" +   "***********sendstuff: {}".format(sendstuff)
			
					self.connection.send(sendstuff)
				
					printString += "Failed to send sendstuff: {}".format(sendstuff)
					print printString
					self.removeSlave()
					break

				else:
					printString += "\n" +   "Pinging to slave"
					self.pingToSlave()
			else:
				print "XXXdead slave: breakXXX"
				break
			# except:
			# 	"exception caught"

			printString += "\n" +   "end of master loop"

			if printString != prevPrintString:
				print printString
				prevPrintString = printString

			time.sleep(0.1)

def starter():

	HOST, PORT = getMyIP(), 50505
	print 'networkMaster running...'

	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.bind((HOST, PORT))
	
	serverSocket.listen(100)

	lock = Lock()#used to lock global variables

	while True:
		connection, addr = serverSocket.accept()
		SlaveHandler(connection, addr, lock).start()
