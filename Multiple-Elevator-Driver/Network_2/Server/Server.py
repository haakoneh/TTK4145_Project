# -*- coding: utf-8 -*-
from threading import Thread, Lock
import SocketServer
from socket import *
import json
import time

messageQueue = []
history = []
userNames = []
ipAdresses = []
blackList = []
banList = []
counter = 0
connections = []



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

				break
			# TODO: Add handling of received payload from client
			msgTimestamp = time.ctime()
			jsonParser = json.loads(receivedString)
			clientRequest = jsonParser['request']
			if clientRequest == 'login':
				if(self.userName != ''):
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'response': 'Error', 'content': 'Allready logged in'}, indent=4)
					self.connection.send(jsonSender)
				else:
					if jsonParser['content'] in userNames:
						jsonSender = json.dumps({'timestamp': msgTimestamp, 'response': 'Error', 'content': 'Username already exists'}, indent=4)
						self.connection.send(jsonSender)
					else:
						validMessage = 1
						for c in jsonParser['content']:
							if ord(c) > 122 or ord(c) < 48:
								jsonSender = json.dumps({'timestamp': msgTimestamp, 'response': 'Error', 'content': 'Invalid username'}, indent=4)
								self.connection.send(jsonSender)
								validMessage = 0
								break
						if validMessage == 1:
							if(jsonParser['content'] in blackList):
								jsonSender = json.dumps({'timestamp': msgTimestamp, 'sender': "From: Admin", 'response': 'error', 'content': 'Blacklisted username'}, indent=4)
								self.connection.send(jsonSender)
							else:
								jsonSender = json.dumps({'timestamp': msgTimestamp, 'sender':jsonParser['content'] , 'content': 'Succesfully logged in'}, indent=4)
								self.connection.send(jsonSender)
								userNames.append(jsonParser['content'])
								connections.append(self.connection)
								ipAdresses.append(self.addr[0])
								self.userName = jsonParser['content']
								if history:
									histories = "\n".join(history)
									jsonSender = json.dumps({'timestamp': msgTimestamp ,'response': 'histories', 'content': histories}, indent=4)
									self.connection.send(jsonSender)	

				history.append(jsonSender)
			elif clientRequest == 'logout':
				if self.userName in userNames:
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'content': 'Succesfully logged out'}, indent=4)
					self.connection.send(jsonSender);
					history.append(jsonSender)
					userNames.pop(userNames.index(self.userName))
					ipAdresses.remove(self.addr[0])
					self.connection.close()
					connections.remove(self.connection)
					break
			elif clientRequest == 'msg':
				if(self.userName not in userNames):
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'response': 'Error', 'content': 'Not logged in'}, indent=4)
					self.connection.send(jsonSender)
				else:
					#TODO: counter should obviously be an int, but the logic to find it might be hard
					
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'sender':self.userName, 'response': 'Message', 'content': jsonParser['content']}, indent=4)
					print jsonSender
					print 'Ban: '
					for connection in connections:
						if connection != self.connection:
							connection.send(jsonSender)
				history.append(jsonSender)
			elif clientRequest == 'names':
				if self.userName in userNames:
					allNames = "\n".join(userNames)
					jsonSender = json.dumps({'timestamp': msgTimestamp ,'response': 'names', 'content': allNames}, indent=4)
					self.connection.send(jsonSender)
					history.append(jsonSender)
				else:
					jsonSender = json.dumps({'timestamp': msgTimestamp , 'content': 'Not logged in'}, indent=4)
					self.connection.send(jsonSender)
			elif clientRequest == 'help':
				jsonSender = json.dumps({'timestamp': msgTimestamp ,'response': 'help', 'content': self.help}, indent=4)
				self.connection.send(jsonSender)
			elif clientRequest == 'history':
				for histories in history:
					self.connection.send(histories)
					time.sleep(0.3)
			else:
				jsonSender = json.dumps({'timestamp': msgTimestamp ,'response': 'List of accepted inputs ', 'content': self.help}, indent=4)
				self.connection.send(jsonSender)



def ban():
	while True:
		ban = raw_input("Ban: ")
		if ban == 'Ban list':
			print blackList
		elif ban == 'Unban':
			bannedUser = raw_input("banned username: ")
			if bannedUser in blackList:
				indexOf = blackList.index(bannedUser)
				blackList.remove(bannedUser)
				banList.pop(indexOf)
		else:
			try:
				index = userNames.index(ban)
				tempCon = connections.pop(index)
				tempIp = ipAdresses.pop(index)
				banList.append(tempIp)
				blackList.append(ban)
				jsonSender = json.dumps({'timestamp': time.ctime(), 'content': "You've been banned"}, indent=4)
				tempCon.send(jsonSender);
				history.append(jsonSender)
				userNames.pop(index)
				tempCon.close()
			except:
				print 'Not a user'

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

	thread = Thread(target = ban, args = (), )
	thread.start()

	while True:
		connection, addr = serverSocket.accept()
		if addr[0] in banList:
			jsonSender = json.dumps({'timestamp': time.ctime(), 'content': "You've IP been banned"}, indent=4)
			connection.send(jsonSender)
			connection.close()
		ClientHandler(connection, addr).start()


