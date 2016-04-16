# -*- coding: utf-8 -*-
import socket
import json
import time
import errno
import sys
import threading
#from watchdog import Watchdog
import globalFunctions
from MessageFormatHandler import *


class Slave:
	
	def __init__(self, host, serverPort):
		print "New Slave instance"
		self.host = host
		self.serverPort = serverPort
		print "Trying to connect to: IP: {}\tPort: {}".format(self.host, self.serverPort)
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
		

	def disconnect(self):
		self.connection.close()
		try:
			self.messageReceiver.stop()
		except:
			pass
	
	def receive(self):
		try:
			return self.connection.recv(4096)
		except:
			print 'no msg'
			return -1

	def send(self, msg):
		try:
			self.connection.send(msg)
		except:
			print "sending failed"
	def sendPing(self):
		#print 'self_ID: ' + str(self.ID)
		self.send(self.messageEncoder.encode('ping', 'slavePing:' + str(self.ID)))

	def handleLossOfMaster(self):
		"""master is dead, act acordingly
		Exit the while loop, so connections die and
		stop pinging alive to processMonitor. Which allows  
		external processMonitor to start main.py

		"""
		if self.ID > 0:
			time.sleep((int(self.ID) - 1) * 0.3)

		self.alive = False

	def setSlaveID(self, newID):
		self.ID = newID

	def getSlaveID(self):
		return self.ID

	def run(self, globalList):
		print "making Slave"
		timeoutCounter = 0

		monitorSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


		while self.alive:
			refusedTosend =[]

			print 'state in slave'
			self.elevStateHandler.printFileContent()
			

			try:
				data = self.connection.recv(4096)
				decData = self.messageParser.parse(data)
				if decData != self.ID:
					self.ID = int(decData)	#needs a format check
				print 'decData[1]: ' + str(decData)

			#master always times out once at initialization for some reason. Quick fix:
			except socket.timeout:
				timeoutCounter += 1
				if timeoutCounter > 1:
					print "Master timed out: ", timeoutCounter
					self.handleLossOfMaster()

			except:
				print "broken pipe"
				self.handleLossOfMaster()


			slavePing = self.messageEncoder.encode('elev_id', "Slave ping: {}".format(self.ID))
			try:
				
				self.connection.send(slavePing)

				if self.messageBuffer:
					print self.messageBuffer

			except:
				print "broken pipe"
				#assume master dead:
				self.handleLossOfMaster()
				refusedTosend.append(slavePing)

			#monitorSocket.sendto("slave {}: alive".format(self.ID), ("localhost", 30000))

			time.sleep(0.4)


#def slaveInit(masterIP):
#	print "New slave"
#	slave = Slave(masterIP, 40404)
#	#slaveThread = threading.Thread(target = slave.run)
#	slaveThread.start()