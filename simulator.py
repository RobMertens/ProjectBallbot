# -*- coding: utf-8 -*-
"""
Simulation test w/ random generated noise.
@Author: Rob Mertens
@Author: Ibe Denaux
"""
###############################################################################
# IMPORT
###############################################################################
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from casadi import *
from omgtools import *

from pid import PID

#np.set_printoptions(threshold=np.nan)

###############################################################################
# OMG-TOOLS problem
###############################################################################
t0 = time.time()

options = {}
options['syslimit'] = 'norm_inf'
options['safety_distance'] = 0.5

# Create the vehicle instance
initPosition = [-9.0, -9.0]
termPosition = [ 9.0,  9.0]
ballbot = Holonomic(options=options)
ballbot.set_initial_conditions(initPosition)
ballbot.set_terminal_conditions(termPosition)

# Create environment
environment = Environment(room={'shape': Square(20.)})
obstacle1 = Rectangle(width=5.0, height=5.0)
environment.add_obstacle(Obstacle({'position': [0.0, 0.0]}, shape=obstacle1))

# Create a point-to-point problem
problem = Point2point(ballbot, environment, freeT=True)
problem.init()

# Create deployer
sampleTime = 0.1
deployer = Deployer(problem, sampleTime, 1)
deployer.reset()

# Desired trajectory
bb_trajectories = deployer.update(0, initPosition)
bb_path 	= np.c_[bb_trajectories['state']]
bb_vel	 	= np.c_[bb_trajectories['input']]
bb_time 	= np.c_[bb_trajectories['time']]

#print(len(bb_time))
#print(bb_path[0])

#print('PROBLEM TIME: ', time.time() - t0)

###############################################
# PID
###############################################

actposx = np.zeros(len(bb_path[0]))
actposy = np.zeros(len(bb_path[0]))

actvelx = np.zeros(len(bb_path[0]))
actvely = np.zeros(len(bb_path[0]))

pidvelx = np.zeros(len(bb_path[0]))
pidvely = np.zeros(len(bb_path[0]))

#controlx = PID(0.8*10.0, 1.5*0.4, 0.0, 1.0, -1.0)
#controly = PID(0.8*10.0, 1.5*0.4, 0.0, 1.0, -1.0)

controlx = PID(1.0, 0.01, 0.0, 1.0, -1.0)
controly = PID(1.0, 0.01, 0.0, 1.0, -1.0)

# Loop
for i in xrange(0, len(bb_path[0])):
	if(i == 0):
		actposx[i] = -9.0
		actposy[i] = -9.0
		
		actvelx[i] = 0.0
		actvely[i] = 0.0
	else:
		actposx[i] = actposx[i-1] + actvelx[i-1]*0.1 + np.random.normal(0.0 ,0.05)
		actposy[i] = actposy[i-1] + actvely[i-1]*0.1 + np.random.normal(0.0 ,0.05)
	
	pidvelx[i] = controlx.calculate(actposx[i], bb_path[0,i])
	pidvely[i] = controly.calculate(actposy[i], bb_path[1,i])
	
	actvelx[i] = bb_vel[0,i] + pidvelx[i] 
	actvely[i] = bb_vel[1,i] + pidvely[i]

###############################################
# PLOT
###############################################

# Create figure
plt.plot(bb_path[0], bb_path[1], label='Desired path')
plt.plot(actposx, actposy, label='Actual path')
plt.gca().add_patch(patches.Rectangle((-2.5, -2.5), 5.0, 5.0))
plt.legend(loc='upper left')
plt.title('Desired vs. actual path')
plt.xlabel('x-axis [m]')
plt.ylabel('y-axis [m]')
plt.axis('equal')
plt.grid()
plt.savefig('images/simulator/path.png')
plt.gcf().clear()

plt.plot(bb_time[0], bb_vel[0], label='FF velocity x')
plt.plot(bb_time[0], bb_vel[1], label='FF velocity y')
plt.legend(loc='upper left')
plt.title('Desired vs. actual path')
plt.xlabel('Time [s]')
plt.ylabel('Feedforward velocity [m/s]')
plt.grid()
plt.savefig('images/simulator/ffvel.png')
plt.gcf().clear()


plt.plot(bb_time[0], pidvelx, label='PID X output')
plt.plot(bb_time[0], pidvely, label='PID Y output')
plt.legend(loc='upper left')
plt.title('PID output velocities in function of time')
plt.xlabel('Time [s]')
plt.ylabel('PID output velocity [m/s]')
plt.ylim([-0.6,0.6])
plt.grid()
plt.savefig('images/simulator/pidvel.png')
plt.gcf().clear()

plt.plot(bb_time[0], actvelx, label='Actual velocity x')
plt.plot(bb_time[0], actvely, label='Actual velocity y')
plt.legend(loc='upper left')
plt.title('Actual velocities in function of time')
plt.xlabel('Time [s]')
plt.ylabel('Actual velocity [m/s]')
#plt.ylim([-0.2,1.0])
plt.grid()
plt.savefig('images/simulator/actvel.png')
plt.gcf().clear()
