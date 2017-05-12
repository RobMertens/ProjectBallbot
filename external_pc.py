import pyre
import struct
import time

P_NODE_SELF = 'PC'
P_NODE_BB = 'RPi'
P_GROUP = 'EAGLE'

S_ROOM_WIDTH = 4.5
S_ROOM_HEIGHT = 2.5

# Pyre node.
node = pyre.Pyre(P_NODE_SELF)
node.start()
node.join(P_GROUP)
uuid = node.uuid()

def findBallbot():
	"""
	Method for assigning the external UUID.
	"""
	ret = False
	peers = node.peers()
	for p in peers:
		if(node.get_peer_name(p)==P_NODE_BB):
			uuid = p
			print("Ballbot", uuid)
			ret = True
	
	return ret

# Find bot.
print("Searching...")
while(findBallbot()==False):
	time.sleep(0.01)
print("Ballbot found!")

# RECV.
while(1):
	msg = node.recv()
	while(msg[0]!='WHISPER'):		
		msg = node.recv()
	
	if(msg[3]=='START'):
		# Receive start cmd.
		raw_input('START?')
		
		# Msg.
		node.whisper(uuid, "ACK")
	
	elif(msg[3]=='ENDPOINT'):
		# Get endpoint.
		print("")
		print("Enter the goal endpoint.")

		# Receive endpoint X
		x_end = 0.0
		while(x_end <= 0.0 or x_end > S_ROOM_WIDTH):
			try:
			    x_end = float(raw_input('X_END:'))
			except ValueError:
			    print("NaN")
			
			# Check boundaries.
			if(x_end <= 0.0):
				print("Value must be greater than %s." % (0.0))
			elif(x_end > S_ROOM_WIDTH):
				print("Value must be lower than %s." % (S_ROOM_WIDTH))
			else:
				pass

		# Receive endpoint Y
		y_end = 0.0
		while(y_end <= 0.0 or y_end > S_ROOM_HEIGHT):
			try:
			    y_end = float(raw_input('Y_END:'))
			except ValueError:
			    print("NaN")
			
			# Check boundaries.
			if(y_end <= 0.0):
				print("Value must be greater than %s." % (0.0))
			elif(x_end > S_ROOM_WIDTH):
				print("Value must be lower than %s." % (S_ROOM_HEIGHT))
			else:
				pass

		# Pack message.
		msg = struct.pack('@2f', x_end, y_end)
		node.whisper(uuid, msg)
			
	else:
		print(msg)


