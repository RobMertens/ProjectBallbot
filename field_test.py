#imports
import numpy as np
from field import field

#static variables
P_NODE		= 'RPi'
P_GROUP_CAM	= 'EAGLE'
P_GROUP_PC	= 'PC'
R_MARKER 	= 12

#objects
field = field(P_NODE, P_GROUP_CAM)

while(1):
	field.update()
	while(field.checkMarker(R_MARKER) == False):
		field.update()
		print("robot not found")
	[posXCam, posYCam, yawCam] = field.getMarkerPose(R_MARKER)
	print (posXCam, posYCam, yawCam)
