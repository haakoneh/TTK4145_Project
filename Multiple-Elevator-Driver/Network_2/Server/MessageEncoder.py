class MessageEncoder():
    def __init__(self):

        self.possible_msg_types = {
            'states': self.encode_states,
            'request': self.encode_request, 
            'elev_id': self.encode_elev_id, 
            
            'udp': self.encode_udp,
	    # More key:values pairs are needed	
        }
    
    def encode(self, msgType, payload):
        if msgType in self.possible_msg_types:
            return self.possible_msg_types[msgType](payload)
        else:
            print 'Msg not valid!'
            # Response not valid
    def encode_states(self, payload):
        stateString = ''
        for state in payload:
            stateString += ' '.join(str(e) for e in state)
            stateString += ' '
        return stateString
    
    def encode_request(self, payload):
        return ''.join(str(e) for e in payload)
    
    def encode_elev_id(self, payload):
        return None
    
    def encode_udp(self, payload):
        return ''.join(str(e) for e in payload)
                

encoder = MessageEncoder()

stateTest = [[0 , 1], [2, 3]]

print encoder.encode('states', stateTest)