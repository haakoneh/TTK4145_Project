# -*- coding: utf-8 -*-
from threading import Thread, Lock
import SocketServer
from socket import *
import json
import time
import getIP
import select


ipAdresses = []
connections = []
IDCounter = 0
#elevConnections = []		#list of elevators, the index will be the ID of the respecitve elevator

class ClientHandler(Thread):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	def __init__(self, connection,addr):
		print "New client handler made"
		super(ClientHandler, self).__init__()
		global IDCounter, connections
		self.connection = connection
		self.addr = addr
		connections.append(self.connection)
		
	def pingToSlave(self):
		self.connection.send(str(self.slaveID()))
	
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

			print receivedString

			#self.connection.send("master ping")
			self.pingToSlave()

			time.sleep(0.1)

			

def starter():

	HOST, PORT = getIP.getMyIP(), 9998
	print 'networkMaster running...'

	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind((HOST, PORT))
	serverSocket.listen(100)


	while True:
		connection, addr = serverSocket.accept()
		ClientHandler(connection, addr).start()
