class SBYieldException(Exception):
	"""
	Basic exception for SByield app errors
	"""
	def __init__(self, msg=None):
		self.message = msg
		
		if msg is None:
			# Set some default useful error message
			self.message = "An error occurred"
			
		super(SBYieldException, self).__init__(msg)
