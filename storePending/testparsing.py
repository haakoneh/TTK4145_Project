#test parsing
from MessageFormatHandler import *
msg = "{u'content': u'0 2', u'msgType': u'pendingRequests'}"

parser = MessageParser()

print parser.parse(msg)

