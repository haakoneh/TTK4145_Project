"""
Payloads, as defined above, are dictionaries in Python. Also, when you decode a JSON object,
you will get a dictionary in Python. Dictionaries are like Hashtables in Java: an unordered set of
key: value pairs. Hence, if following EXAMPLE 1 above, printing payload['request'] will
give you 'login'.
- Following the previous point: when the client (the same logic can be applied to the server)
receives a response from the server, it has to check which type of response it is, in order to
perform the corresponding actions. This can be implemented quite neatly with dictionaries. The
client can have a dictionary of possible responses: the keys will be the possible responses (e.g.
'login', 'msg'), the values will be the corresponding methods to be called when that response
is received:
EXAMPLE 3 (included in the skeleton)
If self.possible_responses is a dictionary as described below (in this example, only error and info are
given), and payload is the decoded JSON object received through the socket (i.e. a dictionary), the
following code will check if payload is a possible response and will call the corresponding method
passing the content of the payload as a parameter: 
"""

import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'states': self.parse_states,
            'request': self.parse_request, 
            'elev_id': self.parse_elev_id, 
            'error': self.parse_error,
            'info': self.parse_info,
            'udp': self.parse_udp,
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode the JSON object

        if payload['msgType'] in self.possible_responses:
            return self.possible_responses[payload['msgType']](payload)
        else:
            print 'Msg not valid!'
            # Response not valid

    def parse_udp(self, payload):
        return payload['content'].split(' ')

    def parse_states(self, payload):
        state_temp = map(int, payload['content'].split(' '))

        state_list= [] 
        for i in xrange(0, len(state_temp), 2):
        	state_list.append([state_temp[i], state_temp[i+1]])
        return state_list


    def parse_request(self, payload):
        return map(int, payload['content'].split(' '))

    def parse_elev_id(self, payload):
        pass

    def parse_error(self, payload):
        pass
    
    def parse_info(self, payload):
        pass
    
    # Include more methods for handling the different responses... 
parser = MessageParser()

string = "0 1 2 3"

data = {'msgType': 'states', 'content': string}

print parser.parse(json.dumps(data))


