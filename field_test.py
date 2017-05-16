import time
import threading

from field import field

#static variables
P_NODE		= 'RPi'
P_GROUP_CAM	= 'EAGLE'
R_MARKER 	= 12

#objects
field = field(P_NODE, P_GROUP_CAM, R_MARKER)

posXCam = 0.0
posYCam = 0.0
yawCam  = 0.0

def receiveCam():
	"""
	Function for updating the field.
	"""
	ballbotFound = field.update()
	if(ballbotFound==True):
		[posXCam, posYCam, yawCam] = field.getMarkerPose(R_MARKER)

"""
MAIN: THREADS
"""
t_receiveEagle = threading.Thread(None, receiveEagle, "eagle_receiver_thread")
t_receiveEagle.start()

while(1):print(posXCam, posYCam, yawCam)
