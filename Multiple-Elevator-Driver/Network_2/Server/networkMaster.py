# -*- coding: utf-8 -*-
from threading import Thread, Lock
import SocketServer
from socket import *
import json
import time


ipAdresses = []
connections = []
elevConnections = []		#list of elevators, the index will be the ID of the respecitve elevator
elevID = 0 					#incremental ID for elevators, might need mutex, since it's changed in threads

class ClientHandler(Thread):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	def __init__(self, connection,addr):
		super(ClientHandler, self).__init__()
		self.connection = connection
		self.addr = addr

		elevators[elevID] 
		elevID += 1
	
	def run(self):
		
		self.userName = ''
		self.help = 'login <username> - log in with the given username\nlogout - log out\nmsg <message> - send message\nnames - list users in chat\nhelp - view help text'
		while True:
			try:
				receivedString = self.connection.recv(4096)
			except:
				try:
					userNames.remove(self.userName)
					connections.remove(self.connection)
				except:
					pass
		
			connections.append(self.connection)
			elevators
			ipAdresses.append(self.addr[0])

			if(receivedString):
				# for con in connections:
				# 	print con
				for elev in elevConnections:
					print elev

				print receivedString
			else:
				continue

			




if __name__ == "__main__":
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations are necessary
	"""
	HOST, PORT = 'localhost', 9998
	print 'Server running...'
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',PORT))
	serverSocket.listen(100)


	while True:
		connection, addr = serverSocket.accept()
		ClientHandler(connection, addr).start()
