# -*- coding: utf-8 -*-
"""
TEST FILE

@author: Rob M.
"""
###############################################################################
# IMPORT
###############################################################################
import numpy as np
import struct
import time
import pyre

###############################################################################
# ZYRE
###############################################################################
# Make node
# Set header.
# Join network.
# Start communication.
n = pyre.Pyre('pc')
n.join('EAGLE')
n.start()

###############################################################################
# LOOP
###############################################################################
# Declare vars
updateTime = 0.0
sampleTime = 0.1
size = 0

# Dicts
markers = {}
obstacles = {}

# Loop
for i in xrange(1, 2):
#while(1):
	# Clear dicts.
	markers.clear()
	obstacles.clear()
	
	# Obtain information from camera.
	message = n.recv()
	while(message[0]!='SHOUT'):
		message = n.recv()
	
	# Only take the camera data
	package = message[4]
	
	#print(z_data)
	j = 0
	markerCount = 0
	obstacleCount = 0
	#print("Package length:")
	#print(len(package))
	while(j < len(package)):
		# HEADER
		# Size.
		size = struct.unpack('@Q', package[j:j+8])[0]
		j += 8
		
		# Header
		h_id = struct.unpack('@i', package[j:j+4])[0]
		#print(repr(package[j:(j+4)]))
		#print("New header")
		#print("h_id:", repr(h_id))
		#h_id, h_time = struct.unpack('@IL', package[j:(j+8)])
		j += size
		
		# REST
		size = struct.unpack('@Q', package[j:j+8])[0]	
		j += 8
		
		if (h_id == 0):			
			# MARKER			
			m_id, m_x, m_y, m_t = struct.unpack('@i3d', package[j:j+size])
			markers.update({markerCount:[m_id, m_x, m_y, m_t]})
			
			markerCount += 1
			j += size
			
		elif (h_id == 1):
			# OBSTACLE
			o_id, o_shape, o_x1, o_y1, o_x2, o_y2, o_x3, o_y3 = struct.unpack('@2i6d', package[j:j+size])
			obstacles.update({obstacleCount:[o_id, o_shape, o_x1, o_y1, o_x2, o_y2, o_x3, o_y3]})
			
			obstacleCount += 1			
			j += size
		else:
			#nothing
			(1)
		
		#print("j:", j)
	
	#print(markers)
	print(obstacles)

n.stop()

        
