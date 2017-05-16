import pyre
import struct
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

P_NODE_SELF = 'PC'
P_NODE_BB = 'RPi'
P_GROUP = 'EAGLE'

S_ROOM_WIDTH = 4.5
S_ROOM_HEIGHT = 2.5

running = True
t = 0.0

# Numpy arrays
posXCam  = []
posYCam  = []
posXPath = []
posYPath = []
velXCorr = []
velYCorr = []
time	 = []

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
			print(node.get_peer_name(uuid), uuid)
			ret = True
	
	return ret

# Find bot.
print("Searching...")
while(findBallbot()==False):
	time.sleep(0.1)
print("Ballbot found!")

# RECV.
while(running):
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
		print("ENDPOINT?")

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
	
	elif(msg[3]=='END'):
		running = False
	
	else:
		print(msg[3])
		
		#update	
		try:
			strs   = msg[3].split(",")
			
			pXCam  = float(strs[0])
			pYCam  = float(strs[1])
			pXPath = float(strs[2])
			pYPath = float(strs[3])
			vXCorr = float(strs[4])
			vYCorr = float(strs[5])
			
			posXCam.append(pXCam)
			posYCam.append(pYCam)
			posXPath.append(pXPath)
			posYPath.append(pYPath)
			velXCorr.append(vXCorr)
			velYCorr.append(vYCorr)
			
			t = t + 0.1
			time.append(t)
		
		except ValueError:
			pass

# End.
print('GOAL REACHED!')

# Put in numpy array.
posXCam = np.array(posXCam)
posYCam = np.array(posYCam)
posXPath = np.array(posXPath)
posYPath = np.array(posYPath)
velXCorr = np.array(velXCorr)
velYCorr = np.array(velYCorr)
time	 = np.array(time)
	

# Plot
plt.plot(posXPath, posYPath, label='Desired path')
plt.plot(posXCam, posYCam, label='Actual path')
plt.gca().add_patch(patches.Circle((2.5, 1.5), 0.5))
plt.legend(loc='upper left')
plt.title('Desired vs. actual path')
plt.xlabel('x-axis [m]')
plt.ylabel('y-axis [m]')
plt.xlim([0, S_ROOM_WIDTH])
plt.ylim([0, S_ROOM_HEIGHT])
plt.axis('equal')
plt.grid()
plt.savefig('images/plot.png')
plt.gcf().clear()	

plt.plot(time, velXCorr, label='PID X output')
plt.plot(time, velYCorr, label='PID Y output')
plt.legend(loc='upper left')
plt.title('PID output velocities in function of time')
plt.xlabel('Time [s]')
plt.ylabel('PID output velocity [m/s]')
plt.ylim([-0.12,0.12])
plt.grid()
plt.savefig('images/vel.png')
plt.gcf().clear()


