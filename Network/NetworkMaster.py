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



ipAdresses = []
connections = []
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
		global IDCounter, connections
		self.connection = connection
		self.addr = addr
		connections.append(self.connection)
		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()
		
	def pingToSlave(self):
		id_ping = self.messageEncoder.encode('elev_id', self.slaveID())
		self.connection.send(id_ping)
	
	def slaveID(self):
		return connections.index(self.connection)

	def run(self):
		
		while True:
			try:
				receivedString = self.connection.recv(4096)
			except:
				#temorarily assuming broken pipe error
				#Remove connection from list, maybe thread seppuku
				connections.remove(self.connection)

			# print 'recievedString: ' + str(receivedString)
			stringer = self.messageParser.parse(receivedString)
			if not stringer:
				break
			
			print stringer

			print "Self IP: ", getMyIP()


			#self.connection.send("master ping")
			try:
				self.pingToSlave()
			except:
				pass

			time.sleep(0.1)

			

def starter():

	HOST, PORT = getMyIP(), 9998
	print 'networkMaster running...'

	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.bind((HOST, PORT))
	serverSocket.listen(100)


	while True:
		connection, addr = serverSocket.accept()
		SlaveHandler(connection, addr).start()
