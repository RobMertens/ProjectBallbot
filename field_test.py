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

for i in range (0, 10):
	field.update()
	while(field.checkMarker(R_MARKER) == False):
		print("robot not found")
	[posXCam, posYCam] = field.getMarkerPosition(R_MARKER)
	print (posXCam, posYCam)
