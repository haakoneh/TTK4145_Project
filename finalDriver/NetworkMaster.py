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
#elevConnections = []		#list of elevators, the index will be the ID of the respecitve elevator

class SlaveHandler(Thread):
	"""
	This is the SlaveHandler class. Everytime a new Slave connects to the
	server, a new SlaveHandler object will be created. This class represents
	only connected Slaves, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	def __init__(self, connection,addr):
		print "New Slave handler made"
		super(SlaveHandler, self).__init__()
		global IDCounter, connections, stateDict, NR_Floors
		self.connection = connection
		self.addr = addr
		connections.append(self.connection)
		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()
		self.msgBuffer = []
		
	def pingToSlave(self):
		print "pinging to slave"
		id_ping = self.messageEncoder.encode('elev_id', self.slaveID())
		self.connection.send(id_ping)
	
	def slaveID(self):
		return connections.index(self.connection)

	def run(self):
		
		while True:
			try:
				receivedString = self.connection.recv(4096)
			except:
				print 'no msg from Slave'
				connections.remove(self.connection)

			# print 'recievedString: ' + str(receivedString)
			# decodedMsg = self.messageParser.parse(receivedString)
			
			#print 'stringer' + str(decodedMsg)

			message = json.loads(receivedString)
			print 'message' + str( message)

			bestElevator = -1


			if message['msgType'] == 'state':
				stateDict[str(self.slaveID())] = self.messageParser.parse(receivedString)
				print 'stateDict: ' + str(stateDict)

			elif message['msgType'] == 'ping':
				ping = self.messageParser.parse(receivedString)
				pass

			elif message['msgType'] == 'request':
				request = self.messageParser.parse(receivedString)

				lowestCost = NR_Floors*2 #should be the maximum cost
				for elevator in stateDict:
					cost = calculateCost(stateDict[elevator], request)
					print "cost: ", cost
					if(cost < lowestCost):
						lowestCost = cost
						bestElevator = elevator
				msg = self.messageEncoder.encode('request', request)
				if not msg in self.msgBuffer:
					self.msgBuffer.append(msg)

				print 'bestElevator: ' + str(bestElevator)

			print "Self IP: ", getMyIP()#store this on setup instead

			try:
				if self.msgBuffer:
					self.connection.send(self.msgBuffer.pop(0))
				else:
					self.pingToSlave()
			except:
				pass
			print "end of master loop"
			time.sleep(0.1)

			

def starter():

	HOST, PORT = getMyIP(), 40404
	print 'networkMaster running...'

	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.bind((HOST, PORT))
	serverSocket.listen(100)


	while True:
		connection, addr = serverSocket.accept()
		SlaveHandler(connection, addr).start()
