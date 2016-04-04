

import socket

def getMyIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	IP = s.getsockname()[0]
	s.close()
	return IP

print getMyIP()




#pseudo code algorithm


socket.sendto(broadcast, port)

re