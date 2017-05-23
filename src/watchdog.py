"""
Watchdog.

@Author: Rob Mertens
"""

class watchdog:
	# Local Imports.
	t = __import__('time')
	
	# Vars.
	__count = 0.0
	
	def __init__(self, target):
		"""
		Constructor
		"""
		self.__target = target
	
	def start(self):
		"""
		Method for starting the watchdog timer.
		"""
		self.__count = self.t.time()
	
	def hold(self):
		"""
		Method for achieving target time.
		"""
		current = self.t.time() - self.__count
		while (current <= self.__target):
			current = self.t.time() - self.__count


