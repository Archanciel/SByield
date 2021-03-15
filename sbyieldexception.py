class SBYieldException(Exception):
	"""Basic exception for errors raised by cars"""
	def __init__(self, msg=None):
		self.message = msg
		
		if msg is None:
			# Set some default useful error message
			self.message = "An error occured"
		super(SBYieldException, self).__init__(msg)
