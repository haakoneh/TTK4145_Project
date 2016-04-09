# -*- coding: utf-8 -*-
from threading import Thread
import json

class MessageReceiver(Thread):
	"""
	This is the message receiver class. The class inherits Thread, something that
	is necessary to make the MessageReceiver start a new thread, and it allows
	the chat client to both send and receive messages at the same time
	"""

	def __init__(self, connection):
		super(MessageReceiver, self).__init__()
		self.connection = connection
		self.daemon = True
		
	def run(self):
		while True:
			try:
				data = self.connection.recv(4096)
			except:
				print 'Connection lost'
				break
			try:
				jsonObject = json.loads(data)
			except:
				break
			if 'sender' in jsonObject:
				print jsonObject['sender']
			if 'timestamp' in jsonObject:
				print jsonObject['timestamp']
			if 'response' in jsonObject:
				print jsonObject['response']
			if 'content' in jsonObject:
				print jsonObject['content']
	
	def stop(self):
		self.daemon = False