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

#elevConnections = []		#list of elevators, the index will be the ID of the respecitve elevator

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
		global IDCounter, connections, stateDict, NR_Floors, allMsgBuffers
		self.connection = connection
		self.addr = addr
		connections.append(self.connection)
		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()
		self.msgBuffer = []
		self.lock = lock

		allMsgBuffers[str(self.slaveID())] = []
		#used for allMsgBuffers, maybe it should be used for stateDict and connections too
		

		
	def pingToSlave(self):

		id_ping = self.messageEncoder.encode('elev_id', self.slaveID())
		self.connection.send(id_ping)
	
	def slaveID(self):
		return connections.index(self.connection)

	def run(self):
		prevPrintString = ""

		
		while True:
			printString = ""
			try:
				receivedString = self.connection.recv(4096)
			except:
				printString += "\n" +   'timeout'
				self.lock.acquire()
				connections.remove(self.connection)
				del allMsgBuffers[self.slaveID()]
				self.lock.release()

			try:
				message = json.loads(receivedString)
			except:
				printString += "json.loads fail"
			printString += "\n" +   'message' + str( message)



			if message['msgType'] == 'state':
				self.lock.acquire()
				stateDict[str(self.slaveID())] = self.messageParser.parse(receivedString)
				self.lock.release()
				printString += "\n" +   'stateDict: ' + str(stateDict)

			elif message['msgType'] == 'ping':
				ping = self.messageParser.parse(receivedString)
				pass

			elif message['msgType'] == 'request':
				request = self.messageParser.parse(receivedString)

				bestElevator = -1


				lowestCost = NR_Floors*2 #should be the maximum cost
				for elevator in stateDict:
					cost = calculateCost(stateDict[elevator], request)
					printString += "\n" +   "cost: {}".format(cost)
					if(cost < lowestCost):
						lowestCost = cost
						bestElevator = elevator

				msg = self.messageEncoder.encode('request', request)

				"""send request to the most suited elevator's buffer"""
				self.lock.acquire()
				

				
				if not str(bestElevator) in allMsgBuffers:
					printString += "\n" +   "new entry in allMsgBuffers"
					allMsgBuffers[str(bestElevator)] = [msg]
				else:
					printString += "\n" +   "trying to append to allMsgBuffers"
					if not msg in allMsgBuffers[str(bestElevator)]:
						allMsgBuffers[str(bestElevator)].append(msg)
				printString += "\n" +   "allMsgBuffers: {}".format(allMsgBuffers)

				printString += "\n" +   "\n**********\nrequest appended to bestElevator: {}\n******\n".format(bestElevator)
				

				self.lock.release()

		

			printString += "\n" +   "Self IP: {}".format(getMyIP())#store this on setup instead
			printString += "\n" +   "*******allMsgBuffers: \n{}\n*******".format(allMsgBuffers) 
			# try:
			printString += "\n" +   "allMsgBuffers[ßelf]: {}".format(allMsgBuffers[str(self.slaveID())])
			if allMsgBuffers[str(self.slaveID())]:
				printString += "\n" +   "***Sending request to slave***: {}".format(allMsgBuffers[str(self.slaveID())])
				sendstuff = allMsgBuffers[str(self.slaveID())].pop(0)
				printString += "\n" +   "***********sendstuff: {}".format(sendstuff)
				self.connection.send(sendstuff)

			else:
				printString += "\n" +   "Pinging to slave"
				self.pingToSlave()
			# except:
			# 	"exception caught"
				pass
			printString += "\n" +   "end of master loop"

			if printString != prevPrintString:
				print printString
				prevPrintString = printString

			time.sleep(0.1)

def starter():

	HOST, PORT = getMyIP(), 40404
	print 'networkMaster running...'

	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.bind((HOST, PORT))
	
	serverSocket.listen(100)

	lock = Lock()#used to lock global variables

	while True:
		connection, addr = serverSocket.accept()
		SlaveHandler(connection, addr, lock).start()
