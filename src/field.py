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
	robot = [0.0, 0.0, 0.0]
	obstacles = {}
	
	# Enum
	__MARKER   = 0
	__OBSTACLE = 1
	__IMAGE    = 2
	
	def __init__(self, name, group, marker):
		"""
		Constructor.
		Initializes the pyre node.
	
		@param: name The name of the pyre node.
		"""
		self.__name = name
		self.__group = group
		
		self.__node = p.Pyre(self.__name)
		self.__node.start()
		self.__node.join(self.__group)
		
		self.__marker = marker
		
		# UUID PC IBE
		self.uuid_self = self.__node.uuid()
		self.uuid_extern = self.__node.uuid()
		
		# Global vars.
		self.posXCam = 0.0
		self.posYCam = 0.0
		self.yawCam = 0.0
		self.posXEnd = 0.0
		self.posYEnd = 0.0
	
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
		
		# Obtain information from camera.
		message = self.__node.recv()
		while(message[0]!='SHOUT'):
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
				if(m_id==12):
					self.robot = [m_x, m_y, m_t]
					
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
				pass
			
			# ERROR
			else:
				pass
	
	
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
	
	def getRobotPose(self):
		return self.robot
	
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
	
	# --------------------------------------
	# THESE FUNCTIONS DO NOT BELONG TO FIELD
	# --------------------------------------
	def assignExternalUuid(self, name):
		"""
		Method for assigning the external UUID.
		"""
		ret = False
		peers = self.__node.peers()
		
		for p in peers:
			if(self.__node.get_peer_name(p)==name):
				self.uuid_extern = p
				ret = True
		
		return ret
	
	def whisperExternalUuid(self, msg):
		"""
		Whisper method
		"""
		self.__node.whisper(self.uuid_extern, msg)
	
	def receiveStartExternalUuid(self):
		"""
		Receive endpoint by whisper method from PC.
		"""
		ret = False
		
		self.whisperExternalUuid('START')
		
		message = self.__node.recv()
		while(message[0]!='WHISPER' and message[1]!=self.uuid_extern):
			message = self.__node.recv()
		
		if(message[3]=='ACK'):
			ret = True
		
		return ret
	
	def receiveEndpointExternalUuid(self):
		"""
		Receive endpoint by whisper method from PC.
		"""
		ret = False
		
		self.whisperExternalUuid('ENDPOINT')
		
		message = self.__node.recv()
		print(message)
		while(message[0]!='WHISPER'):
			message = self.__node.recv()
		
		if(message[3]!='ACK'):
			self.posXEnd, self.posYEnd = self.struct.unpack('@2f', message[3])
			ret = True
		
		return ret
	
	def getEndpoint(self):
		"""
		Get endpoint.
		"""
		return [self.posXEnd, self.posYEnd]

