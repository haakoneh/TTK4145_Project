
flagGlobalDictionary = { 	'flagSlave': True, 
							'flagSlaveMsgReciever': True, 

						}

def getGlobalFlag(flagType):
	if flagType in flagGlobalDictionary:
		return flagGlobalDictionary[flagType]
	else:
		return None

def setGlobalFlag(flagType, flagValue):
	if flagType in flagGlobalDictionary:
		if flagValue == True or flagValue == False:
			flagGlobalDictionary[flagType] = flagValue
		else:
			print 'Illegal flagValue!: ' + str(flagValue)


# print 'flagSlave: ' + str(getGlobalFlag('flagSlave'))

# setGlobalFlag('flagSlave', 'lol')

# print 'flagSlave: ' + str(getGlobalFlag('flagSlave'))