# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 13:46:26 2017

@author: ROB
"""
from pid import PID
import numpy as np
import matplotlib.pyplot as plt


# PID tuning:
# (0) Start from Kp = Ki = Kd = 0.00
# (1) Raise Kp until a decent risetime is accomplished.
# (2) Make Ki = 1.0 and measure the time between Over- and Undershoot (Tout)
#     Multiply this value by 1,50.
# (3) Reduce Kp with 80%. Now you have a PI controller.
# (4) Make Kd 1/4 of Ki to obtain PID control.
#control = PID(0.8*10.0, 1.5*0.4, 0.0, 1.00, -1.00)
control = PID(1.0, 0.01, 0.0, 1.00, -1.00)

# Arrays.
n	= 500
pos	= np.zeros(n)
vel	= np.zeros(n)
time	= np.zeros(n)
time_step = 0.01		# f = 100Hz refreshrate
error 	= 0.05		# 5cm weg te regelen

# Remake PID
for i in xrange(0, n):
	if(i == 0):
		pos[i] = error   
		vel[i] = 0.0
		time[i] = 0.0
	else:
		pos[i] = pos[i-1] + vel[i-1]*time_step    
		vel[i] = control.calculate(pos[i], 0.0)
		time[i] = time[i-1] + time_step

##
# PLOT
##

# Create figure
plt.plot(time, pos)
plt.title('Actual position in function of time')
plt.xlabel('Time [s]')
plt.ylabel('Actual position [m]')
plt.grid()
plt.savefig('images/pid_tuning/actpos.png')
plt.gcf().clear()

plt.plot(time, vel)
plt.title('Actual velocity in function of time')
plt.xlabel('Time [s]')
plt.ylabel('Actual velocity [m/s]')
plt.grid()
plt.savefig('images/pid_tuning/actvel.png')
plt.gcf().clear()
