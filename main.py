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

# Classes
from math import sqrt
from pid import PID
from field import field
from solver import solver
from watchdog import watchdog
from robot import Robot

# Static vars.

# Indexing:
# C : pid-Control
C_KP_X  =  0.5
C_KI_X  =  0.0
C_KD_X  =  0.0
C_MAX_X =  0.08
C_MIN_X = -0.08

C_KP_Y  =  0.5
C_KI_Y  =  0.0
C_KD_Y  =  0.0
C_MAX_Y =  0.08
C_MIN_Y = -0.08

C_FF_VMAX_TOT = 0.02
C_FF_AMAX_TOT = 0.01

C_FF_KP_VEL = 1.2

# R : Robot/Ballbot
R_MARKER = 12
R_PORT   = '/dev/ttyACM0'

# S : Solver/OMG
S_ROOM_WIDTH	= 4.5
S_ROOM_HEIGHT	= 2.5

# P : Pyre
P_NODE_SELF	= 'RPi'
P_NODE_EXTERN	= 'PC'
P_GROUP_CAM	= 'EAGLE'

# Other
LOOPTIME = 0.1

# Objects.
#ballbot = Robot(R_MARKER, R_PORT)
ballbot = Robot(R_PORT)
running = True                        #set the running flag

solver = solver(LOOPTIME)

field = field(P_NODE_SELF, P_GROUP_CAM)
print("Searching...")
while(field.assignExternalUuid(P_NODE_EXTERN)==False):
	t.sleep(0.5)
print("External PC found!")

watchdog = watchdog(LOOPTIME)

pidPosX = PID(C_KP_X, C_KI_X, C_KD_X, C_MAX_X, C_MIN_X)
pidPosY = PID(C_KP_Y, C_KI_Y, C_KD_Y, C_MAX_Y, C_MIN_Y)

def receiver():
	"""
	Function where the ballbot receives info about its state.
	state = [x, y, z, r, p, y]'
	"""
	while running:
		ballbot.receive()
		t.sleep(0.05)

def zyre():
	"""
	Function for receiving robot information.
	"""
	while running:
		field.update()
		t.sleep(0.01)

def controller():
	"""
	Function which performs the motion tasks.
	"""
	for i in range(0,5):
		print(5-i)
		t.sleep(1)
	
	while running:
		# Mode.
		ballbot.set_velocity_mode()
		field.whisperExternalUuid("Velocity mode!")
		
		# Find obstacles.
		# Declare vars
		# Dicts
		markers   = {}
		obstacles = {}
		
		solver.setEnvironment(S_ROOM_WIDTH, S_ROOM_HEIGHT, obstacles)
		
		# Start position from actual position.		
		while(field.checkMarker(R_MARKER)==False):
			field.whisperExternalUuid("Robot not found!")
			t.sleep(0.5)
		
		[posXStart, posYStart] = field.getMarkerPosition(R_MARKER)
		field.whisperExternalUuid("Robot found X:%s Y:%s" % (posXStart, posYStart))
		
		# Receive end position.
		#[posXEnd, posYEnd] = field.receiveEndpointExternalUuid()
		posXEnd = 2.0
		posYEnd = 1.0
		
		field.whisperExternalUuid("Goal X:%s Y:%s" % (posXEnd, posYEnd))
		
		# Solve optimization problem.
		solver.setRobot([posXStart, posYStart],
				[posXEnd, posYEnd],
				C_FF_VMAX_TOT,
				C_FF_AMAX_TOT)
		
		solver.solve()
		
		posXPath, posYPath, velXPath, velYPath, time = solver.getSolution()
		
		# Loop
		for i in xrange(1, len(time)):
			# Watchdog
			watchdog.start() 
			
			# Get ballbot position.
			if(field.checkMarker(R_MARKER)):
				[posXCam, posYCam, yawCam] = field.getMarkerPose(R_MARKER)
			
			else:
				# Give error statement.
				field.whisperExternalUuid("Robot not found!")
			
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
			field.whisperExternalUuid("XCAM:%s YCAM:%s XP:%s YP:%s VCX:%s VCY:%s" % (posXCam, posYCam, posXPath[i], posYPath[i], velXCorr, velYCorr))
			
			# Maintain loop time.
			watchdog.hold()
		
		# MODE.
		field.whisperExternalUuid("Path end reached!")

"""
MAIN: THREADS
"""
# Make the 2 threads and start them
t_receiver = threading.Thread(None, receiver, "ballbot_thread")
t_zyre = threading.Thread(None, zyre, "zyre_thread")
t_controller = threading.Thread(None, controller, "controller_thread")

t_receiver.start()
t_zyre.start()
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
