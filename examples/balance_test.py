"""
Main file for the RPi-ballbot.

@Author: Rob Mertens
@Author: Ibe Denaux
"""
# Import.
# Python
import numpy as np

from src import robot

# Static vars.

# Indexing:
# R : Robot/Ballbot
R_MARKER = 8
R_PORT   = '/dev/ttyACM0'

# Objects.
ballbot = robot(R_MARKER, R_PORT)
ballbot.set_attitude_mode()

"""
Main loop.
"""	
while(1):
	# Mode.
	ballbot.set_attitude_mode()

        
