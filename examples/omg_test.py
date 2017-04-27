"""
Test-file.

@Author: Rob Mertens
@Author: Ibe Denaux
"""
# Import.
# Python
import numpy as np

# Classes
from src import solver

# Const.
CAM_WIDTH	= 4.5 #[m]
CAM_HEIGHT	= 2.3 #[m]
LOOPTIME 	= 0.1 #[s]

# Objects.
solver = solver(LOOPTIME)

obstacles = {}

solver.setEnvironment(CAM_WIDTH, CAM_HEIGHT, obstacles)

# Receive end position.
posXStart = 1.0
posYStart = 1.0
posXEnd   = 4.0
posYEnd   = 2.0

# Solve optimization problem.
solver.setRobot([posXStart, posYStart],
		[posXEnd, posYEnd])
solver.solve()

posXPath, posYPath, velXPath, velYPath, time = solver.getSolution()


