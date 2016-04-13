import json

stateSize = 4

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
            content = self.possible_msg_types[msgType](payload)
            data = {'msgType': msgType, 'content': content}
            return json.dumps(data)
        else:
            print 'Msg not valid!'

    def encode_states(self, payload):
        stateString = ''
        for state in payload:
            stateString += ' '.join(str(e) for e in state)
            stateString += ' '
        return stateString.strip()
    
    def encode_request(self, payload):
        return ' '.join(str(e) for e in payload)
    
    def encode_elev_id(self, payload):
        return str(payload)
    
    def encode_udp(self, payload):
        return str(payload)
        # return ''.join(str(e) for e in payload)


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'states': self.parse_states,
            'request': self.parse_request, 
            'elev_id': self.parse_elev_id, 
            'udp': self.parse_udp,
        # More key:values pairs are needed  
        }

    def parse(self, payload):
        try:
            payload = json.loads(payload) # decode the JSON object
            if payload['msgType'] in self.possible_responses:
                return self.possible_responses[payload['msgType']](payload)
            else:
                print 'Msg not valid!'
                return None
        except:
            return None

    def parse_udp(self, payload):
        return str(payload['content'])

    def parse_states(self, payload):
        state_temp = map(int, payload['content'].split(' '))
        state_list= [] 
        n = 0
        for i in xrange(0, len(state_temp), stateSize):
            n += 1
            simple_state = []
            for j in xrange(i, stateSize*n):
                simple_state.append(state_temp[j])
            state_list.append(simple_state)
        return state_list


    def parse_request(self, payload):
        return map(int, payload['content'].split(' '))

    def parse_elev_id(self, payload):
        return str(payload['content'])
