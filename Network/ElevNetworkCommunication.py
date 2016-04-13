#Change
from timer import Timer
import os
import fcntl 
import time

class ExternalFileHandler():
	def __init__(self, fileName):
		self.timer = Timer()
		self.listChecker = []
		self.externalFile = fileName

	def writeFile(self, fileContent): 
		numTries = 0
		while True:
			try:
				with open(os.path.join(os.pardir, self.externalFile), 'w') as f:
				    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
				    for s in fileContent:
				        f.write(str(s) + '\n')
				   	fcntl.flock(f, fcntl.LOCK_UN)
				break
			except:
				if numTries == 2:
					break
				else: 
					numTries += 1
					time.sleep(0.1)	
	
	def readFile(self):
		"""Reads from file during initialization, only copies orders from inside elevator"""
		numTries = 0
		while True:
			try:
				with open(os.path.join(os.pardir, self.externalFile), 'r') as f:
					fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
					string_list = [line.rstrip('\n') for line in f]
					fcntl.flock(f, fcntl.LOCK_UN)

				fileContent = []
				for string in string_list:
					fileContent.append(map(int, string[1:-1].split(',')))
				
				return fileContent
			except:
				if numTries == 2:
					break
				else: 
					numTries += 1
					time.sleep(0.1)	

	def updateFile(self):
		fileContent = self.readFile()
		if self.listChecker != fileContent:	
			self.writeFile(self.listChecker)
			self.listChecker = fileContent
			self.timer.resetTimer()
		
		elif self.timer.isTimeOut(1) and fileContent:
			print "time's out"
			while self.listChecker:
				fileContent.append(self.listChecker(0))

			self.writeFile([]) 

		elif not fileContent:
			self.timer.resetTimer()

	def getFileListContent(self):
		if not self.listChecker:
			return []
		listContent = self.listChecker
		self.listChecker = []
		self.writeFile([])
		return listContent 

	def addFileContent(self, fileContent):
		self.listChecker.append(fileContent)
		#print self.listChecker
		self.updateFile()
		#self.writeFile(fileContent)

	def printFileContent(self):
		print 'FileContent: ' + str(self.readFile())
