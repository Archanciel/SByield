from sbyieldexception import SBYieldException


class AfterNowPriceRequestDateError(SBYieldException):
	"""
	Exception raised when the date/time price PeiceRequester request
	is after now, so in the future.
	"""

	def __init__(self,
				 requesttDate):
		errorMsg = 'Price request date {} is after now, which is not acceptable !'

		errorMsg = errorMsg.format(requesttDate)

		super(AfterNowPriceRequestDateError, self).__init__(msg=errorMsg)
