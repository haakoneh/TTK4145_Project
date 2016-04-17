from threading import Thread, Lock
import SocketServer
import socket
import json
import time
from GlobalFunctions import * 
from MessageFormatHandler import *
from RequestCostCalculator import *
from colors import *
from channels import INPUT

connections = []
stateList = []
stateDict = {}
allMsgBuffers = {}
pendingRequests = []


class SlaveHandler(Thread):
	def __init__(self, connection,addr, lock):
		super(SlaveHandler, self).__init__()
		global connections, stateDict, allMsgBuffers, pendingRequests
		self.connection = connection
		self.addr = addr
		self.slaveID = -1
		connections.append(self.connection)
		self.updateID()

		self.messageEncoder = MessageEncoder()
		self.messageParser = MessageParser()
		self.msgBuffer = []
		self.lock = lock

		self.stayAlive = True 

		allMsgBuffers[str(self.slaveID)] = []
		
	def msgToAllBuffers(self, msg):
		for msgBuffer in allMsgBuffers:
			allMsgBuffers[msgBuffer].append(msg)
		
	def pingToSlave(self):
		id_ping = self.messageEncoder.encode('elev_id', self.getID())
		self.connection.send(id_ping)
	
	def getID(self):
		return self.slaveID

	def sendRequestToSlave(self, request):
		bestElevator = -1

		lowestCost = INPUT.NUM_FLOORS*2 

		for elevator in stateDict:
			cost = calculateCost(stateDict[elevator], request)
			if elevator >= 0:
				if(cost < lowestCost):
					lowestCost = cost
					bestElevator = elevator

		msg = self.messageEncoder.encode('request', request)
		self.lock.acquire()

		if not str(bestElevator) in allMsgBuffers:
			allMsgBuffers[str(bestElevator)] = [msg]
		else:
			if not msg in allMsgBuffers[str(bestElevator)]:
				allMsgBuffers[str(bestElevator)].append(msg)

		self.lock.release()

	def addPendingGlobalRequest(self, request):
		self.lock.acquire()
		if(request not in pendingRequests):
			pendingRequests.append(request)
		self.lock.release()

	def removePendingGlobalRequest(self, request):
		self.lock.acquire()
		if(request in pendingRequests):
			pendingRequests.remove(request)
		self.lock.release()

	def broadcastPendingRequests(self):
		self.lock.acquire()
		msg = self.messageEncoder.encode('pendingRequests', pendingRequests)
		self.msgToAllBuffers(str(msg))
		self.lock.release()

	def updateID(self):
		try:
			self.slaveID = connections.index(self.connection)
		except:
			cprint("slave not found in connections list", FAIL)
			self.slaveID = -1



	def removeSlave(self):
		self.lock.acquire()
		try:
			del allMsgBuffers[str(self.getID())]
		except:
			cprint("Tried removing slave without msgBuffer entry, ID: ".format(self.getID), FAIL)
		try:
			del stateDict[(str(self.slaveID))]
		except:
			cprint("Tried removing slave without stateDict entry, ID: ".format(self.getID), FAIL)

		connections.remove(self.connection)

		self.msgToAllBuffers(self.messageEncoder.encode("slaveLost", None))

		self.lock.release()

		self.slaveID = -1

	def getMsgBuffer(self):
		default = " "
		return allMsgBuffers.get(str(self.slaveID), default)


	def run(self):
		while True:
			self.updateID()
			try:
				receivedString = self.connection.recv(4096)
			except:
				self.removeSlave()
				break

			try:
				message = json.loads(receivedString)
			except:
				cprint("json.loads fail", FAIL)
				self.removeSlave()
				break


			if message['msgType'] == 'state':
				self.lock.acquire()
				stateDict[str(self.getID())] = self.messageParser.parse(receivedString)
				self.lock.release()

			elif message['msgType'] == 'ping':
				ping = self.messageParser.parse(receivedString)

			elif message['msgType'] == 'request':
				request = self.messageParser.parse(receivedString)
				self.sendRequestToSlave(request)
				self.addPendingGlobalRequest(request)
				self.broadcastPendingRequests()

			elif message['msgType'] == 'removePending':
				request = self.messageParser.parse(receivedString)
				self.removePendingGlobalRequest(request)
				self.broadcastPendingRequests()
				

			if str(self.getID()) in allMsgBuffers:
				if allMsgBuffers[str(self.getID())]:
					sendstuff = allMsgBuffers[str(self.getID())].pop(0)

					try:
						self.connection.send(sendstuff)
					except:
						cprint("Removing slave: {}".format(self.getID()), WARNING)
						self.removeSlave()
						break

				else:
					self.pingToSlave()
			else:
				cprint("Slave {} dead".format(self.getID()), FAIL)
				break

			time.sleep(0.1)

def starter():
	HOST, PORT = getMyIP(), 23432

	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverSocket.bind((HOST, PORT))
	
	serverSocket.listen(100)

	lock = Lock()

	while True:
		connection, addr = serverSocket.accept()
		SlaveHandler(connection, addr, lock).start()
