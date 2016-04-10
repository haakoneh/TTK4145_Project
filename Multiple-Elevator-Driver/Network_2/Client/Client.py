# -*- coding: utf-8 -*-
import socket
import json
import time
#import imp
from MessageReceiver import MessageReceiver
#MessageReceiver = imp.load_source('MessageReceiver', '/MessageReceiver.py')


class Client:
	
	def __init__(self, host, serverPort):
		self.host = host
		self.serverPort = serverPort
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.settimeout(0.2)
		self.connection.connect((self.host, self.serverPort))
		self.jsonObject = None

	def disconnect(self):
		self.connection.close()
		try:
			self.messageReceiver.stop()
		except:
			pass
	def rawInput(self):
		request = raw_input("Request type: ")
		if(request in ["login", "msg"]):	
			content = raw_input("Content: ")
			self.jsonObject = json.dumps({'request': request, 'content': content}, indent=4)
		else:
			self.jsonObject = json.dumps({'request': request}, indent=4)
		return request


	def receiveMessage(self):
		self.messageReceiver = MessageReceiver(self.connection)
		self.messageReceiver.start()

	def send(self):
		self.connection.send(self.jsonObject)


def run(serverIP):
	client = Client(serverIP, 9998)
	
	while True:
		try:
			data = client.connection.recv(4096)
			print data
		except socket.timeout:
			print "timeout"

		
		client.connection.send("Slave ping")
		time.sleep(0.4)