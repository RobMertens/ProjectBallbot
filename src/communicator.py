import pyre as p

class communicator:
	"""
	This class contains functions for the field of view for the EAGLE-camera.
	Every object found by the camera is kept in a dict.

	@Author: Rob Mertens
	"""
	# Imports.
	struct 	= __import__('struct')
	#pyre 	= __import__('pyre')
	__node = p.Pyre()
	
	# Self 
	
	def __init__(self, name, iface, port):
		"""
		Constructor.
		Initializes the pyre node.
	
		@param: name The name of the pyre node.
		"""
		self.__name = name
		self.__iface = iface
		self.__port = port
		
		__node.set_name(self.__name)
		__node.set_interface(self.__interface)
		__node.set_port(self.__port)
	
	def __init__(self, name, iface):
		"""
		Constructor.
		Initializes the pyre node.
	
		@param: name The name of the pyre node.
		"""
		self.__name = name
		self.__iface = iface
		
		__node.set_name(self.__name)
		__node.set_interface(self.__interface)
	
	def __init__(self, name):
		"""
		Constructor.
		Initializes the pyre node.
	
		@param: name The name of the pyre node.
		"""
		self.__name = name
		
		__node.set_name(self.__name)
	
	def __exit__(self):
		"""
		Destructor.
		Initializes the pyre node.
	
		@param: name The name of the pyre node.
		"""
		__node.stop()
	
	def start(self):
		"""
		Start.
		"""
		__node.start()
		#__poller = zmq.Poller()
    		#__poller.register(n.socket(), zmq.POLLIN)
	
	def stop(self):
		"""
		Stop node.
		"""
		__node.stop()
		#zpoller_destroy(__poller) 
	
	def join(self, group):
		"""
		Join group.
		"""
		__node.join(group)
	
	def leave(self, group):
		"""
		Leave group.
		"""
		__node.leave(group)
	
	def getName(self):
		"""
		Method for getting the zyre name.
		"""
		return self.__name
	
	def getActiveGroups(self):
		"""
		Join group.
		"""
		return __node.peer_groups()
	
	def recieve(self):	
		message = __node.recv()
		
		while(message[0] != 'SHOUT'):
		message = __node.recv()
		
		package = message[4]
		
		return message
	
	def recieveCommand(self):
		
		
	def unpack(self):
		"""
		Method for receiving signals from the camera.
		
		@return: Package w/ information.
		"""
		# Reset lists.
		byte = 0
		n = 0
		
		size = []
		data = []
				
		# Obtain information from camera.
		self.recieve()

		# Only take the camera data.
		package = message[4]

		# Loop through package.
		while(byte < len(package)):
			# Size.
			size[n] = struct.unpack('@Q', package[byte:(byte+8)])[0]
			byte += 8
			
			# Data.
			data[n] = struct.unpack('@i', package[byte:(byte+size[n])])[0]
			byte += size
			
			n += 1
				
		# Return
		return size, data








