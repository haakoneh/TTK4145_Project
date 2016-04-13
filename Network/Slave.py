# -*- coding: utf-8 -*-
import socket
import json
import time
import errno
import sys
import threading
from watchdog import Watchdog
import globalFunctions
from MessageFormatHandler import *

class Slave:
	
	def __init__(self, host, serverPort):
		print "New Slave instance"
		self.host = host
		self.serverPort = serverPort
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.settimeout(0.2)
		self.connection.connect((self.host, self.serverPort))
		self.ID = -1
		self.jsonObject = None
		self.alive = True
		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()

	def disconnect(self):
		self.connection.close()
		try:
			self.messageReceiver.stop()
		except:
			pass
	
	def receiveMessage(self):
		self.messageReceiver = MessageReceiver(self.connection)
		self.messageReceiver.start()

	def send(self):
		self.connection.send(self.jsonObject)

	def handleLossOfMaster(self):
		"""master is dead, act acordingly
		Exit the while loop, so connections die and
		stop pinging alive to processMonitor. Which allows  
		external processMonitor to start main.py

		"""
		if self.ID > 0:
			time.sleep((int(self.ID) - 1) * 0.3)

		self.alive = False

		# if(self.ID == 0):
		# 	print "Your master died"
		# 	#restart as slave
		# 	slave.run()


		# if(self.ID >= 1):
		# 	#Dead master: Take over
		# 	#restart as master
		# 	print "Distant master died: Rise to power"

		# 	# time.sleep((int(self.ID) - 1)*0.2)
		# 	time.sleep(0.2)
		# 	# print "acive count: ", threading.activeCount()
		# 	# print "enumerate: ", threading.enumerate()

		# 	self.alive = False

		# else:
		# 	#restart as slave
		# 	print "Distant master died find new master"
		# 	self.alive = False



	def run(self):
		print "making Slave"
		timeoutCounter = 0

		monitorSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


		#runPythonScript("elevMain.py")

		while self.alive:
			
			try:
				data = self.connection.recv(4096)
				decData = self.messageParser.parse(data)
				if decData != self.ID:
					self.ID = int(decData)	#needs a format check
				print decData

			#master always times out once at initialization for some reason. Quick fix:
			except socket.timeout:
				timeoutCounter += 1
				if timeoutCounter > 1:
					print "Master timed out: ", timeoutCounter
					self.handleLossOfMaster()

			except:
				print "broken pipe"
				self.handleLossOfMaster()

			try:
				slavePing = self.messageEncoder.encode('elev_id', "Slave ping: {}".format(self.ID))
				self.connection.send(slavePing)
			except:
				print "broken pipe"
				#assume master dead:
				self.handleLossOfMaster()

			monitorSocket.sendto("slave {}: alive".format(self.ID), ("localhost", 30000))

			time.sleep(0.4)


def slaveInit(masterIP):
	print "New slave"
	slave = Slave(masterIP, 9998)
	slaveThread = threading.Thread(target = slave.run)
	slaveThread.start()