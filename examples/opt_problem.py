"""
This file contains the optimization problem solved by the OMG-Tools toolbox.

@author: Rob Mertens
"""
# Imports.
from math import sin, cos, pi
from src import solver

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

np.set_printoptions(threshold=np.nan)

# Statics.
SAMPLETIME  = 0.1

ROOM_WIDTH  = 20
ROOM_HEIGHT = 20

O1_ORIGIN_X = 0.0
O1_ORIGIN_Y = 0.0
O1_WIDTH    = 2.0
O1_HEIGHT   = 2.0
O1_ANGLE    = pi/4

O2_ORIGIN_X = 5.0
O2_ORIGIN_Y = 5.0
O2_RADIUS   = 2.0

POS_START_X = -9.0
POS_START_Y = -9.0
POS_END_X   =  9.0
POS_END_Y   =  9.0

# Functions.
def rectangle(n, x, y, w, h, o):
	"""
	Function for defining an rectangular obstacle.
	"""
	x1 = x - 0.5*w*cos(o) + 0.5*h*sin(o)
	y1 = y - 0.5*w*sin(o) - 0.5*h*cos(o)
	x2 = x + 0.5*w*cos(o) + 0.5*h*sin(o)
	y2 = y + 0.5*w*sin(o) - 0.5*h*cos(o)
	x3 = x + 0.5*w*cos(o) - 0.5*h*sin(o)
	y3 = y + 0.5*w*sin(o) + 0.5*h*cos(o)	
	
	rectangle = [n, 2, x1, y1, x2, y2, x3, y3]
	
	return rectangle

def circle(n, x, y, r):
	"""
	Function for defining an circular obstacle.
	"""
	x1 = x
	y1 = y
	x2 = x + r
	y2 = y + r
	x3 = x - r
	y3 = y - r
	
	circle = [n, 3, x1, y1, x2, y2, x3, y3]
	
	return circle

# OPT_PROBLEM
# Set up the problem.
solver = solver(SAMPLETIME)

# Make obstacles.
# These objects have the same format as <eagle> objects.
o1 = rectangle(0, O1_ORIGIN_X, O1_ORIGIN_Y, O1_WIDTH, O1_HEIGHT, O1_ANGLE)
o2 = circle(1, O2_ORIGIN_X, O2_ORIGIN_Y, O2_RADIUS)

obstacles = {0:o1, 1:o2}

solver.setEnvironment(ROOM_WIDTH, ROOM_HEIGHT, obstacles)

# Make robot.
solver.setRobot([POS_START_X, POS_START_Y], [POS_END_X, POS_END_Y])

# Solve.
solver.solve()

# Solution.
posXPath, posYPath, velXPath, velYPath, time = solver.getSolution()

# Plot
plt.plot(posXPath, posYPath, label='Desired path')
plt.gca().add_patch(patches.Rectangle((O1_ORIGIN_X - 0.5*O1_WIDTH, O1_ORIGIN_Y - 0.5*O1_HEIGHT), O1_WIDTH, O1_HEIGHT))
plt.gca().add_patch(patches.Circle((O2_ORIGIN_X, O2_ORIGIN_Y), O2_RADIUS))
plt.legend(loc='upper left')
plt.xlabel('x-axis [m]')
plt.ylabel('y-axis [m]')
plt.axis('equal')
plt.grid()
plt.savefig('images/opt_problem/path.png')
plt.gcf().clear()

plt.plot(time, velXPath, label='Velocity x')
plt.plot(time, velYPath, label='Velocity y')
plt.legend(loc='upper left')
plt.title('Velocity in function of time.')
plt.xlabel('Time [s]')
plt.ylabel('Feedforward velocity [m/s]')
plt.grid()
plt.savefig('images/opt_problem/vel.png')
plt.gcf().clear()


