import json
from MessageEncoder import *

class MessageSender:
	def __init__(self, connection):
		self.connection = connection
		self.encoder = MessageEncoder()

	def sendMessage(self, msgType, payload):
			data = json.dumps(self.encoder.encode(msgType, payload))
			self.connection.send(data)