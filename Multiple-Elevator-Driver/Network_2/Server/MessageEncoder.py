class MessageEncoder():
    def __init__(self):

        self.possible_msg_types = {
            'states': self.encode_states,
            'request': self.encode_request, 
            'elev_id': self.encode_elev_id, 
            
            'udp_response': self.udp_response,
	    # More key:values pairs are needed	
        }
    
    def encode(self, msgType, payload):
        if msgType in self.possible_responses:
            return self.possible_responses[msgType](payload)
        else:
            print 'Msg not valid!'
            # Response not valid
    def encode_states(self, payload):
        stateString = ''
        for state in payload:
            stateString += ''.join(str(e) for e in state)
        return stateString
    
    def encode_request(self, payload):
        pass
    
    def encode_elev_id(self, payload):
        pass
    
    def udp_response(self, payload):
        pass
        
   
        