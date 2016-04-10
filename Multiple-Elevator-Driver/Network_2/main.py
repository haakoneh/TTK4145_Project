# import Client
# import Server


#master.py
from masterMeetSlave import *

statelist = []


#--------main purpose-------

# settup server

# start elevator
# thread UDP_listenforBroadcast

# refresh elevator states and order queue

# for orders in queue:
# 	elevator = findOptimalElevator(elevStateList, request)

# send(order, elevator)

#---------------------------

#startup: look for other masters first
seeker = MasterSlaveSeeker()






#we're the master, so we're saying that to other elevators
seeker.replyToSlaves()
