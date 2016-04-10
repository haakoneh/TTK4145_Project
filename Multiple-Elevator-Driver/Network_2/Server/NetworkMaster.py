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
		super(ClientHandler, self).__init__()
		global IDCounter, connections
		self.connection = connection
		self.addr = addr
		self.ID = 0
		IDCounter += 1
		connections.append(self.connection)
		
	
	def run(self):
		
		self.userName = ''
		self.help = 'login <username> - log in with the given username\nlogout - log out\nmsg <message> - send message\nnames - list users in chat\nhelp - view help text'
		while True:
			try:
				receivedString = self.connection.recv(4096)
			except select.error:
				try:
					print 'connection lost'
					userNames.remove(self.userName)
					connections.remove(self.connection)
				except:
					pass

			if(receivedString):
				# for con in connections:
				# 	print con
				for elev in connections:
					print elev

				print receivedString
			else:
				continue

			self.connection.send("ping")
			time.sleep(0.1)

			

def starter():
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations are necessary
	"""
	HOST, PORT = getIP.getMyIP(), 9998
	print 'Server running...'
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind((HOST, PORT))
	serverSocket.listen(100)


	while True:
		connection, addr = serverSocket.accept()
		ClientHandler(connection, addr).start()
