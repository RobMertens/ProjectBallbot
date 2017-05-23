from src.pid import PID
from src.field import field
from src.robot import Robot

import numpy as np
import threading
import time as t

#PID variables
KP = 0.3
KI = 0.0
KD = 0.0

MAXOUTPUT = 0.08
MINOUTPUT = -0.08

#PID objects
pidPosX = PID(KP, KI, KD, MAXOUTPUT, MINOUTPUT)
pidPosY = PID(KP, KI, KD, MAXOUTPUT, MINOUTPUT)

#ballbot
R_MARKER = 12
R_PORT   = '/dev/ttyACM0'
ballbot = Robot(R_PORT)

#Pyre node
P_NODE_SELF	= 'RPi'
P_NODE_EXTERN	= 'PC'
P_GROUP_CAM	= 'EAGLE'

field = field(P_NODE_SELF, P_GROUP_CAM)
print("Searching...")
while(field.assignExternalUuid(P_NODE_EXTERN)==False):
	t.sleep(0.5)
print("External PC found!")

#other variables
posXEnd = 2.0
posYEnd = 1.0

running = False

#functions

def receiver():
	"""
	Function where the ballbot receives info about its state.
	state = [x, y, z, r, p, y]'
	"""
	while running:
		ballbot.receive()
		t.sleep(0.05)

def controller():
	"""
	Function which performs the motion tasks.
	"""
	for i in range(0,5):
		print(5-i)
		t.sleep(1)
	
	# Mode.
	running = True
	ballbot.set_attitude_mode()
	
	# Start position from actual position.
	field.update()
	
	while(field.checkMarker(R_MARKER)==False):
		field.whisperExternalUuid("Robot not found!")
		t.sleep(0.5)

	[posXStart, posYStart, yawCam] = field.getMarkerPose(R_MARKER)
	
	ballbot.set_velocity_mode()
	field.whisperExternalUuid("Velocity mode!")
	
	#loop
	while running:
		#Update field.
		field.update()
		
		# Get ballbot position.
		if (field.checkMarker(R_MARKER)):
			[posXCam, posYCam, yawCam] = field.getMarkerPose(R_MARKER)
			#field.whisperExternalUuid("X:%s Y:%s YAW:%s" % (posXCam, posYCam, yawCam))
		else:
			# Give error statement.
			field.whisperExternalUuid("Robot not found!")
		
		#position control		
		velX = pidPosX.calculate(posXCam, posXEnd)
		velY = pidPosY.calculate(posYCam, posYEnd)
		
		# Velocity command.			
		ballbot.set_velocity_cmd(velX, velY, 0, yawCam)
		field.whisperExternalUuid("X:%s Y:%s YAW:%s V_X:%s V_Y:%s" % (posXCam, posYCam, yawCam, velX, velY))
		t.sleep(0.05)

"""
MAIN: THREADS
"""
# Make the 2 threads and start them
t_receiver = threading.Thread(None, receiver, "ballbot_thread")
t_controller = threading.Thread(None, controller, "controller_thread")
t_receiver.start()
t_controller.start()

# Wait for user input to make the program halt
raw_input("press some key...")

# Set running false when we got a keystroke
running = False

# Wait for both threads to finish
#while t_receiver.is_alive() or t_controller.is_alive():
#	pass
#	t.sleep(0.1)

ballbot.set_idle_mode()
print "Stopped!"
