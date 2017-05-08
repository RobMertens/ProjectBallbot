# Should be local declaration.
import pyre as p

class field:
	"""
	This class contains functions for the field of view for the EAGLE-camera.
	Every object found by the camera is kept in a dict.

	@Author: Rob Mertens
	"""
	# Imports.
	struct 	= __import__('struct')
	#pyre 	= __import__('pyre')
	
	# Data buffer		
	markers = {}
	obstacles = {}
	
	# Enum
	__MARKER   = 0
	__OBSTACLE = 1
	__IMAGE    = 2
	
	def __init__(self, name, group):
		"""
		Constructor.
		Initializes the pyre node.
	
		@param: name The name of the pyre node.
		"""
		self.__name = name
		self.__group = group
		
		self.__node = p.Pyre(self.__name)
		#self.__node.set_name(self.__name)
		self.__node.start()
		self.__node.join(self.__group)
	
	def __exit__(self):
		"""
		Destructor.
		Initializes the pyre node.
	
		@param: name The name of the pyre node.
		"""
		self.__node.stop()
	
	def update(self):
		"""
		Method for receiving signals from the camera.
		
		@return: Package w/ information.
		"""
		# Reset lists.
		byte = 0
		size = 0
		markerCount = 0
		obstacleCount = 0
		self.markers.clear()
		self.obstacles.clear()
		success = True
		
		# Obtain information from camera.
		message = self.__node.recv()
		while(message[0] != 'SHOUT'):
			message = self.__node.recv()

		# Only take the camera data.
		package = message[4]

		# Loop through package.
		while(byte < len(package)):
			# HEADER
			# Size.
			size = self.struct.unpack('@Q', package[byte:(byte+8)])[0]
			byte += 8
			
			# Header
			h_id = self.struct.unpack('@i', package[byte:(byte+4)])[0]
			byte += size
	
			# REST
			size = self.struct.unpack('@Q', package[byte:(byte+8)])[0]	
			byte += 8
			
			# MARKER
			if (h_id == self.__MARKER):						
				m_id, m_x, m_y, m_t = self.struct.unpack('@i3d', package[byte:(byte+size)])
				self.markers.update({markerCount:[m_id, m_x, m_y, m_t]})
				
				markerCount += 1
				byte += size
			
			# OBSTACLE
			elif (h_id == self.__OBSTACLE):
				o_id, o_shape, o_x1, o_y1, o_x2, o_y2, o_x3, o_y3 = self.struct.unpack('@2i6d', package[byte:(byte+size)])
				self.obstacles.update({obstacleCount:[o_id, o_shape, o_x1, o_y1, o_x2, o_y2, o_x3, o_y3]})
				
				obstacleCount += 1
				byte += size
			
			# IMAGE
			elif (h_id == self.__IMAGE):
				#TODO:: What to do with an image?
				success = False
			
			# ERROR
			else:
				success = False
				
		# Return
		return success
	
	def checkMarker(self, markerId):
		"""
		Method for checking if a specific marker is in the field.
	
		@return: active Is the specific marker active (True/False).
		"""
		active = False
		
		for i,j in self.markers.iteritems():
			if (j[0] == markerId):
				active = True
		return active
		
	def getMarkers(self):
		"""
		Method for getting a list w/ all active markers.
	
		@return: markers The active markers list.
		"""
		return self.markers
	
	def getMarkerData(self, markerId):
		"""
		Method for getting all data of a given marker.
		The data is [id, x, y, yaw].

		@param: markerId The marker id.
		@return: marker The marker data package.
		"""
		marker = [0]
		
		for i,j in self.markers.iteritems():
			if (j[0] == markerId):
				marker = j
		
		return marker
	
	def getMarkerPose(self, markerId):
		"""
		Method for getting the pose of a given marker.
		The data is [x, y, yaw].

		@param: markerId The marker id.
		@return: marker The marker data package.
		"""
		marker = [0]
		
		for i,j in self.markers.iteritems():
			if (j[0] == markerId):
				marker = j[1:4]
		
		return marker
	
	def getMarkerPosition(self, markerId):
		"""
		Method for getting the position of a given marker.
		The data is [x, y].

		@param: markerId The marker id.
		@return: marker The marker data package.
		"""
		marker = [0]

		for i,j in self.markers.iteritems():
			if (j[0] == markerId):
				marker = j[1:3]
		
		return marker
	
	def getMarkerYaw(self, markerId):
		"""
		Method for getting the position of a given marker.
		The data is [yaw].

		@param: markerId The marker id.
		@return: marker The marker data package.
		"""
		marker = [0]
		
		for i,j in self.markers.iteritems():
			if (j[0] == markerId):
				marker = j[3]
		
		return marker
	
	def getObstacles(self):
		"""
		Method for getting a list w/ all active obstacles.
	
		@return: obstacles The active obstacles list.
		"""
		return self.obstacles
	
	def getObstacle(self, obstacleId):
		"""
		Method for getting all data of a given obstacle.
		The data is [id, shape, x1, y1, x2, y2, x3, y3].

		@param: markerId The marker id.
		@return: marker The marker data package.
		"""
		obstacle = [0]
		
		for i,j in self.obstacles:
			if (j[0] == obstacleId):
				obstacle = j
		
		return obstacle
	
	def getMarkerCount(self):
		"""
		Method
		"""
		# Count.
		markerCount = len(self.markers)
		
		# Return.
		return markerCount
	
	def getObstacleCount(self):
		"""
		Method
		"""
		# Count.
		obstacleCount = len(self.obstacles)
		
		# Return.
		return obstacleCount
	
	def getObjectCount(self):
		"""
		Method
		"""
		# Count.
		objectCount = self.getMarkerCount() + self.getObstacleCount()
		
		# Return.
		return objectCount
	

