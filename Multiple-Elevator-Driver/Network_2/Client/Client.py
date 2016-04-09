# -*- coding: utf-8 -*-
import socket
import json
import time
from MessageReceiver import MessageReceiver
from runPythonScript import *
from UDP_broadcaster import *

class Client:
	
	def __init__(self, host, serverPort):
		self.host = host
		self.serverPort = serverPort
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((self.host,self.serverPort))
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

	

if __name__ == '__main__':
	UDP_Check = UDP_broadcaster()
	if UDP_Check.broadcaster():
		print 'We are slaves'
	else: 
		print 'We are masters'
		runPythonScript('test.py')

	#client = Client('localhost', 9998)
	#client.receiveMessage()
	#while True:
	#	logout = client.rawInput()
	#	client.send()
	#	if(logout == "logout"):
	#		time.sleep(0.5)
	#		client.disconnect()
	#		break
	#	time.sleep(0.4)
