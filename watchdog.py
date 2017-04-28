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
		__count = t.time()
	
	def hold(self):
		"""
		Method for achieving target time.
		"""
		while (current <= target):
			current = t.time() - __count


