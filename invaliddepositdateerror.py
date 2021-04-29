from sbyieldexception import SBYieldException


class InvalidDepositDateError(SBYieldException):
	"""
	Exception raised when the deposit CSV file contains a deposit whose date is after the
	last yield payment date.
	"""
	def __init__(self,
				 depositCsvFilePathName,
				 owner,
				 depositDate,
				 depositAmount,
				 yieldPaymentDate):
		errorMsg = "CSV file {} contains a deposit of {} for owner {} with a deposit \
date of {} which is after the last payment date of {}".format(depositCsvFilePathName,
															  depositAmount,
															  owner,
															  depositDate,
															  yieldPaymentDate)

		super(InvalidDepositDateError, self).__init__(msg=errorMsg)
