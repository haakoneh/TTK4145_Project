import json
from MessageEncoder import *

class MessageSender:
	def __init__(self, connection):
		self.connection = connection
		self.encoder = MessageEncoder()

	def sendMessage(self, msgType, payload):
		content = self.encoder.encode(msgType, payload)
		data = {'msgType': msgType, 'content': content}
		self.connection.send(json.dumps(data))