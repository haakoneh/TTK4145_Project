import json

stateSize = 4
requestSize = 2

class MessageEncoder():
    def __init__(self):
        self.possible_msg_types = {
            'state': self.encodeState,
            'request': self.encodeRequest, 
            'elev_id': self.encodElevID, 
            'ping': self.encodePing,
            'udp': self.encodeUDP,
            'pendingRequests': self.encodePending,
            'removePending': self.encodeRemovePending,
            'slaveLost': self.encodeSlaveLost
        }
    
    def encode(self, msgType, payload):
        if msgType in self.possible_msg_types:
            content = self.possible_msg_types[msgType](payload)
            data = {'msgType': msgType, 'content': content}
            return json.dumps(data)
        else:
            print 'Msg not valid!'

    def encodePing(self, payload):
        return str(payload)

    def encodeState(self, payload):
        return ' '.join(str(e) for e in payload)
    
    def encodeRequest(self, payload):
        return ' '.join(str(e) for e in payload)
    
    def encodElevID(self, payload):
        return str(payload)
    
    def encodeUDP(self, payload):
        return str(payload)

    def encodePending(self, payload):
        pendingString = ''
        for request in payload:
            pendingString += ' '.join(str(e) for e in request)
            pendingString += ' '
        return str(pendingString.strip())

    def encodeRemovePending(self, payload):
        return ' '.join(str(e) for e in payload)
    
    def encodeSlaveLost(self, payload):
        return None

class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'state': self.parseState,
            'request': self.parseRequest, 
            'elev_id': self.parseElevID, 
            'ping': self.parsePing,
            'udp': self.parseUDP,
            'pendingRequests': self.parsePending,
            'removePending': self.parseRemovePending  
        }

    def parse(self, payload):
        try:
            payload = json.loads(payload) # decode the JSON object
        
        except:
            pass

        try:
            if payload['msgType'] in self.possible_responses:
                return self.possible_responses[payload['msgType']](payload)
            else:
                print 'Msg not valid!'
                return None
        except:
            print "Parsing returned none"
            return None

    def parseUDP(self, payload):
        return str(payload['content'])

    def parsePing(self, payload):
        return str(payload)

    def parseState(self, payload):
        return map(int, payload['content'].split(' '))

    def parseRequest(self, payload):
        return map(int, payload['content'].split(' '))

    def parseElevID(self, payload):
        return int(payload['content'])

    def parsePending(self, payload):
        if(payload == None):
            return []
        request_temp = map(int, payload['content'].split(' '))
        requestList= [] 
        n = 0
        for i in xrange(0, len(request_temp), requestSize):
            n += 1
            simpleRequest = []
            for j in xrange(i, requestSize*n):
                simpleRequest.append(request_temp[j])
            requestList.append(simpleRequest)

        return requestList

    def parseRemovePending(self, payload):
        return map(int, payload['content'].split(' '))
