from sbyieldexception import SBYieldException


class InvalidDepositDateTimeError(SBYieldException):
	"""
	Exception raised when the deposit CSV file contains a deposit whose time component is
	after the Swissborg yield payment time of 09:00:00 or if the tie compoonent format is
	invalid.
	"""

	def __init__(self,
				 depositCsvFilePathName,
				 owner,
				 depositDate,
				 depositAmount,
				 invalidTimeFormat = False):
		if not invalidTimeFormat:
			errorMsg = 'CSV file {} contains a deposit of {} for owner {} with a deposit ' \
'date of {} whose time component is later than the 09:00:00 Swissborg ' \
'yield payment time. Set the time to a value before 09:00:00 and retry.'
		else:
			errorMsg = 'CSV file {} contains a deposit of {} for owner {} with a deposit ' \
'date of {} whose format is invalid. Correct the date time component and retry.'

		errorMsg = errorMsg.format(depositCsvFilePathName,
								   depositAmount,
								   owner,
								   depositDate)

		super(InvalidDepositDateTimeError, self).__init__(msg=errorMsg)
