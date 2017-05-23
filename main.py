"""
Main file for the RPi-ballbot.

@Author: Rob Mertens
@Author: Ibe Denaux
"""
# Import.
# Python
import numpy as np
import time as t
import threading
import Queue

from math import atan2, pi

# Classes
from src.pid import PID
from src.field import field
from src.solver import solver
from src.watchdog import watchdog
from src.robot import Robot

# Indexing:
# C : pid-Control
C_KP_X  =  0.4
C_KI_X  =  0.005
C_KD_X  =  0.0
C_MAX_X =  0.125
C_MIN_X = -0.125

C_KP_Y  =  0.7
C_KI_Y  =  C_KP_Y/80
C_KD_Y  =  0.0
C_MAX_Y =  0.1
C_MIN_Y = -0.1

C_FF_VMAX_TOT = 0.08
C_FF_AMAX_TOT = 0.06

C_FF_KP_VEL = 4.0

# R : Robot/Ballbot
R_MARKER = 12
R_PORT   = '/dev/ttyACM1'

# S : Solver/OMG
S_ROOM_WIDTH	= 4.5
S_ROOM_HEIGHT	= 2.5
S_SAFETY_MARGIN	= 0.5

# P : Pyre
P_NODE_SELF	= 'RPi'
P_NODE_EXTERN	= 'PC'
P_GROUP_CAM	= 'EAGLE'

# Other
LOOPTIME = 0.1

# Globals
running = True                        #set the running flag

# Objects.
ballbot = Robot(R_PORT)

solver = solver(LOOPTIME)

field = field(P_NODE_SELF, P_GROUP_CAM, R_MARKER)

watchdog = watchdog(LOOPTIME)

pidPosX = PID(C_KP_X, C_KI_X, C_KD_X, C_MAX_X, C_MIN_X)
pidPosY = PID(C_KP_Y, C_KI_Y, C_KD_Y, C_MAX_Y, C_MIN_Y)

def flush(q):
	"""
	Empty queue.
	"""
	while(q.empty()==False):
		q.get_nowait()

def receiveState():
	"""
	Function where the ballbot receives info about its state.
	state = [x, y, z, r, p, y]'
	"""
	while running:
		ballbot.receive()
		t.sleep(0.05)

def receiveEagle(q):
	"""
	Function for updating the field.
	"""
	while running:
		# Field receiver.
		field.update()
		dataField = field.getRobotPose()
		
		# Ballbot receiver.
		#ballbot.receive()
		#ballbot.info_pose()
		#dataBallbot = ballbot.getState()
		
		data = dataField #+ dataBallbot
		
		# Put on queue.
		q.put_nowait(data)

def controller(q):
	"""
	Function which performs the motion tasks.
	"""
	# Find PC.
	print("Searching...")
	while(field.assignExternalUuid(P_NODE_EXTERN)==False):
		t.sleep(0.1)
	print("External PC found!")
	
	# Start-up indicator.
	for i in range(0,5):
		print(5-i)
		t.sleep(1)
	
	# Running.
	while running:
		# Mode.
		ballbot.set_velocity_mode()
		field.whisperExternalUuid("VELOCITY MODE!")
		
		# Get from queue.
		[posXCam, posYCam, yawCam] = q.get()
		#[posXCam, posYCam, yawCam, bb_x, bb_y, bb_z, bb_roll, bb_pitch, bb_yaw] = q.get()
		
		# Setup robot.		
		#while(field.receiveEndpointExternalUuid()==False):
		#	t.sleep(0.1)	
		#[posXEnd, posYEnd] = field.getEndpoint()
		posXEnd = 1.0
		posYEnd = 1.0
		field.whisperExternalUuid("BALLBOT AT X:%s Y:%s" % (posXCam, posYCam))
		field.whisperExternalUuid("GOAL AT X:%s Y:%s" % (posXEnd, posYEnd))
		
		# Setup and solve optimization problem.		
		solver.setEnvironment(S_ROOM_WIDTH, S_ROOM_HEIGHT)
		solver.addCircle(2.5, 1.5, 0.5)
		solver.setRobot([posXCam, posYCam],
				[posXEnd, posYEnd],
				S_SAFETY_MARGIN,
				C_FF_VMAX_TOT,
				C_FF_AMAX_TOT)
		
		solver.solve()
		
		posXPath, posYPath, velXPath, velYPath, time = solver.getSolution()
		
		# Start cmd.
		#while(field.receiveStartExternalUuid()==False):
		#	t.sleep(0.5)
		
		# Empty queue.
		flush(q)
		
		# Bug fix.
		gammaOld = 0.0
		end = round(0.8*len(time))
		velXPathRot = 0.0
		
		# Loop
		for i in xrange(1, len(time)):
			# Watchdog
			watchdog.start() 
			
			# Update from queue.
			[posXCam, posYCam, yawCam] = q.get()
			#[posXCam, posYCam, yawCam, bb_x, bb_y, bb_z, bb_roll, bb_pitch, bb_yaw] = q.get()
			
			# Calculate angles.
			gamma = atan2(velYPath[i], velXPath[i])
			if(i > end and abs(velXPathRot) < 0.01):
				gamma = gammaOld
			
			alpha = gamma - yawCam
			#print(gamma*180/pi, yawCam*180/pi, alpha*180/pi)
			
			# Rotate to path frame.
			#[posXCamRot, posYCamRot] = ballbot.rotate(posXCam, posYCam, gamma)
			e_x_g = posXPath[i] - posXCam
			e_y_g = posYPath[i] - posYCam
			[e_x, e_y] = ballbot.rotate(e_x_g, e_y_g, -gamma)
			[velXPathRot, velYPathRot] = ballbot.rotate(velXPath[i], velYPath[i], -gamma)
			
			# Correct position.
			velXCorr = pidPosX.calculate(0.0, e_x)
			velYCorr = pidPosY.calculate(0.0, e_y)
			
			# Correct velocity gain.
			kp = solver.getFeedforwardGain(velXPathRot, velYPathRot, C_FF_KP_VEL, C_FF_VMAX_TOT)
			if(i > end):
				kp = 1.0
			
			# Feed forward.
			velXCmd = velXPathRot*kp + velXCorr
			velYCmd = velYPathRot*kp + velYCorr
			
			# Velocity command.			
			[velXCmdRob, velYCmdRob] = ballbot.rotate(velXCmd, velYCmd, alpha)
			ballbot.set_velocity_cmd(velXCmdRob, velYCmdRob, 0)
			field.whisperExternalUuid("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (posXCam, posYCam, posXPath[i], posYPath[i], velXPath[i], velYPath[i], velXCorr, velYCorr,  velXPathRot, velYPathRot, velXCmd, velYCmd, e_x, e_y))
			#field.whisperExternalUuid("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s") % (posXCam, posYCam, posXPath[i], posYPath[i], velXPath[i], velYPath[i], velXCorr, velYCorr, velXPathRot, velYPathRot, velXCmd, velYCmd, e_x, e_y, bb_roll, bb_pitch, bb_yaw"))
			
			# Hold gamma.
			gammaOld = gamma
			
			# Maintain loop time.
			watchdog.hold()
		
		# MODE.
		field.whisperExternalUuid("END")
		
		# Empty the queue.
		flush(q)

"""
MAIN: THREADS
"""

queue = Queue.LifoQueue()

# Make the 2 threads and start them
#t_receiveState = threading.Thread(target=receiveState)
t_receiveEagle = threading.Thread(target=receiveEagle, args=[queue])
t_controller   = threading.Thread(target=controller  , args=[queue])

#t_receiveState.start()
t_receiveEagle.start()
t_controller.start()

# Wait for user input to make the program halt
raw_input("Press key to stop...")

# Set running false when we got a keystroke
running = False

# Wait for both threads to finish
#while t_receiver.is_alive() or t_controller.is_alive():
#	pass
#	t.sleep(0.1)

ballbot.set_idle_mode()
print("Program ended!")
