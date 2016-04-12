# -*- coding: utf-8 -*-
import socket
import json
import time
import errno
import sys
#import imp
from MessageReceiver import MessageReceiver
import threading
#MessageReceiver = imp.load_source('MessageReceiver', '/MessageReceiver.py')
#from main import *


class Client:
	
	def __init__(self, host, serverPort):
		print "New client instance"
		self.host = host
		self.serverPort = serverPort
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.settimeout(0.2)
		self.connection.connect((self.host, self.serverPort))
		self.ID = -1
		self.jsonObject = None

		self.alive = True

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

	def handleLossOfMaster(self):

		if(self.ID == 0):
			print "Your master died"
			#restart as slave


		if(self.ID >= 1):
			#Dead master: Take over
			#restart as master
			print "Distant master died: Rise to power"
			time.sleep(1)
			print "acive count: ", threading.activeCount()
			print "enumerate: ", threading.enumerate()

			self.alive = False
			#self.disconnect()

		else:
			#restart as slave
			print "Distant master died find new master"
			self.alive = False



	def run(self):
		print "making client"
		timeoutCounter = 0
		while self.alive:
			try:
				data = self.connection.recv(4096)
				if data != self.ID:
					self.ID = data	#needs a format check
				print data

			#master always times out once at initialization for some reason. Quick fix:
			except socket.timeout:
				timeoutCounter += 1
				if timeoutCounter > 1:
					print "Master timed out: ", timeoutCounter
					#master is most likely dead: take over

					self.handleLossOfMaster()

			except:
			
				print "broken pipe"
				self.handleLossOfMaster()

			try:
				self.connection.send("Slave ping: {}".format(self.ID))
			except:
				print "broken pipe"
				#assume master dead:
				self.handleLossOfMaster()




			time.sleep(0.4)

		#ugly ass fix
		#main()