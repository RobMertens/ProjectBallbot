class solver:
	"""
	This class contains functions which solve the optimization problem.

	@Author: Rob Mertens
	"""
	# Local imports.
	m	= __import__('math')
	np 	= __import__('numpy')
	omg 	= __import__('omgtools')
	#plt 	= __import__('matplotlib.pyplot')
	#shapes = __import__('matplotlib.patches')
	
	# Start-/endpoint
	#__initialPosition  = []
	#__terminalPosition = []
	
	# Solution
	#__position = []
	#__veloctiy = []
	#__time	   = []
	
	# Static vars.
	#updatePeriod = 1.0
	
	def __init__(self, samplePeriod):
		"""
		Constructor.
		"""
		# Some vars.
		self.samplePeriod = samplePeriod
		
		self.__initialPosition = []
		self.__terminalPosition = []
		
		self.__position = []
		self.__velocity = []
		self.__time = []
		
		self.updatePeriod = 1.0
	
	def setSampletime(self, samplePeriod):
		"""
		Method for setting the sampling period.
		
		@param samplePeriod The sample period value.
		"""
		self.samplePeriod = samplePeriod
	
	def setRobot(self, initialPosition, terminalPosition, sdis, vmax, amax):
		"""
		Method for adding a robot to the system.
		
		@param:
		@param:
		"""
		# Positions.
		self.__initialPosition = initialPosition
		self.__terminalPosition = terminalPosition
		
		# Options.
		options = {'syslimit': 'norm_2', 'safety_distance': sdis}
		
		# Add and set.
		self.__robot = self.omg.Holonomic(options=options, bounds={'vmin':-vmax, 'vmax':vmax, 'amin':-amax, 'amax':amax})
		self.__robot.set_initial_conditions(self.__initialPosition)
		self.__robot.set_terminal_conditions(self.__terminalPosition)
	
	def setEnvironment(self, width, height):
		"""
		Method for setting up the environment.
		
		@param: width The width of the camera Field of View
		@param: height The height of the camera Field of View.
		@param: obstacles A list with all obstacles.
		"""
		# Define the shape of the room.
		# This is the field of view of the camera.
		# Manual is good enough for now.
		self.__environment = self.omg.Environment(room={'shape': self.omg.Rectangle(width, height), 'position': [0.5*width, 0.5*height]})
		#self.addObstacles(obstacles)
	
	def addObstacles(self, obstacles):
		"""
		Method for setting up the environment.
		
		@param: obstacles A list with all obstacles in eagle-format.
		"""
		# Put in all obstacles.
		for i,o in obstacles.iteritems():
			# center
			#center = []
			
			# Sort
			if (o[1] == 0):
				# TRIANGLE
				# Not (yet) supported in ProjectEagle.
				pass
			
			elif (o[1] == 1):
				# SQUARE
				# Not (yet) supported in ProjectEagle.
				pass
			
			elif (o[1] == 2):
				# RECTANGLE
				orientation = self.m.atan2((o[4] - o[6]), (o[7] - o[5]))
				height 	= (o[4] - o[6])/(self.m.sin(orientation))
				width 	= (o[4] - o[2])/(self.m.cos(orientation))
				center  = [(o[2] + 0.5*width*self.m.cos(orientation) - 0.5*height*self.m.sin(orientation)),
					   (o[3] + 0.5*width*self.m.sin(orientation) + 0.5*height*self.m.cos(orientation))]
				
				obstacle = self.omg.Rectangle(width, height, orientation)
				
			elif (o[1] == 3):
				# CIRCLE
				radius = o[4] - o[2]
				center = [o[2], o[3]]
				
				obstacle = self.omg.Circle(radius)
			
			elif (o[1] == 4):
				# ELLIPSOID
				# Not (yet) supported in ProjectEagle.
				pass
			
			else:
				# Unknown shape
				pass
			
			
			self.__environment.add_obstacle(self.omg.Obstacle({'position': center}, shape=obstacle))
	
	def addCircle(self, x_c, y_c, r):
		"""
		Add circle.
		"""
		self.__environment.add_obstacle(self.omg.Obstacle({'position': [x_c, y_c]}, shape=self.omg.Circle(radius=r)))
	
	def solve(self):
		"""
		Method for solving the optimization problem.
		"""
		# Create problem.
		problem = self.omg.Point2point(self.__robot, self.__environment, freeT=True)
		problem.init()
		deployer = self.omg.Deployer(problem, self.samplePeriod, self.updatePeriod)
		
		# Solve problem and store solution.
		solution = deployer.update(0, self.__initialPosition)
		self.__position = self.np.c_[solution['state']]
		self.__velocity = self.np.c_[solution['input']]
		self.__time     = self.np.c_[solution['time']]
			
	def getFeedforwardGain(self, velXPath, velYPath, C_FF_KP_VEL, C_FF_VMAX_TOT):
		"""
		FF gain calculation.
		"""
		velPath = self.m.sqrt(velXPath*velXPath + velYPath*velYPath)
	
		kp = (1.0 - C_FF_KP_VEL)/(C_FF_VMAX_TOT)*velPath + C_FF_KP_VEL
	
		return kp
	
	def getSolution(self):
		"""
		Method for getting the solution.
		
		@return: __position[0]	The x-position path vector.
		@return: __position[1]	The y-position path vector.
		@return: __velocity[0]	The x-velocity path vector.
		@return: __velocity[1]	The y-velocity path vector.
		@return: __time[0]	The time vector.
		"""
		return self.__position[0], self.__position[1],self.__velocity[0], self.__velocity[1], self.__time[0]
	
	def plotProblem(self):
		# Create figure
		pass

