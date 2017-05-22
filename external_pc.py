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
# Global vars are declared in the {CAM}-frame.
posXCamGlobal	= []
posYCamGlobal	= []
posXPathGlobal	= []
posYPathGlobal	= []
velXPathGlobal	= []
velYPathGlobal	= []

# Local vars are declared in the {PATH}-frame.
velXCorrLocal	= []
velYCorrLocal	= []
velXPathLocal	= []
velYPathLocal	= []
velXCmdLocal	= []
velYCmdLocal	= []
errorXLocal	= []
errorYLocal	= []

# Robot vars are variable from the low-level controller.
rollRobot 	= []
pitchRobot 	= []
yawRobot 	= []

# Time vector.
timeVec	 	= []

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
			#print(node.get_peer_name(uuid), uuid)
			ret = True
	
	return ret

"""
MAIN PROGRAM
"""
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
		#print(msg[3])
		
		#update	
		try:
			# Get message.
			strs   = msg[3].split(",")
			
			# Message structure
			# First the globals.
			gPosXCam  = float(strs[0])
			gPosYCam  = float(strs[1])
			gPosXPath = float(strs[2])
			gPosYPath = float(strs[3])
			gVelXPath = float(strs[4])
			gVelYPath = float(strs[5])
			
			posXCamGlobal.append(gPosXCam)
			posYCamGlobal.append(gPosYCam)
			posXPathGlobal.append(gPosXPath)
			posYPathGlobal.append(gPosYPath)
			velXPathGlobal.append(gVelXPath)
			velYPathGlobal.append(gVelYPath)
			
			# Second the locals.
			lVelXCorr = float(strs[6])
			lVelYCorr = float(strs[7])
			lVelXPath = float(strs[8])
			lVelYPath = float(strs[9])
			lVelXCmd  = float(strs[10])
			lVelYCmd  = float(strs[11])
			lErrorX   = float(strs[12])
			lErrorY   = float(strs[13])
			
			velXCorrLocal.append(lVelXCorr)
			velYCorrLocal.append(lVelYCorr)
			velXPathLocal.append(lVelXPath)
			velYPathLocal.append(lVelYPath)
			velXCmdLocal.append(lVelXCmd)
			velYCmdLocal.append(lVelYCmd)
			errorXLocal.append(lErrorX)
			errorYLocal.append(lErrorY)
			
			# Third the ballbot state.
			#rRoll     = float(strs[14])
			#rPitch    = float(strs[15])
			#rYaw      = float(strs[16])
			
			#rollRobot.append(rRoll)
			#pitchRobot.append(rPitch)
			#yawRobot.append(rYaw)
			
			# Fourth the time vec.			
			t = t + 0.1
			timeVec.append(t)
			
			# Print data.
			print(gPosXPath, gPosYPath, gPosXCam, gPosYCam, lErrorX, lErrorY)
		
		except ValueError:
			pass

# End.
print('GOAL REACHED!')

# LOGGING
# Put in numpy array.
posXCamGlobal  = np.array(posXCamGlobal)
posYCamGlobal  = np.array(posYCamGlobal)
posXPathGlobal = np.array(posXPathGlobal)
posYPathGlobal = np.array(posYPathGlobal)
velXPathGlobal = np.array(velXPathGlobal)
velYPathGlobal = np.array(velYPathGlobal)

velXCorrLocal  = np.array(velXCorrLocal)
velYCorrLocal  = np.array(velYCorrLocal)
velXPathLocal  = np.array(velXPathLocal)
velYPathLocal  = np.array(velYPathLocal)
velXCmdLocal   = np.array(velXCmdLocal)
velYCmdLocal   = np.array(velYCmdLocal)
errorXLocal    = np.array(errorXLocal)
errorYLocal    = np.array(errorYLocal)

rollRobot      = np.array(rollRobot)
pitchRobot     = np.array(pitchRobot)
yawRobot       = np.array(yawRobot)

timeVec	       = np.array(timeVec)

#Save
root = 'images/'
gmtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

basestr = root
basestr += gmtime

logfile = basestr
logfile += ".txt"

np.savetxt(logfile,    (posXCamGlobal,posYCamGlobal,
			posXPathGlobal,posYPathGlobal,
			velXPathGlobal,velYPathGlobal,
			velXCorrLocal,velYCorrLocal,
			velXPathLocal,velYPathLocal,
			velXCmdLocal,velYCmdLocal,
			errorXLocal,errorYLocal,
			#rollRobot,
			#pitchRobot,
			#yawRobot,
			timeVec))

posestr = basestr
posestr += '_pose.png'

pidvelstr = basestr
pidvelstr += '_pidvel.png'

errstr = basestr
errstr += '_error.png'

# Plot
plt.plot(posXPathGlobal, posYPathGlobal, label='Desired path')
plt.plot(posXCamGlobal, posYCamGlobal, label='Actual path')
plt.gca().add_patch(patches.Circle((2.5, 1.5), 0.25))
plt.legend(loc='upper left')
plt.title('Desired vs. actual path')
plt.xlabel('x-axis [m]')
plt.ylabel('y-axis [m]')
plt.axis('equal')
plt.axis([0, S_ROOM_WIDTH, 0, S_ROOM_HEIGHT])
plt.grid()
plt.savefig(posestr)
plt.gcf().clear()	

plt.plot(timeVec, velXCorrLocal, label='PID X output')
plt.plot(timeVec, velYCorrLocal, label='PID Y output')
plt.legend(loc='lower left')
plt.title('PID output velocities in function of time')
plt.xlabel('Time [s]')
plt.ylabel('PID output velocity [m/s]')
plt.ylim([-0.15,0.15])
plt.grid()
plt.savefig(pidvelstr)
plt.gcf().clear()

plt.plot(timeVec, errorXLocal, label='Error X in path frame')
plt.plot(timeVec, errorYLocal, label='Error Y in path frame')
plt.legend(loc='lower left')
plt.title('Errors in function of time expressed in the path frame')
plt.xlabel('Time [s]')
plt.ylabel('Error [m]')
#plt.ylim([-0.15,0.15])
plt.grid()
plt.savefig(errstr)
plt.gcf().clear()
