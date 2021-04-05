from sbyieldexception import SBYieldException


class InvalidDepositTimeError(SBYieldException):
    """
    Exception raised when the deposit CSV file contains a deposit whose date is after the
    last yield payment date.
    """

    def __init__(self,
                 depositCsvFilePathName,
                 owner,
                 depositDate,
                 depositAmount):
        errorMsg = 'CSV file {} contains a deposit of {} for owner {} with a deposit ' + \
                   'date {} whose time component is later than the 09:00:00 Swissborg ' + \
                   'yield payment time. Set the time to a value before 09:00:00 and retry.'
        errorMsg = errorMsg.format(depositCsvFilePathName,
                                   depositAmount,
                                   owner,
                                   depositDate)
    
        super(InvalidDepositTimeError, self).__init__(msg=errorMsg)
