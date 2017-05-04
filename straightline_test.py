"""
Main file for the RPi-ballbot.

@Author: Rob Mertens
@Author: Ibe Denaux
"""
# Import.
# Python
import numpy as np
import threading
import time as t

# Classes
from pid import PID
from field import field
from solver import solver
from watchdog import watchdog
from robot import Robot

# Static vars.

# Indexing:
# C : pid-Control
C_KP_X  =  1.0
C_KI_X  =  0.1
C_KD_X  =  0.0
C_MAX_X =  1.0
C_MIN_X = -1.0

C_KP_Y  =  1.0
C_KI_Y  =  0.1
C_KD_Y  =  0.0
C_MAX_Y =  1.0
C_MIN_Y = -1.0

# R : Robot/Ballbot
R_MARKER = 12
R_PORT   = '/dev/ttyACM0'

# S : Solver/OMG
S_ROOM_WIDTH	= 4.5
S_ROOM_HEIGHT	= 2.3

# P : Pyre
P_NODE		= 'RPi'
P_GROUP_CAM	= 'EAGLE'
P_GROUP_PC	= 'PC'

# Other
LOOPTIME = 0.1

# Objects.
#ballbot = Robot(R_MARKER, R_PORT)
ballbot = Robot(R_PORT)
running = True                          #set the running flag

solver = solver(LOOPTIME)

field = field(P_NODE, P_GROUP_CAM)

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

def controller():
	"""
	Function which performs the motion tasks.
	"""
	for i in range(0,5):
		print(5-i)
		t.sleep(1)
	
	while running:
		# Mode.
		ballbot.set_attitude_mode()
		
		# Find obstacles.
		# Declare vars
		# Dicts
		markers   = {}
		obstacles = {}
		
		solver.setEnvironment(S_ROOM_WIDTH, S_ROOM_HEIGHT, obstacles)
		print("Environment set.")
		
		# Start position from actual position.
		field.update()
		print("Field updated.")
		
		while(field.checkMarker(R_MARKER) == False):
			print("Robot not found!")
			pass
		
		posXStart, posYStart = field.getMarkerPosition(R_MARKER)
		
		# Receive end position. (PC-GROUP)
		posXEnd = 4.0
		posYEnd = 2.0
		
		# Solve optimization problem.
		solver.setRobot([posXStart, posYStart],
				[posXEnd, posYEnd])
		solver.solve()
		
		posXPath, posYPath, velXPath, velYPath, time = solver.getSolution()
		
		# Move over path.		
		# Velocity mode.
		ballbot.set_velocity_mode()
		
		# Loop
		for i in xrange(1, len(time)):
			# Watchdog
			watchdog.start() 
			
			# Update field.
			field.update()
			
			# Get ballbot position.
			if (field.checkMarker(R_MARKER)):
				posXCam, posYCam = field.getMarkerPosition(R_MARKER)
			else:
				# Give error statement.
				print("Robot not found!")
			
			# Correct position.
			velXCorr = pidPosX.calculate(posXCam, posXPath)
			velYCorr = pidPosY.calculate(posYCam, posYPath)
			
			# Feed forward.
			velXCmd = velXPath + velXCorr
			velYCmd = velYPath + velYCorr
			
			# Velocity command.			
			ballbot.set_velocity_cmd(velXCmd, velYCmd, 0)
			
			# Maintain loop time.
			watchdog.hold()
		
		# MODE.
		ballbot.set_attitude_mode()

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
print "Stopped"
