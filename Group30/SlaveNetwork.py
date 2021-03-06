# -*- coding: utf-8 -*-
import socket
import json
import time
import errno
import sys
import threading
#from watchdog import Watchdog
import GlobalFunctions
from MessageFormatHandler import *


class SlaveNetwork:
	
	def __init__(self, host, serverPort):
		self.host = host
		self.serverPort = serverPort
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.settimeout(1)
		try:
			self.connection.connect((self.host, self.serverPort))
		except:
			print 'connection refused'

		self.ID = -1
		self.jsonObject = None
		self.alive = True
		self.messageBuffer = []
		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()
		self.timeoutCounter = 0
		

	def disconnect(self):
		self.connection.close()
		try:
			self.messageReceiver.stop()
		except:
			pass
	
	

	def receive(self):
		try:
			tempMsg = self.connection.recv(4096)
			return tempMsg
		except socket.timeout:
			self.timeoutCounter += 1
			if self.timeoutCounter > 3:
				print "Master timed out: ", self.timeoutCounter
				self.handleLossOfMaster()
		except:

			self.timeoutCounter += 1
			if self.timeoutCounter > 3:
				print "Master timed out: ", self.timeoutCounter
				self.handleLossOfMaster()
			print 'Unkown error, timeoutCounter: ' + str(self.timeoutCounter)
			return -1

	def send(self, msg):
		try:
			self.connection.send(msg)
			self.timeoutCounter = 0
		except socket.timeout:
				self.timeoutCounter += 1
				if self.timeoutCounter > 3:
					print "Master timed out: ", self.timeoutCounter
					self.handleLossOfMaster()
		except:
			self.timeoutCounter += 1
			if self.timeoutCounter > 3:
				print "Master timed out: ", self.timeoutCounter
				self.alive = False
			# 		self.handleLossOfMaster()
			# self.handleLossOfMaster()
			print 'Unkown error, timeoutCounter: ' + str(self.timeoutCounter)
			return -1
	def sendPing(self):
		#print 'self_ID: ' + str(self.ID)
		self.send(self.messageEncoder.encode('ping', 'slavePing:' + str(self.ID)))

	def handleLossOfMaster(self):
		time.sleep(abs((int(self.ID)) * 2))
		self.alive = False

	def setSlaveID(self, newID):
		self.ID = newID

	def getSlaveID(self):
		return self.ID

