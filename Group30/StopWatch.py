from datetime import datetime

class StopWatch:
	def __init__(self):
		self.time = datetime.now()
		self.flag = 0

	def resetTimer(self):
		self.time = datetime.now()
		self.flag = 1

	def isTimeOut(self, seconds):
		timeDifference = datetime.now() - self.time
		if(timeDifference.seconds >= seconds):
			self.flag = 0
			return 1
		else:
			return 0
	
	def getTimeFlag(self):
		return self.flag