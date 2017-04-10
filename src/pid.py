
class PID:
	"""
	Simple discrete PID-class.

	@Author: Rob Mertens
	"""	
	def __init__(self, kp, ki, kd, maxOutput, minOutput):
		"""
		Constructor
		"""        
		# Gain values
		self.kp = kp
		self.ki = ki
		self.kd = kd
		
		# Output limits
		self.minOutput = minOutput
		self.maxOutput = maxOutput
		
		# Interal vars for computation
		# Private vars
		self.__iTerm = 0.0
		self.__lastError = 0.0
		
		# Output value
		self.__output = 0.0
	
	def calculate(self, actual, desired):
		"""
		Method for calculating the PID output.
		"""
		# Calc error
		error = desired - actual
		
		# I-term calculations
		self.__iTerm += error
		
		# Output calculations
		self.__output = self.kp*error + self.ki*self.__iTerm + self.kd*(error - self.__lastError)
		if   (self.__output > self.maxOutput):self.__output = self.maxOutput
		elif (self.__output < self.minOutput):self.__output = self.minOutput        
		
		# Error update
		self.__lastError = error
		
		# Return statement
		return self.__output
	
	def setGainValues(self, kp, ki, kd):
		"""
		Method for setting the gain values
		"""
		self.kp = kp
		self.ki = ki
		self.kd = kd
	
	def setProportionalGain(self, kp):
		"""
		Method for getting the proportional gain value
		"""
        	self.kp = kp
	
	def setIntegralGain(self, ki):
		"""
		Method for getting the proportional gain value
		"""
		self.ki = ki
	
	def setDifferentailGain(self, kd):
		"""
		Method for getting the proportional gain value
		"""
	        self.kd = kd
        
	def setOutputLimits(self, maxOutput, minOutput):
		"""
		Method for setting the PID output.
		"""	
		self.minOutput = minOutput
		self.maxOutput = maxOutput
	
	def getProportionalGain(self):
		"""
		Method for getting the proportional gain value
		"""		
		return self.kp
	
	def getIntegralGain(self):
		"""
		Method for getting the integral gain value
		"""
		return self.ki
	
	def getDifferentialGain(self):
		"""
		Method for getting the differential gain value
		"""
		return self.kd
	
	def getOutputLimits(self):
		"""
		Method for getting the output limits
		"""		
		return [self.maxOutput, self.minOutput]
	
	def getMinOutputLimit(self):
		"""
		Method for getting the minimum output limit
		"""		
		return self.minOutput
	
	def getMaxOutputLimit(self):
		"""
		Method for getting the maximum output limit
		"""
		return self.maxOutput

