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

# Classes
from pid import PID
from field import field
from solver import solver
from watchdog import watchdog
from robot import Robot

# Indexing:
# C : pid-Control
C_KP_X  =  0.4
C_KI_X  =  0.0
C_KD_X  =  0.0
C_MAX_X =  0.1
C_MIN_X = -0.1

C_KP_Y  =  0.4
C_KI_Y  =  0.0
C_KD_Y  =  0.0
C_MAX_Y =  0.1
C_MIN_Y = -0.1

C_FF_VMAX_TOT = 0.1
C_FF_AMAX_TOT = 0.04

C_FF_KP_VEL = 1.5

# R : Robot/Ballbot
R_MARKER = 12
R_PORT   = '/dev/ttyACM0'

# S : Solver/OMG
S_ROOM_WIDTH	= 4.5
S_ROOM_HEIGHT	= 2.5
S_SAFETY_MARGIN	= 0.2

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
		field.update()
		q.put_nowait(field.getRobotPose())

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
		
		[posXCam, posYCam, yawCam] = q.get()
		# Setup robot.		
		#while(field.receiveEndpointExternalUuid()==False):
		#	t.sleep(0.1)	
		#[posXEnd, posYEnd] = field.getEndpoint()
		posXEnd = 1.0
		posYEnd = 1.0
		field.whisperExternalUuid("BALLBOT AT X:%s Y:%s" % (posXCam, posYCam))
		field.whisperExternalUuid("GOAL AT X:%s Y:%s" % (posXEnd, posYEnd))
		
		# Setup and solve optimization problem.
		#obstacles = {}
		#obstacles = {o1:[0, 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
		
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
		
		# Loop
		for i in xrange(1, len(time)):
			# Watchdog
			watchdog.start() 
			
			[posXCam, posYCam, yawCam] = q.get()
			
			# Correct position.
			velXCorr = pidPosX.calculate(posXCam, posXPath[i])
			velYCorr = pidPosY.calculate(posYCam, posYPath[i])
			
			# Correct velocity gain.
			kp = solver.getFeedforwardGain(velXPath[i], velYPath[i], C_FF_KP_VEL, C_FF_VMAX_TOT)
			
			# Feed forward.
			velXCmd = velXPath[i]*kp + velXCorr
			velYCmd = velYPath[i]*kp + velYCorr
			
			# Velocity command.			
			ballbot.set_velocity_cmd(velXCmd, velYCmd, 0, yawCam)
			#[velXRob, velYRob, velZRob] = ballbot.global2RobotFrame(velXCmd, velYCmd, 0, yawCam)
			#field.whisperExternalUuid("V_ROB_X:%s V_ROB_Y:%s YAW:%s" % (velXRob, velYRob, yawCam))
			field.whisperExternalUuid("%s,%s,%s,%s,%s,%s" % (posXCam, posYCam, posXPath[i], posYPath[i], velXCorr, velYCorr))
			
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
t_receiveState = threading.Thread(target=receiveState)
t_receiveEagle = threading.Thread(target=receiveEagle, args=[queue])
t_controller   = threading.Thread(target=controller  , args=[queue])

t_receiveState.start()
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
