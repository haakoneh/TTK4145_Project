from MessageParser import *
from MessageEncoder import *
import json 

def testing(testType):
	parser = MessageParser()
	encoder = MessageEncoder()

	print 

	if testType == 1:
		stateTest = [[0 , 1], [2, 3]]

		print encoder.encode('states', stateTest)

		req = [1 , 2]

		print encoder.encode('request', req)

	elif testType == 2:
		string = "0 1 2 3"

		data = {'msgType': 'states', 'content': string}

		#print parser.parse(json.dumps(data))

		data_2 = {'msgType': 'request', 'content': '1 2'}

		print parser.parse(json.dumps(data_2))

	elif testType == 3:
		stateTest = [[0 , 1], [2, 3]]

		print 'Expected result: ' + str(stateTest)

		data = {'msgType': 'states', 'content': encoder.encode('states', stateTest)} 
		#print data

		print  'Given result: ' + str(parser.parse(json.dumps(data)))

	else:
		print 'Invalid type'

	print


into = raw_input('What type of test? ')

testing(int(into))