# -*- coding: utf-8 -*-
import socket
import json
import time
import errno
import sys
#import imp
from MessageReceiver import MessageReceiver
#MessageReceiver = imp.load_source('MessageReceiver', '/MessageReceiver.py')


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


	def run(self):
		print "making client"
		timeoutCounter = 0
		while True:
			try:
				data = self.connection.recv(4096)
				if data != self.ID:
					self.ID = data	#needs a format check
				print data

			

				#master always times out once at initialization for some reason. Quick fix:

				timeoutCounter += 1
				if timeoutCounter > 1:
					print "Master timed out"
					#master is most likely dead: take over

					if(self.ID == 0):
						#you're the masters favourite slave. Something is probably wrong with you: kill yourself
						print "Your master died"
						return "Your master died"

					if(self.ID == 1):
						#Dead master: Take over
						#restart as master
						print "Your master died"
						return "Distant master died"

						self.disconnect()
					else:
						#restart as slave

						pass
					return "timeout"
			except:
				# if e.errno == errno.EPIPE:
				print "broken pipe"

			# except socket.error, e:
			# 	if isinstance(e.args, tuple):
			# 		print "errno is %d" % e[0]
			# 		if e[0] == errno.EPIPE:
			# 			# remote peer disconnected
			# 			print "Detected remote disconnect"
			# 		else:
			# 			# determine and handle different error
			# 			pass
			



			try:
				self.connection.send("Slave ping: {}".format(self.ID))
			except:
				print "broken pipe"
			time.sleep(0.4)